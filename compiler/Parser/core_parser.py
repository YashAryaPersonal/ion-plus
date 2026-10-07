from compiler.Parser.nodes import * 
from compiler.Lexer.tokens import *
from compiler.Errors.err import *


class CoreParser():
    def __init__(self, tokens: list[TokenStruct], filename: str):
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
    
    def match(self, *tokentypes, use_consume = False):
        if not use_consume:
            if self.peek().token in tokentypes:
                return True
            else:
                return False
        else:
            if self.consume().token in tokentypes:
                return True
            else:
                return False
    
    def error(self, msg):
        throw(SyntaxError(msg, self.peek().line, self.peek().col, self.filename))
        
    def expect(self, tok: Tokens):
        if self.peek().token == tok:
            return self.consume()
        else:
            self.error("Unexpected token found")


class SecondaryMethodsParser(CoreParser):
    # Assembler Functions
    def parse_type(self, dt_tk: TokenStruct, checkout=False):
        if dt_tk.token == Tokens.DT_BOOL:
            return Bool(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.DT_BYTE:
            return Byte(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.DT_CHAR:
            return Char(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.DT_FLOAT:
            return Float(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.DT_INT:
            return Int(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.DT_NONE:
            return NoneType(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.DT_PTR:
            return Ptr(self.peek().line, self.peek().col)
        else: return False if checkout else self.error("Unexpected Type Found")
        
    def parse_literal(self, dt_tk: TokenStruct, value, checkout=False):
        if dt_tk.token == Tokens.INTEGER_LITERAL:
            return IntegerLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == Tokens.FLOAT_LITERAL:
            return FloatLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == Tokens.BINARY_LITERAL:
            return BinaryLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == Tokens.STRING_LITERAL:
            return StringLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == Tokens.CHARACTER_LITERAL:
            return CharLiteral(self.peek().line, self.peek().col, value)
        elif dt_tk.token == Tokens.HEXADECIMAL_LITERAL:
            return HexadecimalLiteral(self.peek().line, self.peek().col, value)
        else: return False if checkout else self.error("Unexpected Literal Found")
        
    def parse_modifier(self, dt_tk: TokenStruct, checkout=False):
        if dt_tk.token == Tokens.VM_ALLOC:
            return Alloc(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.VM_ATOMIC:
            return Atomic(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.VM_CONST:
            return Const(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.VM_UNSIGNED:
            return Unsigned(self.peek().line, self.peek().col)
        elif dt_tk.token == Tokens.VM_VOLATILE:
            return Volatile(self.peek().line, self.peek().col)
        else:
            return False if checkout else self.error("Unexpected Modifier Found")