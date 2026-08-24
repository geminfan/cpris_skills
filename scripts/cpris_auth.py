#!/usr/bin/env python3
"""CPRIS 微信端 REST API（AI 安全网关）认证与调用辅助脚本。

固定网关：https://teacherwx.cpris.com
业务接口：{网关}/ai/gw/{service}/{业务路径}（响应已经过敏感数据脱敏）
凭据文件：${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json
           （HERMES_HOME 未设置时回退到 ~/.hermes/...）

用法：
  python cpris_auth.py login <api-key>    验证并保存 AI 网关 API-Key
  python cpris_auth.py status             查看当前配置状态
  python cpris_auth.py logout             清除已保存的 API-Key
  python cpris_auth.py call <METHOD> <path> [--body '<json>'] [--query k=v ...]
                                          用已保存 key 调用接口；业务路径
                                          （如 /user/info）会自动补
                                          /ai/gw/{service} 前缀，也可直接
                                          给完整网关路径 /ai/gw/user/user/info

说明：
  - key 校验：长度 >= 8 且仅含 A-Za-z0-9-_. （通常以 ak- 开头，不强制）。
  - 验证顺序：GET /ai/gw/health（白名单，探活）→ GET /ai/gw/user/user/info
    （带 X-Api-Key）。401 = key 无效；200 = 验证成功；403/405/429/502 =
    认证已通过但权限/频率/下游受限（保存并提示）；503 = 网关停用，不保存。
  - saas 模块（登录/短信/数据字典等）未对 AI 网关开放，脚本直接拒绝。
  - 展示 key 时仅保留首尾各 4 字符。
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

GATEWAY = "https://teacherwx.cpris.com"
HEALTH_PATH = "/ai/gw/health"
VERIFY_PATH = "/ai/gw/user/user/info"
GW_PREFIX = "/ai/gw/"
_KEY_RE = re.compile(r"^[A-Za-z0-9\-_.]+$")

# 业务路径首段 -> 网关 service 名（与 cpris_wxapp/ai 的 routes 配置一致）
SEGMENT_TO_SERVICE = {
    "user": "user",
    "childrenInfo": "children",
    "guardian": "children",
    "parent": "parent",
    "training": "training",
    "team": "training",
    "periodical": "training",
    "iepLib": "training",
    "assess": "assess",
    "assessDefine": "assess",
    "assessGuide": "assess",
}

# saas 模块未对 AI 网关开放（敏感数据处理规范）
SAAS_SEGMENTS = {
    "login", "loginOut", "phone", "wx", "auth", "data", "files",
    "nation", "region", "sysBasedata",
}

# saas auth 服务下的精确路径（挂在 /parent 前缀下，但属于登录接口）
SAAS_EXACT_PATHS = {"/parent/phone/login", "/parent/wx/login"}


def creds_path():
    home = os.environ.get("HERMES_HOME") or os.path.join(
        os.path.expanduser("~"), ".hermes"
    )
    return os.path.join(home, "cpris-wxapp-rest-api", "credentials.json")


def mask(value):
    if not value:
        return "(空)"
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}...{value[-4:]}"


def load_creds():
    path = creds_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_creds(api_key):
    path = creds_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "gateway": GATEWAY,
        "apiKey": api_key,
        "validatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return data


def is_key_candidate(raw):
    raw = raw.strip()
    return len(raw) >= 8 and bool(_KEY_RE.match(raw))


def to_gateway_path(path):
    """业务路径 -> 网关路径。已是 /ai/gw/ 前缀则原样返回。"""
    if not path.startswith("/"):
        path = "/" + path
    if path.startswith(GW_PREFIX):
        return path
    if path in SAAS_EXACT_PATHS:
        raise ValueError(
            f"{path} 是 saas 模块登录接口，未对 AI 网关开放，禁止调用。"
        )
    segment = path.split("/", 2)[1] if path.count("/") >= 1 else ""
    if segment in SAAS_SEGMENTS:
        raise ValueError(
            f"/{segment} 属于 saas 模块（登录/短信/数据字典），未对 AI 网关开放，禁止调用。"
        )
    service = SEGMENT_TO_SERVICE.get(segment)
    if service is None:
        raise ValueError(
            f"无法识别业务路径 /{segment} 对应的网关服务。"
            f"可用前缀：{', '.join(sorted(SEGMENT_TO_SERVICE))}；"
            "或直接传入完整网关路径 /ai/gw/{service}/..."
        )
    return f"{GW_PREFIX}{service}{path}"


def _request(method, path, api_key=None, body=None, query=None):
    url = GATEWAY + path
    if query:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(query)
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
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


def cmd_login(api_key):
    raw = api_key.strip()
    if not is_key_candidate(raw):
        print("❌ API-Key 格式不符：需 >= 8 字符且仅含 A-Za-z0-9-_. （通常以 ak- 开头）。",
              file=sys.stderr)
        return 2

    # 1. 网关探活（白名单，无需 key）
    status, body = _request("GET", HEALTH_PATH)
    if status is None:
        print(f"⚠️  网关不可达：{body}，未保存 key。", file=sys.stderr)
        return 1
    if status == 503:
        print("⚠️  AI 网关总开关已关闭（503），无法验证 key，未保存。", file=sys.stderr)
        return 1
    if status != 200:
        print(f"⚠️  网关健康检查返回 HTTP {status}，无法确认网关状态，未保存。"
              f"响应片段：{body[:200]}", file=sys.stderr)
        return 1

    # 2. 验证 key
    status, body = _request("GET", VERIFY_PATH, api_key=raw)
    if status is None:
        print(f"⚠️  {body}，未保存 key。", file=sys.stderr)
        return 1
    if status == 200:
        save_creds(raw)
        print(f"✅ 验证成功，已保存 API-Key（{mask(raw)}）到 {creds_path()}")
        return 0
    if status == 401:
        print("❌ API-Key 无效（401），未保存。请向平台管理员确认 key 是否已在"
              " cpris.ai-gateway.auth.api-keys 中登记。", file=sys.stderr)
        return 1
    if status == 403:
        save_creds(raw)
        print(f"⚠️  key 认证有效但无权访问验证路径（403），已保存（{mask(raw)}）。"
              "该 key 的允许路径受限，调用时请注意范围。")
        return 0
    if status in (405, 429, 502):
        save_creds(raw)
        reason = {405: "方法受限（405）", 429: "触发限流（429）",
                  502: "下游服务暂不可达（502）"}[status]
        print(f"⚠️  key 认证已通过，但验证请求未成功：{reason}。已保存（{mask(raw)}）。")
        return 0
    print(f"⚠️  验证返回 HTTP {status}，无法确认 key 有效性，未保存。"
          f"响应片段：{body[:200]}", file=sys.stderr)
    return 1


def cmd_status():
    creds = load_creds()
    if not creds or not creds.get("apiKey"):
        print("未配置：无有效 API-Key。请使用 'login <api-key>' 提供 AI 网关 API-Key。")
        return 1
    print(f"已配置 | 网关: {creds.get('gateway', GATEWAY)} | "
          f"API-Key: {mask(creds['apiKey'])} | "
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
    if not creds or not creds.get("apiKey"):
        print("❌ 未配置：请先使用 'login <api-key>' 提供 AI 网关 API-Key。",
              file=sys.stderr)
        return 1
    try:
        gw_path = to_gateway_path(path)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 2
    query = {}
    for pair in (query_pairs or []):
        if "=" in pair:
            k, v = pair.split("=", 1)
            query[k] = v
    status, resp = _request(
        method.upper(), gw_path, creds["apiKey"], body=body, query=query
    )
    if status is None:
        print(f"⚠️  {resp}", file=sys.stderr)
        return 1
    if status == 401:
        cmd_logout()
        print("❌ API-Key 已失效（401），已清除凭据。请重新获取并登录。",
              file=sys.stderr)
        return 1
    if status == 403:
        print("❌ 该 API-Key 无权访问此路径（403）：路径不在 key 的允许范围内，"
              "不要重试。请向管理员申请扩大 allowed-paths。", file=sys.stderr)
        print(resp)
        return 1
    if status == 405:
        print(f"❌ 该 API-Key 不允许使用 {method.upper()} 方法（405）。",
              file=sys.stderr)
        print(resp)
        return 1
    if status == 429:
        print("❌ 请求过于频繁（429）：已触发限流，请等待约 60 秒后重试。",
              file=sys.stderr)
        return 1
    if status == 502:
        print("❌ 下游服务不可达或脱敏处理失败（502）。请稍后重试；"
              "禁止绕过网关直连业务服务。", file=sys.stderr)
        print(resp)
        return 1
    if status == 503:
        print("❌ AI 网关已停用（503）。请联系管理员。", file=sys.stderr)
        return 1
    print(f"HTTP {status}")
    print(resp)
    return 0 if 200 <= status < 300 else 1


def main():
    parser = argparse.ArgumentParser(description="CPRIS AI 网关认证与调用辅助")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_login = sub.add_parser("login", help="验证并保存 AI 网关 API-Key")
    p_login.add_argument("api_key", help="AI 网关签发的 API-Key（通常以 ak- 开头）")

    sub.add_parser("status", help="查看当前配置状态")
    sub.add_parser("logout", help="清除已保存的 API-Key")

    p_call = sub.add_parser("call", help="通过 AI 网关调用接口")
    p_call.add_argument("method", help="HTTP 方法，如 GET/POST")
    p_call.add_argument("path", help="业务路径（如 /user/info）或完整网关路径"
                                     "（如 /ai/gw/user/user/info）")
    p_call.add_argument("--body", help="JSON 请求体字符串", default=None)
    p_call.add_argument("--query", nargs="*", help="查询参数 k=v", default=None)

    args = parser.parse_args()
    if args.cmd == "login":
        return cmd_login(args.api_key)
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "logout":
        return cmd_logout()
    if args.cmd == "call":
        return cmd_call(args.method, args.path, args.body, args.query)
    return 2


if __name__ == "__main__":
    sys.exit(main())
