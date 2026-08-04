#!/usr/bin/env python3
"""Learntide 本地静态预览服务器。

用法:
    python serve.py                 # 默认 127.0.0.1:8000，服务当前目录
    python serve.py --port 8080
    python serve.py --host 0.0.0.0 --port 9000
    python serve.py --root ./dist   # 服务指定目录

注意: 仅用于本地预览，不用于生产。由你(伟超)本机启动，范柏唱不负责启动。
"""
import argparse
import http.server
import mimetypes
import os
import socketserver

# 补齐全常见静态资源的 MIME，避免部分 Python 版本把 .js/.json 当 text/plain
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("application/xml", ".xml")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("text/css", ".css")


def main():
    parser = argparse.ArgumentParser(description="Learntide 本地静态服务器")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8000, help="监听端口")
    parser.add_argument("--root", default=".", help="要服务的根目录")
    args = parser.parse_args()

    os.chdir(args.root)
    handler = http.server.SimpleHTTPRequestHandler
    # ThreadingTCPServer 支持并发请求；allow_reuse_address 避免端口占用报错
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((args.host, args.port), handler) as httpd:
        url = f"http://{args.host}:{args.port}/"
        print(f"Learntide 本地预览已就绪: {url}")
        print("在浏览器打开上面的地址。按 Ctrl+C 停止。")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止。")


if __name__ == "__main__":
    main()
