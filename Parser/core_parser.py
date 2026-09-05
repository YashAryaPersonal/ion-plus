from nodes import *
from Lexer.tokens import *


class Parser():
    def __init__(self):
        self.pointer: int = 0
        self.symbol_table