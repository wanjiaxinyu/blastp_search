"""Stage 4:把 BLAST 可能出的错都定义成"自己的异常类型"。

为什么要这么做?
- 底层可能因为各种原因失败:没装 blastp、数据库不存在、序列非法、blast 进程报错……
  与其到处抛裸的 RuntimeError,不如定义清晰的类型,让上层能分门别类地处理。
- 所有异常都继承同一个父类 BlastError,这样最外层用一句 `except BlastError`
  就能接住一整个家族(不管是哪种具体错误)。
"""


class BlastError(Exception):
    """所有 BLAST 相关错误的父类。用 except BlastError 可一次性接住全部子类。"""


class BlastNotInstalledError(BlastError):
    """系统里没装 blastp(不在 PATH 中)。"""


class DatabaseNotFoundError(BlastError):
    """指定的 BLAST 数据库不存在。"""


class InvalidSequenceError(BlastError):
    """输入序列非法(为空,或含非法字符)。"""


class BlastRunError(BlastError):
    """blast 进程返回了错误。"""
