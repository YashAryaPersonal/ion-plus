from compiler.Parser.nodes import * 
from compiler.Lexer.tokens import *
from compiler.Errors.err import *


class CoreParser():
    def __init__(self, tokens: list[Token], filename: str):
        self.filename = filename
        self.tokens = tokens
        self.pointer: int = 0
        self.symbol_table: list[str] = field(default_factory=str)
        
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
        throw(SyntaxError(msg, self.peek().line, self.peek().col, self.filename))
        
    def expect(self, tok: TokenType):
        if self.peek().token == tok:
            return self.consume()
        else:
            self.error("Unexpected token found")

    def parse_type(self, dt_tk: Token, checkout=False):
        if dt_tk.token == TokenType.DT_BOOL:
            return Bool(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.DT_BYTE:
            return Byte(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.DT_CHAR:
            return Char(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.DT_FLOAT:
            return Float(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.DT_INT:
            return Int(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.DT_NONE:
            return NoneType(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.DT_PTR:
            return Ptr(self.peek().line, self.peek().col)
        else: return False if checkout else self.error("Unexpected Type Found")
        
    def parse_literal(self, dt_tk: Token, value, checkout=False):
        if dt_tk.token == TokenType.INTEGER_LITERAL:
            return IntegerLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == TokenType.FLOAT_LITERAL:
            return FloatLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == TokenType.BINARY_LITERAL:
            return BinaryLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == TokenType.STRING_LITERAL:
            return StringLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == TokenType.CHARACTER_LITERAL:
            return CharLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == TokenType.HEXADECIMAL_LITERAL:
            return HexadecimalLiteral(self.peek().line, self.peek().col, value)
        else: return False if checkout else self.error("Unexpected Literal Found")
        
    def parse_modifier(self, dt_tk: Token, checkout=False):
        if dt_tk.token == TokenType.VM_ALLOC:
            return Alloc(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.VM_ATOMIC:
            return Atomic(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.VM_CONST:
            return Const(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.VM_UNSIGNED:
            return Unsigned(self.peek().line, self.peek().col)
        elif dt_tk.token == TokenType.VM_VOLATILE:
            return Volatile(self.peek().line, self.peek().col)
        else:
            return False if checkout else self.error("Unexpected Modifier Found")