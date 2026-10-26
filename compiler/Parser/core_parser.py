from compiler.Parser.nodes import * 
from compiler.Lexer.tokens import *
from compiler.Errors.err import *


class CoreParser():
    def __init__(self, tokens: list[Token], filename: str):
        self.filename = filename
        self.tokens = tokens
        self.pointer: int = 0
        self.symbol_table: list[str] = field(default_factory=str)
        
        self.errFound = False
        
    def peek(self, dis: int = 0):
        return self.tokens[self.pointer + dis]
    
    def consume(self):
        return_val = self.peek()
        self.pointer += 1
        return return_val
    
    def match(self, *tokentypes):
        if self.peek().token in tokentypes:
            return True
        else:
            return False
    
    def error(self, msg):
        self.errFound = True
        appearErr(SyntaxError(msg, self.peek().line, self.peek().col, self.filename))
        
    def expect(self, tok: TokenType):
        if self.peek().token == tok:
            return self.consume()
        else:
            self.error("Unexpected token found")

    def parse_type(self, dt_tk: Token, checkout=False):
        line = self.peek().line
        col = self.peek().col
        
        match dt_tk.token:
            case TokenType.DT_BOOL: return Bool(line, col)
            case TokenType.DT_BYTE: return Byte(line, col)
            case TokenType.DT_CHAR: return Char(line, col)
            case TokenType.DT_FLOAT: return Float(line, col)
            case TokenType.DT_INT: return Int(line, col)
            case TokenType.DT_NONE: return NoneType(line, col)
            case TokenType.DT_PTR: return Ptr(line, col)
            case _: return False if checkout else self.error("Unexpected Type Found")

    def parse_literal(self, dt_tk: Token, value, checkout=False):
        line = self.peek().line
        col = self.peek().col
        
        match dt_tk.token:
            case TokenType.INTEGER_LITERAL: return True if checkout else IntegerLiteral(line, col, value)
            case TokenType.FLOAT_LITERAL: return True if checkout else FloatLiteral(line, col, value)
            case TokenType.BINARY_LITERAL: return True if checkout else BinaryLiteral(line, col, value)
            case TokenType.STRING_LITERAL: return True if checkout else StringLiteral(line, col, value)
            case TokenType.CHARACTER_LITERAL: return True if checkout else CharLiteral(line, col, value)
            case TokenType.HEXADECIMAL_LITERAL: return True if checkout else HexadecimalLiteral(line, col, value)
            case _: return False if checkout else self.error("Unexpected Literal Found")

    def parse_operators(self, dt_tk: Token, checkout=False):
        line = self.peek().line
        col = self.peek().col
        
        match dt_tk.token:
            case TokenType.OP_ADDITION: return Addition(line, col)
            case TokenType.OP_SUBTRACTION: return Substraction(line, col)
            case TokenType.OP_MULTIPLICATION: return Multiplication(line, col)
            case TokenType.OP_DIVISION: return Division(line, col)
            case TokenType.OP_EQUAL_TO: return EqualTo(line, col)
            case TokenType.OP_LESS_THAN: return LessThan(line, col)
            case TokenType.OP_LESS_THAN_EQ: return LessThanEq(line, col)
            case TokenType.OP_GREATER_THAN: return GreaterThan(line, col)
            case TokenType.OP_GREATER_THAN_EQ: return GreaterThanEq(line, col)
            case TokenType.KW_BITWISE_AND: return BitAnd(line, col)
            case TokenType.KW_BITWISE_OR: return BitOr(line, col)
            case TokenType.KW_BITWISE_XOR: return BitXor(line, col)
            case TokenType.KW_BITWISE_NAND: return BitNand(line, col)
            case TokenType.KW_BITWISE_SHIFT_LEFT: return ShiftLeft(line, col)
            case TokenType.KW_BITWISE_SHIFT_RIGHT: return ShiftRight(line, col)
            case TokenType.OP_INCREMENT: return IncrementalAssignment(line, col)
            case TokenType.OP_DECREMENT: return DecrementalAssignment(line, col)
            case TokenType.OP_ADDITION_ASSIGNMENT: return AdditionalAssignment(line, col)
            case TokenType.OP_SUBTRACTIONAL_ASSIGNMENT: return SubtractionalAssignment(line, col)
            case TokenType.OP_MULTIPLICATIONAL_ASSIGNMENT: return MultiplicationalAssignment(line, col)
            case TokenType.OP_DIVISIONAL_ASSIGNMENT: return DivisionalAssignment(line, col)
            case _: return False if checkout else self.error("Unexpected Operator Found")

    def parse_modifier(self, checkout=False):
        line = self.peek().line
        col = self.peek().col
        
        match self.peek().token:
            case TokenType.VM_ALLOC: return Alloc(line, col)
            case TokenType.VM_ATOMIC: return Atomic(line, col)
            case TokenType.VM_CONST: return Const(line, col)
            case TokenType.VM_UNSIGNED: return Unsigned(line, col)
            case TokenType.VM_VOLATILE: return Volatile(line, col)
            case _: return False if checkout else self.error("Unexpected Modifier Found")
            
    def get_gravity(self, token: Token) -> int:
        match token.token:
            case TokenType.OP_ASSIGNMENT | TokenType.OP_ADDITION_ASSIGNMENT | TokenType.OP_SUBTRACTIONAL_ASSIGNMENT | TokenType.OP_MULTIPLICATIONAL_ASSIGNMENT | TokenType.OP_DIVISIONAL_ASSIGNMENT:
                return 10
            case TokenType.KW_OR:
                return 20
            case TokenType.KW_AND:
                return 30
            case TokenType.KW_BITWISE_OR | TokenType.KW_BITWISE_XOR | TokenType.KW_BITWISE_AND | TokenType.KW_BITWISE_NAND:
                return 40
            case TokenType.OP_EQUAL_TO | TokenType.OP_LESS_THAN | TokenType.OP_LESS_THAN_EQ | TokenType.OP_GREATER_THAN | TokenType.OP_GREATER_THAN_EQ:
                return 50
            case TokenType.KW_BITWISE_SHIFT_LEFT | TokenType.KW_BITWISE_SHIFT_RIGHT:
                return 60
            case TokenType.OP_ADDITION | TokenType.OP_SUBTRACTION:
                return 70
            case TokenType.OP_MULTIPLICATION | TokenType.OP_DIVISION | TokenType.OP_MODULO:
                return 80
            case TokenType.PUNC_DOT | TokenType.PUNC_LEFT_BRACKET | TokenType.PUNC_LEFT_PARENTHESIS:
                return 90
            case _:
                return 0