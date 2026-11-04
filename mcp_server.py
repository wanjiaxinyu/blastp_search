"""MCP stage 2:工程化的 MCP server —— 复用 stage5 的成熟核心,并新增一个 resource。

相比 stage1,两处升级:
  1) 工具内部改用 stage5 那套成熟核心(blast_core:带校验、结构化结果;errors:分类异常),
     体现"同一套核心既能给 LangChain 用,也能挂到 MCP 上"——换协议不改核心。
  2) 新增一个 MCP **resource**:MCP 不只有 tool(可执行动作),还有 resource(可读数据)。
     这里把"当前数据库的信息"暴露成一个资源,客户端可以读取它。

注意:blast_core / errors / config 这三个文件是从 stage5 复制过来的(config 仅调整了路径深度),
其余原样——这就是"复用成熟核心"的直接体现。

跑 / 验证:
    python mcp_server.py          # 启动(stdio 等待连接)
    python test_client.py         # 连上来,列出工具+资源、各调用一次(不需要 LLM key)
"""

import os

from mcp.server.fastmcp import FastMCP

import config
from blast_core import format_hits, run_blastp
from errors import BlastError

mcp = FastMCP("blast")


@mcp.tool()
def blastp_search(sequence: str) -> str:
    """用 BLASTP 把一段蛋白序列与本地蛋白数据库比对,找出最相似的已知蛋白。
    输入一段蛋白序列,返回最相似的几条命中(含一致性和 E-value)。"""
    try:
        hits = run_blastp(sequence)          # 成熟核心:内部会校验、出错抛 BlastError
        return format_hits(hits)
    except BlastError as exc:
        return "BLAST 出错:" + str(exc)


@mcp.resource("blast://database/info")
def database_info() -> str:
    """把当前 BLAST 数据库的信息暴露成一个可读资源(resource,不是可执行的 tool)。"""
    fasta = os.path.join(config.ROOT, "data", "demo_proteins.fasta")
    n = 0
    if os.path.exists(fasta):
        with open(fasta) as f:
            n = sum(1 for line in f if line.startswith(">"))
    return (
        "数据库名: demo_proteins\n"
        "路径: " + config.DB + "\n"
        "序列条数: " + str(n) + "\n"
        "类型: 蛋白(protein)\n"
        "说明: 演示用合成序列,可用 blastp_search 工具进行比对。"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
