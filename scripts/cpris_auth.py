#!/usr/bin/env python3
"""CPRIS 微信端 REST API 认证与调用辅助脚本。

固定网关：http://test.cpris.com
凭据文件：${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json
           （HERMES_HOME 未设置时回退到 ~/.hermes/...）

用法：
  python cpris_auth.py login <token>      验证并保存 Token
  python cpris_auth.py status             查看当前登录状态
  python cpris_auth.py logout             清除已保存的 Token
  python cpris_auth.py call <METHOD> <path> [--body '<json>'] [--query k=v ...]
                                          用已保存 Token 调用接口

说明：
  - Token 校验：去掉可选 "Bearer " 前缀后长度 >= 64 且为 Base64/Base64URL 字符集。
  - 验证依据：GET /user/info 返回 HTTP 200。先原样发送；若无前缀且 401/403，
    则重试一次 "Bearer <token>"。
  - 展示 Token 时仅保留首尾各 6 字符。
"""
import json
import os
import re
import sys
import argparse
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone

GATEWAY = "http://test.cpris.com"
VERIFY_PATH = "/user/info"
_B64_RE = re.compile(r"^[A-Za-z0-9+/_-]+={0,2}$")


def creds_path():
    home = os.environ.get("HERMES_HOME") or os.path.join(
        os.path.expanduser("~"), ".hermes"
    )
    return os.path.join(home, "cpris-wxapp-rest-api", "credentials.json")


def mask(value):
    if not value:
        return "(空)"
    core = value[7:] if value.lower().startswith("bearer ") else value
    if len(core) <= 12:
        return "***"
    return f"{core[:6]}...{core[-6:]}"


def load_creds():
    path = creds_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_creds(authorization):
    path = creds_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "gateway": GATEWAY,
        "authorization": authorization,
        "validatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return data


def is_token_candidate(raw):
    core = raw[7:] if raw.lower().startswith("bearer ") else raw
    core = core.strip()
    return len(core) >= 64 and bool(_B64_RE.match(core))


def _request(method, path, authorization, body=None, query=None):
    url = GATEWAY + path
    if query:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(query)
    headers = {"Authorization": authorization}
    data = None
    if body is not None:
        data = body.encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except urllib.error.URLError as e:
        return None, f"网络错误: {e.reason}"


def cmd_login(token):
    raw = token.strip()
    if not is_token_candidate(raw):
        print("❌ Token 格式不符：去掉可选 'Bearer ' 前缀后需 >= 64 字符且为 "
              "Base64/Base64URL 字符集。", file=sys.stderr)
        return 2

    has_prefix = raw.lower().startswith("bearer ")
    core = raw[7:].strip() if has_prefix else raw

    # 尝试 1：原样发送
    attempts = [raw]
    # 尝试 2：仅当无前缀时，追加 Bearer 重试
    if not has_prefix:
        attempts.append(f"Bearer {core}")

    for authz in attempts:
        status, body = _request("GET", VERIFY_PATH, authz)
        if status is None:
            print(f"⚠️  {body}，未修改现有凭据。", file=sys.stderr)
            return 1
        if status == 200:
            save_creds(authz)
            print(f"✅ 验证成功，已保存 Token（{mask(authz)}）到 {creds_path()}")
            return 0
        if status not in (401, 403):
            print(f"⚠️  验证返回 HTTP {status}，无法确认登录，未保存。响应片段："
                  f"{body[:200]}", file=sys.stderr)
            return 1
    print("❌ Token 无效或已过期（401/403），未保存。请重新提供有效 Token。",
          file=sys.stderr)
    return 1


def cmd_status():
    creds = load_creds()
    if not creds or not creds.get("authorization"):
        print("未登录：无有效凭据。请使用 'login <token>' 提供登录 Token。")
        return 1
    print(f"已登录 | 网关: {creds.get('gateway', GATEWAY)} | "
          f"Token: {mask(creds['authorization'])} | "
          f"验证时间: {creds.get('validatedAt', '未知')}")
    return 0


def cmd_logout():
    path = creds_path()
    if os.path.isfile(path):
        os.remove(path)
        print(f"✅ 已清除凭据文件：{path}")
    else:
        print("无凭据文件可清除。")
    return 0


def cmd_call(method, path, body=None, query_pairs=None):
    creds = load_creds()
    if not creds or not creds.get("authorization"):
        print("❌ 未登录：请先使用 'login <token>' 提供登录 Token。", file=sys.stderr)
        return 1
    query = {}
    for pair in (query_pairs or []):
        if "=" in pair:
            k, v = pair.split("=", 1)
            query[k] = v
    if not path.startswith("/"):
        path = "/" + path
    status, resp = _request(
        method.upper(), path, creds["authorization"], body=body, query=query
    )
    if status is None:
        print(f"⚠️  {resp}", file=sys.stderr)
        return 1
    if status in (401, 403):
        cmd_logout()
        print(f"❌ Token 已失效（HTTP {status}），已清除凭据。请重新登录。",
              file=sys.stderr)
        return 1
    print(f"HTTP {status}")
    print(resp)
    return 0 if 200 <= status < 300 else 1


def main():
    parser = argparse.ArgumentParser(description="CPRIS REST API 认证与调用辅助")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_login = sub.add_parser("login", help="验证并保存 Token")
    p_login.add_argument("token", help="登录 Token（可含 Bearer 前缀）")

    sub.add_parser("status", help="查看登录状态")
    sub.add_parser("logout", help="清除已保存的 Token")

    p_call = sub.add_parser("call", help="调用受保护接口")
    p_call.add_argument("method", help="HTTP 方法，如 GET/POST")
    p_call.add_argument("path", help="接口路径，如 /user/info")
    p_call.add_argument("--body", help="JSON 请求体字符串", default=None)
    p_call.add_argument("--query", nargs="*", help="查询参数 k=v", default=None)

    args = parser.parse_args()
    if args.cmd == "login":
        return cmd_login(args.token)
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "logout":
        return cmd_logout()
    if args.cmd == "call":
        return cmd_call(args.method, args.path, args.body, args.query)
    return 2


if __name__ == "__main__":
    sys.exit(main())
