# MCP Stage 2 — 工程化 server(复用成熟核心 + resource)

两处升级:

1. 工具内部改用**主线 stage5 的成熟核心**(`blast_core.py` 带校验/结构化结果,`errors.py` 分类异常)——这三个文件是从 stage5 复制来的(`config.py` 仅改了路径深度),体现"同一套核心,换协议不改"。
2. 新增一个 **resource**:`blast://database/info`。MCP 不只有 tool(可执行动作),还有 resource(可读数据)。

- `mcp_server.py` —— `@mcp.tool()` 暴露 blastp_search;`@mcp.resource(...)` 暴露数据库信息。
- `test_client.py` —— 列出工具**和资源**,各调用/读取一次(不需要 LLM key)。

```bash
python test_client.py
```

**重点**:tool vs resource 的区别;以及"成熟核心可以直接挂到 MCP 上"。
