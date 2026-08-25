#!/usr/bin/env python3
"""CPRIS 微信端 REST API（AI 安全网关）认证与调用辅助脚本。

AI 网关：默认 http://testai.cpris.com，覆盖优先级 环境变量 CPRIS_AI_GATEWAY
        > 凭据文件 gateway 字段 > 默认值。
业务接口：{AI 网关}/ai/gw/{service}/{业务路径}（响应已经过敏感数据脱敏）
业务网关 http://test.cpris.com 是 AI 网关内部转发的目标，本脚本不直连。
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
  - 调用方认证只用请求头 X-Api-Key。AI 网关内部会拿它到 auth 的
    POST /ai/key/token 换登录 JWT，再以 Authorization: bearer {token} 转发下游，
    X-Api-Key 不透传；脚本不需要也不应该自己带 Authorization 头。
  - key 校验：长度 >= 8 且仅含 A-Za-z0-9-_. （通常以 ak- 开头，不强制）。key 是否
    有效最终由 auth 查 t_ai_key 判定（api_key 命中、end_date 空或未过期、绑定的
    员工存在且 is_login=1）。
  - 验证顺序：GET /ai/gw/health（白名单，探活）→ GET /ai/gw/user/user/info
    （带 X-Api-Key）。200 = 验证成功（保存）；401 = key 不存在或已过期（不保存）；
    403 看 msg：含「路径」= 本地 ACL 受限但 key 有效（保存），其他 403 = 换不到
    token（不保存）；405/429 = 认证已通过（保存）；502/503 = 认证服务或网关异常，
    有效性无法确认（不保存）。
  - saas 模块（登录/短信/数据字典等）与 auth 的 /ai/key/token 未对调用方开放，
    脚本直接拒绝。
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

# AI 网关默认地址；业务网关 http://test.cpris.com 是 AI 网关内部转发的目标，脚本不直连
DEFAULT_GATEWAY = "http://testai.cpris.com"
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
    # auth 的 API-Key 换 token 接口（/ai/key/token），只允许 AI 网关内部调用
    "ai",
}

# saas auth 服务下的精确路径（挂在 /parent 前缀下，但属于登录接口）
SAAS_EXACT_PATHS = {"/parent/phone/login", "/parent/wx/login"}


def gateway():
    """AI 网关地址：环境变量 CPRIS_AI_GATEWAY > 凭据文件 gateway 字段 > 默认值。"""
    env = os.environ.get("CPRIS_AI_GATEWAY")
    if env:
        return env.rstrip("/")
    creds = load_creds()
    if creds and creds.get("gateway"):
        return str(creds["gateway"]).rstrip("/")
    return DEFAULT_GATEWAY


def error_msg(body, default=""):
    """从网关/auth 的错误响应体 {"code":..,"msg":".."} 里取 msg。"""
    try:
        data = json.loads(body)
    except (TypeError, ValueError):
        return default
    if isinstance(data, dict):
        return str(data.get("msg") or default)
    return default


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
        "gateway": gateway(),
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
    url = gateway() + path
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
        print("❌ API-Key 无效或已过期（401），未保存。请向平台管理员确认该 key 是否已在"
              " auth 的 t_ai_key 表中登记、end_date 是否已过期。", file=sys.stderr)
        return 1
    if status == 403:
        msg = error_msg(body, "无权访问")
        if "路径" in msg:
            # AI 网关本地 ACL 拒绝：key 本身有效，只是 allowed-paths 受限
            save_creds(raw)
            print(f"⚠️  key 有效但无权访问验证路径（403：{msg}），已保存（{mask(raw)}）。"
                  "该 key 的 allowed-paths 受限，调用时请注意范围。")
            return 0
        # auth 侧拒绝：换不到登录 token（未绑定机构/用户、账号禁用、机构过期等）
        print(f"❌ 该 API-Key 无法换取登录 token（403：{msg}），未保存。请管理员检查"
              " t_ai_key 的 merchant_id/employee_id 绑定与 t_employee 的 is_login 状态。",
              file=sys.stderr)
        return 1
    if status in (405, 429):
        save_creds(raw)
        reason = {405: "方法受限（405）", 429: "触发限流（429）"}[status]
        print(f"⚠️  key 认证已通过，但验证请求未成功：{reason}。已保存（{mask(raw)}）。")
        return 0
    if status in (502, 503):
        reason = {502: "认证服务返回异常或下游不可达（502）",
                  503: "网关已停用或认证服务不可达（503）"}[status]
        print(f"⚠️  {reason}，无法确认 key 有效性，未保存。响应片段：{body[:200]}",
              file=sys.stderr)
        return 1
    print(f"⚠️  验证返回 HTTP {status}，无法确认 key 有效性，未保存。"
          f"响应片段：{body[:200]}", file=sys.stderr)
    return 1


def cmd_status():
    creds = load_creds()
    if not creds or not creds.get("apiKey"):
        print("未配置：无有效 API-Key。请使用 'login <api-key>' 提供 AI 网关 API-Key。")
        return 1
    print(f"已配置 | AI 网关: {gateway()} | "
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
        print("❌ API-Key 已失效（401）：t_ai_key 中查不到该 key 或 end_date 已过期，"
              "已清除凭据。请重新获取并登录。", file=sys.stderr)
        return 1
    if status == 403:
        msg = error_msg(resp, "无权访问")
        if "路径" in msg:
            print(f"❌ 该 API-Key 无权访问此路径（403：{msg}）：路径不在 key 的 "
                  "allowed-paths 范围内，不要重试。请向管理员申请扩大范围。",
                  file=sys.stderr)
        else:
            print(f"❌ 该 API-Key 无法换取登录 token（403：{msg}）：可能未绑定机构/用户、"
                  "绑定账号已禁用或机构已过期。凭据保留，请联系管理员处理。",
                  file=sys.stderr)
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
        print("❌ 认证服务返回异常、下游服务不可达或脱敏处理失败（502）。请稍后重试；"
              "禁止绕过网关直连业务服务。", file=sys.stderr)
        print(resp)
        return 1
    if status == 503:
        print("❌ AI 网关已停用，或认证服务（auth）不可达（503）。凭据保留，"
              "请联系管理员。", file=sys.stderr)
        return 1
    print(f"HTTP {status}")
    print(resp)
    return 0 if 200 <= status < 300 else 1


def main():
    parser = argparse.ArgumentParser(description="CPRIS AI 网关认证与调用辅助")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_login = sub.add_parser("login", help="验证并保存 AI 网关 API-Key")
    p_login.add_argument("api_key",
                         help="AI 网关 API-Key（登记在 t_ai_key，通常以 ak- 开头）")

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
