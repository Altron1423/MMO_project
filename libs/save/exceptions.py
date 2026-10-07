from typing import final

@final
class BlockNotInDimensionException(Exception):
    """Возникает при попытке загрузить в Dimension не подходящий MapBlock"""

