# MCP 

这是一个基于 Python 和 MCP（Model Context Protocol）构建的蛋白质序列检索工具。项目通过调用本地 NCBI BLASTP，将输入的蛋白质序列与本地蛋白质数据库进行比对，筛选出相似度较高的已知蛋白，并返回序列 ID、一致性、比对长度、E-value 和描述等结果。通过 stdio 方式与 Codex 等 MCP 客户端通信，使大模型能够直接调用本地 BLASTP 完成蛋白质序列分析。

✅️使用
一、需要使用ssh-keygen -t ed25519来先配置“公私钥”
stdio 方式,客户端和服务器必须在同一台机器上(客户端要把 server 当本地子进程启动,靠标准输入输出通信)。电脑上的 Codex 没法直接把"另一台服务器上的 Python 文件"当本地子进程拉起来。SSH 隧道，让 Codex 还是以为在本地跑,实际通过 SSH 到服务器上执行。
二、codex的plugins中配置

✅️解释
一、任何一个程序都带有标准输入，标准输出，标准错误三个通道。当大模型想要调用工具时，客户端会向你的程序的 stdin 写入一行 JSON 字符串（比如 {"method": "tools/call", "params": {...}}）。你的程序监听到 stdin 有数据，解析 JSON，执行本地代码（比如读文件）。你的程序把结果打包成 JSON，通过 console.log() 或 print() 输出到 stdout。客户端从 stdout 截获这个 JSON，返回给大模型。

二、结构

```
mcp_server.py
      │
      ├── config.py
      ├── errors.py
      └── blast_core.py
              │
              ├── 调用系统 blastp
              └── 读取本地 BLAST 数据库

config.py 集中管理 .env、数据库路径、E-value、最大命中数等配置
errors.py 定义统一的 BLAST 异常体系 
blast_core.py 核心业务层：清洗序列、校验、执行 blastp、解析结果
mcp_server.py MCP 服务入口，向外暴露工具和资源
```



