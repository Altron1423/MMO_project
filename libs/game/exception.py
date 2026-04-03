from typing import final

@final
class GameStartException(Exception):
    """Возникает при ошибке загрузки игры"""

@final
class BarReadSrtException(Exception):
    """Возникает при ошибке преобразования строки в ProgressBar"""

