#!/usr/bin/env python3
"""bs-webctl — 独立浏览器控制 CLI，供任意 AI Agent 使用。

用法:
  bs-webctl sessions                    列出所有浏览器标签页
  bs-webctl scan [--text-only] [--tabs-only] [--tab-id ID] [--maxlen N]
                                                 获取当前页简化 HTML/文本
  bs-webctl exec <script> [--tab-id ID] [--no-monitor] [--save-to PATH]
                                                 在浏览器中执行 JS，返回结果 + DOM diff
  bs-webctl exec-file <path> [...]        从文件读 JS 执行
  bs-webctl server                        前台启动 TMWebDriver master（调试用）
  bs-webctl install-extension             解压 Chrome 扩展到 ~/.bs-webctl/extension/

安装依赖:  pip install bs-webctl
输出格式:  每行 JSON（status + data），供其他 Agent 解析
"""
import sys, os, json, argparse, traceback

# 抑制库内部的 print 调试输出，不污染 stdout
_real_stdout = sys.stdout
sys.stdout = sys.stderr

from bs_webctl.driver import TMWebDriver
from bs_webctl import simphtml

sys.stdout = _real_stdout

_driver = None

def driver():
    global _driver
    if _driver is None:
        _driver = TMWebDriver()
    return _driver

def fmt_error(e):
    et, ev, tb = sys.exc_info()
    frames = traceback.extract_tb(tb)
    if frames:
        f = frames[-1]
        return f"{et.__name__}: {ev} @ {os.path.basename(f.filename)}:{f.lineno}"
    return f"{et.__name__}: {ev}"

def json_out(obj):
    print(json.dumps(obj, ensure_ascii=False, default=str))

# ── subcommands ──────────────────────────────────────────────

def cmd_sessions(args):
    d = driver()
    sess = d.get_all_sessions()
    json_out({"status": "success", "tabs": sess, "active": d.default_session_id})

def cmd_scan(args):
    d = driver()
    sess = d.get_all_sessions()
    if not sess:
        json_out({"status": "error", "msg": "no browser tabs connected"})
        return
    if args.tab_id:
        d.default_session_id = args.tab_id
    if args.tabs_only:
        tabs = [{"id": s["id"], "url": s.get("url", ""), "title": s.get("title", "")}
                for s in d.get_all_sessions() if not s.get("url", "").startswith("chrome-native://")]
        json_out({"status": "success", "tabs": tabs, "active": d.default_session_id})
        return
    try:
        content = simphtml.get_html(d, cutlist=True, maxchars=args.maxlen,
                                    text_only=args.text_only)
        if args.text_only:
            content = content[:args.maxlen // 3]
        json_out({"status": "success", "content": content, "active": d.default_session_id})
    except Exception as e:
        json_out({"status": "error", "msg": fmt_error(e)})

def cmd_exec(args):
    d = driver()
    if not d.get_all_sessions():
        json_out({"status": "error", "msg": "no browser tabs connected"})
        return
    if args.tab_id:
        d.default_session_id = args.tab_id
    script = args.script
    if args.script_file and not script:
        with open(args.script_file, encoding="utf-8") as f:
            script = f.read()
    if not script:
        json_out({"status": "error", "msg": "no script provided"})
        return
    try:
        r = simphtml.execute_js_rich(script, d, no_monitor=args.no_monitor)
        if args.save_to and "js_return" in r:
            with open(args.save_to, "w", encoding="utf-8") as f:
                f.write(str(r["js_return"] or ""))
            r["js_return"] = f"[saved to {args.save_to}]"
        json_out(r)
    except Exception as e:
        json_out({"status": "error", "msg": fmt_error(e)})

def cmd_install_extension(args):
    import pathlib, zipfile
    zip_path = pathlib.Path(__file__).parent / "extension" / "tmwd_cdp_bridge.zip"
    dest = pathlib.Path.home() / ".bs-webctl" / "extension"
    if dest.exists() and any(dest.iterdir()):
        sys.stderr.write(f"[WARN] {dest} already exists and is non-empty\n")
        if not args.force:
            json_out({"status": "error", "msg": f"{dest} already exists. Use --force to overwrite."})
            return
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)
    json_out({"status": "success", "extension_path": str(dest),
              "instructions": "Open chrome://extensions → Enable Developer mode → Load unpacked → select the path above"})

def cmd_server(args):
    sys.stderr.write("TMWebDriver master on ws://127.0.0.1:18765 (http :18766)\n")
    sys.stderr.write("Install Chrome extension: assets/tmwd_cdp_bridge/\n")
    sys.stderr.write("Open any normal URL, then `python webctl.py sessions` from another terminal.\n")
    TMWebDriver()
    import time
    while True:
        time.sleep(60)

# ── main ─────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(prog="bs-webctl",
                                description="Standalone browser-control CLI for AI agents")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("sessions", help="list connected tabs")

    s = sub.add_parser("scan", help="get simplified page HTML")
    s.add_argument("--text-only", action="store_true")
    s.add_argument("--tabs-only", action="store_true")
    s.add_argument("--tab-id", help="switch to this tab first")
    s.add_argument("--maxlen", type=int, default=35000)

    e = sub.add_parser("exec", help="execute JS in browser, return result + DOM diff")
    e.add_argument("script", nargs="?", help="inline JS (or omit and use --script-file)")
    e.add_argument("--script-file", help="read JS from file")
    e.add_argument("--tab-id")
    e.add_argument("--no-monitor", action="store_true", help="skip DOM diff monitoring")
    e.add_argument("--save-to", help="save js_return to file")

    e2 = sub.add_parser("exec-file", help="execute JS from file (shortcut)")
    e2.add_argument("path", help="path to JS file")
    e2.add_argument("--tab-id")
    e2.add_argument("--no-monitor", action="store_true")
    e2.add_argument("--save-to")

    sub.add_parser("install-extension", help="extract Chrome extension to ~/.bs-webctl/extension/").add_argument("--force", action="store_true", help="overwrite if exists")

    sub.add_parser("server", help="start TMWebDriver master in foreground")

    args = p.parse_args()
    if args.cmd == "sessions":
        cmd_sessions(args)
    elif args.cmd == "scan":
        cmd_scan(args)
    elif args.cmd == "exec":
        cmd_exec(args)
    elif args.cmd == "exec-file":
        args.script, args.script_file = None, args.path
        cmd_exec(args)
    elif args.cmd == "install-extension":
        cmd_install_extension(args)
    elif args.cmd == "server":
        cmd_server(args)

if __name__ == "__main__":
    main()
