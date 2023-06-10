from os import listdir
from pathlib import Path
from typing import Callable, List

HERE = Path(__file__).parent

patterns: List[Callable[[str], str]] = [
    __import__(file[:-3], globals(), locals(), [], 1).pattern_handler
    for file in listdir(HERE)
    if not file.startswith("_") and file.endswith(".py")
]
