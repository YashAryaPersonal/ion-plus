from compiler.Parser.nodes import * 
from compiler.Lexer.tokens import *
from compiler.Errors.err import *
from compiler.Parser.main_parser import *


class PrattParser(Parser):
    def __init__(self):
        self.gravity = {
            "prenthesis": 100,
            "exponents": 80,
            "multiplication_or_division": 40,
            "addition_or_substraction": 20
        }
        
    def pratt_power_up():
        # most help needed for pratt parser is in the main parser, so this class will inherit from it
        pass