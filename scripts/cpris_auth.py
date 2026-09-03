#!/usr/bin/env python3
"""Portable CPRIS AI gateway client; Python 3.9+ standard library only."""
import argparse
import base64
import ctypes
import getpass
import http.client
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / "references" / "gateway-config.json"
HEALTH_PATH = "/ai/gw/health"
VERIFY_PATH = "/ai/gw/user/user/info"
PREFIX = "/ai/gw/"
DELETE_WORDS = ("delete", "remove", "destroy", "erase", "purge", "删除", "移除", "清除", "销毁")
METHODS = ("GET", "POST", "PUT", "PATCH", "HEAD", "OPTIONS")


class ClientError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_json(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ClientError("无法读取 JSON 配置或凭据文件，请检查文件格式和访问权限。") from None
    if not isinstance(value, dict):
        raise ClientError("配置或凭据文件必须是 JSON 对象。")
    return value


def config_root():
    custom = os.environ.get("CPRIS_CONFIG_HOME")
    if custom:
        root = Path(custom).expanduser()
        if not root.is_absolute():
            raise ClientError("CPRIS_CONFIG_HOME 必须是工作区之外的绝对路径。")
    elif os.name == "nt":
        root = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming") / "cpris"
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "cpris"
    root = root.resolve()
    if root.is_relative_to(Path(__file__).resolve().parents[1]) or root.is_relative_to(Path.cwd().resolve()):
        raise ClientError("凭据目录必须位于 Skill 和当前工作区之外。")
    if any((parent / ".git").exists() for parent in (root, *root.parents)):
        raise ClientError("凭据目录不能位于 Git 仓库内。")
    return root / "cpris-wxapp-rest-api"


def check_key(value):
    if not isinstance(value, str) or not value.strip():
        raise ClientError("未配置 API-Key；请通过 login、安全环境变量或智能体密钥管理器提供。")
    value = value.strip()
    # The server imposes no 'ak-' prefix or minimum length; reject unsafe header bytes.
    if any(ord(char) < 33 or ord(char) > 126 for char in value):
        raise ClientError("API-Key 必须是不含空白和控制字符的可见 ASCII 字符串。")
    return value


def protect_windows(data, decrypt=False):
    """DPAPI binds encrypted credentials to the current Windows user."""
    class Blob(ctypes.Structure):
        _fields_ = [("size", ctypes.c_uint32), ("data", ctypes.POINTER(ctypes.c_ubyte))]
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    result = Blob()
    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    function = crypt32.CryptUnprotectData if decrypt else crypt32.CryptProtectData
    function.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p,
                         ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(Blob)]
    function.restype = ctypes.c_int
    if not function(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(result)):
        raise ClientError("Windows 用户凭据加密/解密失败；请在原用户环境操作或重新登录。")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    kernel32.LocalFree.restype = ctypes.c_void_p
    try:
        return ctypes.string_at(result.data, result.size)
    finally:
        kernel32.LocalFree(ctypes.cast(result.data, ctypes.c_void_p))


def redact_key(value, key):
    if isinstance(value, str):
        return value.replace(key, "[REDACTED]")
    if isinstance(value, list):
        return [redact_key(item, key) for item in value]
    if isinstance(value, dict):
        return {name.replace(key, "[REDACTED]"): redact_key(item, key) for name, item in value.items()}
    return value


class Client:
    def __init__(self, args):
        self.config = read_json(CONFIG)
        environments = self.config["environments"]
        chosen = args.env or os.environ.get("CPRIS_ENV")
        override = args.gateway or os.environ.get("CPRIS_AI_GATEWAY")
        if override:
            override = override.rstrip("/")
            matching = [name for name, item in environments.items() if item["aiGateway"] == override]
            if not matching or (chosen and chosen != matching[0]):
                raise ClientError("AI 网关必须匹配已配置的测试或正式地址，且与所选环境一致。")
            chosen = matching[0]
        self.environment = chosen or self.config["defaultEnvironment"]
        if self.environment not in environments:
            raise ClientError("CPRIS_ENV 仅支持 test 或 production。")
        self.gateway = environments[self.environment]["aiGateway"]
        self.path = config_root() / self.environment / "credentials.json"
        self.timeout = args.timeout
        self.opener = urllib.request.build_opener(NoRedirect())

    def credentials(self):
        if not self.path.exists():
            return {}
        value = read_json(self.path)
        if value.get("gateway") != self.gateway or value.get("environment") != self.environment:
            raise ClientError("凭据绑定的环境或网关不匹配，请在当前环境重新登录。")
        if "apiKeyProtected" in value:
            if os.name != "nt":
                raise ClientError("Windows 加密凭据不能在其他操作系统读取，请重新登录。")
            encrypted = base64.b64decode(value["apiKeyProtected"], validate=True)
            value["apiKey"] = protect_windows(encrypted, decrypt=True).decode("utf-8")
        elif os.name == "nt" and value.get("apiKey"):
            raise ClientError("Windows 本地凭据必须使用 DPAPI 加密，请重新登录。")
        return value

    def key(self):
        scoped = os.environ.get("CPRIS_" + self.environment.upper() + "_API_KEY")
        if scoped:
            return check_key(scoped), "environment"
        generic = os.environ.get("CPRIS_API_KEY")
        if generic:
            if os.environ.get("CPRIS_API_KEY_GATEWAY", "").rstrip("/") != self.gateway:
                raise ClientError("CPRIS_API_KEY 必须同时设置匹配当前网关的 CPRIS_API_KEY_GATEWAY。")
            return check_key(generic), "environment"
        return check_key(self.credentials().get("apiKey")), "file"

    def gateway_path(self, raw, method):
        if method not in METHODS:
            raise ClientError("不支持该 HTTP 方法；AI 网关禁止 DELETE。")
        if not raw or re.search(r"[\x00-\x20\x7f]", raw) or "\\" in raw:
            raise ClientError("路径不可为空或包含空白、控制字符、反斜杠。")
        parsed = urllib.parse.urlsplit(raw)
        if parsed.scheme or parsed.netloc or parsed.fragment or raw.startswith("//"):
            raise ClientError("仅接受业务相对路径或 /ai/gw 路径，不接受 URL 或片段。")
        path = parsed.path if parsed.path.startswith("/") else "/" + parsed.path
        if re.search(r"%(?![0-9a-fA-F]{2})", path):
            raise ClientError("路径含无效百分号编码。")
        decoded = urllib.parse.unquote(path, errors="strict")
        if "%" in decoded or any(char in decoded for char in "\\;?#") or "//" in decoded:
            raise ClientError("路径含重复编码、路径参数或非法分隔符。")
        if re.search(r"[\x00-\x20\x7f]", decoded) or any(part in (".", "..") for part in decoded.split("/")):
            raise ClientError("路径含控制字符或目录跳转。")
        lower = decoded.lower()
        if any(word in lower for word in DELETE_WORDS) or any(
            part == "del" or part.startswith(("del-", "del_")) for part in lower.split("/")
        ):
            raise ClientError("AI 网关禁止删除接口，不能通过更换方法或编码绕过。")
        if decoded == HEALTH_PATH:
            if method != "GET":
                raise ClientError("健康检查只接受 GET。")
            return HEALTH_PATH + ("?" + parsed.query if parsed.query else "")
        service, business = None, decoded
        if decoded.startswith(PREFIX):
            parts = decoded[len(PREFIX):].split("/", 1)
            if len(parts) != 2 or not parts[1]:
                raise ClientError("网关路径必须包含 service 和业务路径。")
            service, business = parts[0], "/" + parts[1]
        segment = business.split("/", 2)[1]
        if segment in self.config["blockedPrefixes"] or any(
            business == item or business.startswith(item + "/") for item in self.config["blockedPaths"]
        ):
            raise ClientError("登录、短信、内部换 token 和未开放的 SaaS 路径不可调用。")
        expected = self.config["prefixToService"].get(segment)
        if not expected or (service and service != expected):
            raise ClientError("业务路径未配置服务映射，或完整网关路径的服务与业务前缀不匹配。")
        encoded = urllib.parse.quote(PREFIX + expected + business, safe="/-._~")
        return encoded + ("?" + parsed.query if parsed.query else "")

    def request(self, method, path, key=None, body=None, query=None):
        path = self.gateway_path(path, method)
        pairs = urllib.parse.parse_qsl(urllib.parse.urlsplit(path).query, keep_blank_values=True)
        pairs.extend(query or [])
        forbidden = {"apikey", "xapikey", "authorization", "accesstoken", "token",
                     "method", "methodoverride", "httpmethodoverride", "xhttpmethodoverride"}
        if any(re.sub(r"[^a-z0-9]", "", name.lower()) in forbidden for name, _ in pairs):
            raise ClientError("不能在查询参数中传递凭据或覆盖 HTTP 方法。")
        if key and (key in urllib.parse.unquote(path) or any(key in name or key in value for name, value in pairs)):
            raise ClientError("路径和查询参数不可包含 API-Key。")
        if key and body is not None and key in body.decode("utf-8"):
            raise ClientError("JSON 请求体不可包含 API-Key。")
        url = self.gateway + path
        if query:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(query)
        headers = {"Accept": "application/json"}
        if key and urllib.parse.urlsplit(path).path != HEALTH_PATH:
            headers["X-Api-Key"] = key
        if body is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            response = self.opener.open(req, timeout=self.timeout)
        except urllib.error.HTTPError as error:
            response = error
        except (urllib.error.URLError, TimeoutError, OSError):
            raise ClientError("网络请求失败或超时；凭据保留，写操作请先确认结果再决定是否重试。") from None
        with response:
            status = response.code
            try:
                content = json.loads(response.read().decode("utf-8"))
            except (UnicodeError, ValueError):
                content = None
            content_type = response.headers.get_content_type()
        # Backend error responses bypass masking; do not expose their original text or data.
        if not 200 <= status < 300:
            known = {
                401: "认证失败；可能是密钥失效或下游认证失败。凭据保留，请重新登录或联系管理员。",
                403: "路径权限、删除禁令或账号/机构登录资格限制；不要绕过或重试同一操作。",
                404: "服务路由或接口不存在，请核对当前部署。",
                405: "HTTP 方法不被允许；不可自行改用其他方法重试。",
                429: "触发限流；读取请求可稍后重试，写请求不要自动重放。",
                502: "认证服务、业务服务或脱敏处理异常。",
                503: "AI 网关已停用或认证服务不可达。",
            }
            return {"ok": False, "httpStatus": status, "error": known.get(status, "网关返回非成功状态；重定向不会被跟随。")}
        is_health = urllib.parse.urlsplit(path).path == HEALTH_PATH
        if content is None or (not is_health and content_type != "application/json"):
            return {"ok": False, "httpStatus": status, "error": "响应不是受支持的 JSON；未展示未经确认脱敏的内容。"}
        code = content.get("code") if isinstance(content, dict) else None
        if code is not None and str(code) != "200":
            safe_code = code if isinstance(code, int) or (isinstance(code, str) and code.isdigit() and len(code) <= 6) else None
            return {"ok": False, "httpStatus": status, "businessCode": safe_code, "error": "业务返回失败；HTTP 成功不代表业务成功。"}
        if key:
            content = redact_key(content, key)
        return {"ok": True, "httpStatus": status, "data": content}

    def save(self, key):
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        value = {"environment": self.environment, "gateway": self.gateway,
                 "validatedAt": datetime.now(timezone.utc).isoformat()}
        if os.name == "nt":
            value["apiKeyProtected"] = base64.b64encode(protect_windows(key.encode("utf-8"))).decode("ascii")
        else:
            os.chmod(self.path.parent, 0o700)
            value["apiKey"] = key
        temporary = None
        try:
            fd, temporary = tempfile.mkstemp(dir=self.path.parent, prefix=".credentials-")
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(value, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            os.replace(temporary, self.path)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)


def emit(result):
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


def main():
    parser = argparse.ArgumentParser(description="CPRIS AI 网关客户端（默认测试环境）")
    parser.add_argument("--env", choices=("test", "production"))
    parser.add_argument("--gateway", help="已配置的 AI 网关地址；兼容 CPRIS_AI_GATEWAY")
    parser.add_argument("--timeout", type=float, default=30)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health", help="无需密钥的健康检查")
    sub.add_parser("status", help="查看当前环境配置，不请求网络")
    sub.add_parser("logout", help="清除当前环境的本地凭据")
    login = sub.add_parser("login", help="通过 /user/info 验证密钥")
    login.add_argument("--key-stdin", action="store_true", help="从标准输入读取密钥")
    login.add_argument("--no-save", action="store_true", help="只验证，不持久化")
    call = sub.add_parser("call", help="通过 AI 网关调用 JSON 接口")
    call.add_argument("method", type=str.upper, choices=METHODS)
    call.add_argument("path")
    bodies = call.add_mutually_exclusive_group()
    bodies.add_argument("--body", help="JSON 请求体")
    bodies.add_argument("--body-file", type=Path, help="UTF-8 JSON 请求文件")
    call.add_argument("--query", nargs="*", default=[], help="查询参数 key=value，支持重复键")
    args = parser.parse_args()
    if not 0 < args.timeout <= 300:
        raise ClientError("timeout 必须在 0 到 300 秒之间。")
    client = Client(args)
    if args.command == "health":
        return emit(client.request("GET", HEALTH_PATH))
    if args.command == "status":
        try:
            _, source = client.key()
        except ClientError as error:
            return emit({"ok": False, "environment": client.environment, "gateway": client.gateway, "error": str(error)})
        return emit({"ok": True, "environment": client.environment, "gateway": client.gateway,
                     "credentialSource": source, "message": "本地状态不代表当前密钥有效性。"})
    if args.command == "logout":
        client.path.unlink(missing_ok=True)
        return emit({"ok": True, "environment": client.environment,
                     "message": "已清除当前环境的本地凭据；环境变量请在调用进程或密钥管理器中清除。"})
    if args.command == "login":
        if args.key_stdin:
            key = check_key(sys.stdin.readline().rstrip("\r\n"))
        elif any(os.environ.get(name) for name in ("CPRIS_API_KEY", "CPRIS_" + client.environment.upper() + "_API_KEY")):
            key, _ = client.key()
        elif sys.stdin.isatty():
            key = check_key(getpass.getpass("CPRIS API-Key: "))
        else:
            raise ClientError("非交互环境请使用密钥环境变量或 --key-stdin。")
        result = client.request("GET", HEALTH_PATH)
        if not result["ok"]:
            return emit(result)
        result = client.request("GET", VERIFY_PATH, key)
        data = result.get("data")
        if result["ok"] and not (isinstance(data, dict) and str(data.get("code")) == "200" and isinstance(data.get("data"), dict) and data["data"]):
            result = {"ok": False, "error": "验证接口未返回预期的用户信息，未保存密钥。"}
        if not result["ok"]:
            return emit(result)
        if not args.no_save:
            client.save(key)
        return emit({"ok": True, "environment": client.environment, "saved": not args.no_save,
                     "message": "用户信息接口验证成功。"})
    path = client.gateway_path(args.path, args.method)
    body = args.body_file.read_text(encoding="utf-8-sig") if args.body_file else args.body
    if body is not None:
        if args.method not in ("POST", "PUT", "PATCH"):
            raise ClientError("该方法不接受 JSON 请求体。")
        body = json.dumps(json.loads(body), ensure_ascii=False, allow_nan=False).encode("utf-8")
    query = []
    for pair in args.query:
        if "=" not in pair or not pair.split("=", 1)[0]:
            raise ClientError("查询参数必须使用非空 key=value 格式。")
        query.append(tuple(pair.split("=", 1)))
    key = None if urllib.parse.urlsplit(path).path == HEALTH_PATH else client.key()[0]
    return emit(client.request(args.method, path, key, body, query))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ClientError as error:
        emit({"ok": False, "error": str(error)})
        sys.exit(2)
    except (OSError, ValueError, KeyError, TypeError, http.client.HTTPException):
        emit({"ok": False, "error": "配置、输入或文件操作失败；未输出可能含敏感数据的异常原文。"})
        sys.exit(2)
