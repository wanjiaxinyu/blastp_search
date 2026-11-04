# blastp_search

✅️使用方法
一、配好从你电脑到服务器的免密 SSH(否则 Codex 自动连时会卡在输密码)
Codex 是在后台把 ssh ... 当子进程启动的,没有交互终端给你输密码,SSH 要么读不到密码直接失败,要么卡住
⚠️现在这个 MCP 是 stdio 方式,它有个硬限制:stdio 的客户端和服务器必须在同一台机器上(客户端要把 server 当本地子进程启动,靠标准输入输出通信)。电脑Codex 没法直接把"另一台服务器上的 Python 文件"当本地子进程拉起来。通过SSH 隧道，让 Codex 还是以为在本地跑,实际通过 SSH 到服务器上执行。

"公私钥"-ssh-keygen -t ed25519

二、codex的Plugins中进行配置

✅️解释

