"""连接 stage2 的 MCP server:列出工具和资源,各调用/读取一次 —— 不需要 LLM key。

演示 MCP 的两类东西:
  - tool(可执行动作):blastp_search
  - resource(可读数据):blast://database/info

运行:
    python test_client.py
"""

import asyncio
import os
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SERVER = os.path.join(HERE, "mcp_server.py")
QUERY = os.path.join(REPO, "data", "query.fasta")


def text_of(result):
    """MCP 工具返回的是内容块列表,取出其中的文本。"""
    if isinstance(result, list):
        return "\n".join(b.get("text", "") for b in result if isinstance(b, dict))
    return str(result)


async def main():
    client = MultiServerMCPClient({
        "blast": {"command": sys.executable, "args": [SERVER], "transport": "stdio"}
    })

    # --- 工具 ---
    tools = await client.get_tools()
    print("工具:", [t.name for t in tools])
    blastp = next(t for t in tools if t.name == "blastp_search")
    result = await blastp.ainvoke({"sequence": open(QUERY).read()})
    print("\nblastp_search 结果:\n" + text_of(result))

    # --- 资源(用底层 session 读取)---
    async with client.session("blast") as session:
        listed = await session.list_resources()
        uris = [str(r.uri) for r in listed.resources]
        print("\n资源:", uris)
        got = await session.read_resource(uris[0])
        print("\n读取资源 " + uris[0] + ":\n" + got.contents[0].text)


if __name__ == "__main__":
    asyncio.run(main())
