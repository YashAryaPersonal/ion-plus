from compiler.Parser.nodes import * 
from compiler.Lexer.tokens import *
from compiler.Errors.err import *
from compiler.Parser.core_parser import *


class Parser(CoreParser):
    def pratt_power_up(self):
        # gravities
        pratt_gravity = {
            "prenthesis": 100,
            "exponents": 80,
            "multiplication_or_division": 40,
            "addition_or_substraction": 20
        }
        # suffix list
        supposed_suffix = [
            Tokens.STRING_LITERAL, 
            Tokens.BINARY_LITERAL, 
            Tokens.CHARACTER_LITERAL, 
            Tokens.FLOAT_LITERAL, 
            Tokens.INTEGER_LITERAL,
            Tokens.HEXADECIMAL_LITERAL,
            Tokens.IDENTIFIER, # identifier
            Tokens.OP_SUBTRACTION,
            Tokens.PUNC_LEFT_BRACKET, # [
            Tokens.PUNC_RIGHT_BRACKET, # {
            Tokens.PUNC_LEFT_PARENTHESIS # (
        ]
        # infix list
        supposed_infix = [
            Tokens.OP_SUBTRACTION,
            Tokens.OP_ADDITION,
            Tokens.OP_DIVISION,
            Tokens.OP_MULTIPLICATION,
            Tokens.OP_MODULO,
            Tokens.OP_GREATER_THAN_EQ,
            Tokens.OP_GREATER_THAN,
            Tokens.OP_LESS_THAN_EQ,
            Tokens.OP_LESS_THAN,
            Tokens.OP_EQUAL_TO,
            Tokens.PUNC_DOT
        ]
        current_gravity: int = 0
        output_ast: ASTNode = ASTNode(self.peek().line, self.peek().col)
        
        while not self.match(Tokens.NEWLINE):
            if self.match(*supposed_suffix):
                pass
            else:
                self.consume()
                self.error("Unexpected Token Found, An Expression must contain suffix `-`, `(`, `{`, `[`, identifier or literal")
        
        return output_ast
    
    def parse_declaration_func_or_val(self):
        if self.peek().token == Tokens.SOF or self.peek().token == Tokens.NEWLINE:
            if self.peek(2).token == Tokens.OP_ASSIGNMENT:
                return self.parse_vardec()
            elif self.peek(2).token == Tokens.PUNC_LEFT_PARENTHESIS:
                pass
                    
        else: self.error("Unexpected syntax found")
        
    def parse_vardec(self, modifier=False):
        modifiers: list[Modifier] = []
        if modifier:
            
            while self.match(
                Tokens.VM_ALLOC,
                Tokens.VM_ATOMIC, 
                Tokens.VM_CONST, 
                Tokens.VM_UNSIGNED, 
                Tokens.VM_VOLATILE
            ):
                modifiers.append(self.parse_modifier(self.consume()))
                
        if self.parse_type(self.peek(), checkout=True) != False:
            
            var_line, var_col = self.peek().line, self.peek().col
            var_type = self.parse_type(self.consume())
            var_name = Identifier(self.peek().line, self.peek().col, self.consume().lexeme)
            self.expect(Tokens.OP_ASSIGNMENT)
            var_value = self.pratt_power_up()
            
            return VariableDeclaration(
                var_line,
                var_col,
                var_type,
                var_name,
                var_value,
                modifiers
            )
        else: self.error("Unexpected Variable")
            
    # Parser Func
    def parse(self):
        # setup
        return_tree: Program = Program(name=self.filename)
        
        # loop
        while self.peek().token != Tokens.EOF:
            # check
            if self.match(
                Tokens.DT_BOOL, 
                Tokens.DT_BYTE, 
                Tokens.DT_CHAR, 
                Tokens.DT_FLOAT, 
                Tokens.DT_INT, 
                Tokens.DT_NONE, 
                Tokens.DT_PTR
            ):
                return_tree.appendBody(self.parse_declaration_func_or_val())
            if self.match(
                Tokens.VM_ALLOC, 
                Tokens.VM_ATOMIC, 
                Tokens.VM_CONST, 
                Tokens.VM_UNSIGNED, 
                Tokens.VM_VOLATILE
            ):
                return_tree.appendBody(self.parse_vardec(modifier=True))
            
            # catch all (untouch)
            elif self.match(Tokens.NEWLINE, Tokens.SOF): 
                if self.consume().token == Tokens.NEWLINE:
                    print("Newline Found..")
                else:
                    print("Parsing Started...")
            else:
                self.error("Unexpected token found, yo")
                
        
        # return
        return return_tree