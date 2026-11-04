


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
