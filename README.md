# MCP 

✅️使用
一、需要使用ssh-keygen -t ed25519来先配置“公私钥”
stdio 方式,客户端和服务器必须在同一台机器上(客户端要把 server 当本地子进程启动,靠标准输入输出通信)。电脑上的 Codex 没法直接把"另一台服务器上的 Python 文件"当本地子进程拉起来。SSH 隧道，让 Codex 还是以为在本地跑,实际通过 SSH 到服务器上执行。
二、codex的plugins中配置

✅️解释
一、任何一个程序都带有标准输入，标准输出，标准错误三个通道。当大模型想要调用工具时，客户端会向你的程序的 stdin 写入一行 JSON 字符串（比如 {"method": "tools/call", "params": {...}}）。你的程序监听到 stdin 有数据，解析 JSON，执行本地代码（比如读文件）。你的程序把结果打包成 JSON，通过 console.log() 或 print() 输出到 stdout。客户端从 stdout 截获这个 JSON，返回给大模型。

