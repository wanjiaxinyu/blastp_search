"""Stage 5 核心:调用 blastp、校验输入、解析成结构化结果。

相比 Stage 4,这里把结果从"一堆 dict"升级成 dataclass(字段清晰、好读好用),
其余(校验、抛自定义异常)保持一致。仍然只用标准库 + dataclass,不依赖 LLM,可单独测。
"""

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

import config
from errors import (
    BlastNotInstalledError,
    BlastRunError,
    DatabaseNotFoundError,
    InvalidSequenceError,
)

COLUMNS = ["sseqid", "pident", "length", "evalue", "bitscore", "stitle"]
VALID_AA = set("ACDEFGHIKLMNPQRSTVWYBXZ")


@dataclass
class Hit:
    """一条比对命中。用 dataclass 把字段写清楚。"""
    subject: str      # 命中序列 ID
    title: str        # 命中序列描述
    identity: float   # 一致性百分比
    length: int       # 比对长度
    evalue: float     # E-value(越小越可靠)
    bitscore: float   # bit score


def clean_sequence(sequence):
    """去掉 FASTA 头和所有空白(包括行内空格),返回纯序列(大写)。"""
    out = []
    for ln in sequence.strip().splitlines():
        if ln.strip().startswith(">"):
            continue
        out.append("".join(ln.split()))   # 去掉这一行的所有空白
    return "".join(out).upper()


def run_blastp(sequence, db=None, evalue=None, max_hits=None):
    """跑 blastp,返回 list[Hit]。出错时抛出 BlastError 的子类。"""
    db = db or config.DB
    evalue = evalue if evalue is not None else config.EVALUE
    max_hits = max_hits if max_hits is not None else config.MAX_HITS

    if shutil.which("blastp") is None:
        raise BlastNotInstalledError("没找到 blastp,请先安装 NCBI BLAST+")
    if not os.path.exists(db + ".pin"):
        raise DatabaseNotFoundError("找不到数据库:" + db)

    seq = clean_sequence(sequence)
    if not seq:
        raise InvalidSequenceError("序列为空")
    illegal = set(seq) - VALID_AA
    if illegal:
        raise InvalidSequenceError("序列含非法字符:" + "".join(sorted(illegal)))

    with tempfile.TemporaryDirectory() as tmp:
        qpath = os.path.join(tmp, "q.fasta")
        with open(qpath, "w") as f:
            f.write(">query\n" + seq + "\n")
        cmd = ["blastp", "-query", qpath, "-db", db, "-evalue", str(evalue),
               "-max_target_seqs", str(max_hits), "-outfmt", "6 " + " ".join(COLUMNS)]
        result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise BlastRunError("blastp 运行失败:" + result.stderr)

    hits = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", len(COLUMNS) - 1)
        d = dict(zip(COLUMNS, parts))
        hits.append(Hit(
            subject=d["sseqid"],
            title=d["stitle"],
            identity=float(d["pident"]),
            length=int(d["length"]),
            evalue=float(d["evalue"]),
            bitscore=float(d["bitscore"]),
        ))
    return hits


def format_hits(hits):
    """把 list[Hit] 整理成一段可读文字(给人或 LLM 看)。"""
    if not hits:
        return "没有找到显著命中(可以把 evalue 放宽再试)。"
    out = ["找到 " + str(len(hits)) + " 条命中:"]
    for h in hits:
        out.append("- " + h.subject
                   + " (一致性 " + str(round(h.identity, 1)) + "%, E-value " + str(h.evalue) + "): "
                   + h.title)
    return "\n".join(out)
