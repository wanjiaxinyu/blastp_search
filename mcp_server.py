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
        hits = run_blastp(sequence)          
        return format_hits(hits)
    except BlastError as exc:
        return "BLAST 出错:" + str(exc)


@mcp.resource("blast://database/info")
def database_info() -> str:
    """把当前 BLAST 数据库的信息暴露成一个可读资源(resource,不是可执行的 tool)。"""
    fasta = os.path.join(config.ROOT, "data", "uniprot_sprot.fasta")
    n = 0
    if os.path.exists(fasta):
        with open(fasta) as f:
            n = sum(1 for line in f if line.startswith(">"))
    return (
        "数据库名: demo_proteins\n"
        "路径: " + config.DB + "\n"
        "序列条数: " + str(n) + "\n"
        "类型: 蛋白(protein)\n"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
