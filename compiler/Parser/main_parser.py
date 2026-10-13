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
            TokenType.STRING_LITERAL, 
            TokenType.BINARY_LITERAL, 
            TokenType.CHARACTER_LITERAL, 
            TokenType.FLOAT_LITERAL, 
            TokenType.INTEGER_LITERAL,
            TokenType.HEXADECIMAL_LITERAL,
            TokenType.IDENTIFIER, # identifier
            TokenType.OP_SUBTRACTION,
            TokenType.PUNC_LEFT_BRACKET, # [
            TokenType.PUNC_RIGHT_BRACKET, # {
            TokenType.PUNC_LEFT_PARENTHESIS # (
        ]
        # infix list
        supposed_infix = [
            TokenType.OP_SUBTRACTION,
            TokenType.OP_ADDITION,
            TokenType.OP_DIVISION,
            TokenType.OP_MULTIPLICATION,
            TokenType.OP_MODULO,
            TokenType.OP_GREATER_THAN_EQ,
            TokenType.OP_GREATER_THAN,
            TokenType.OP_LESS_THAN_EQ,
            TokenType.OP_LESS_THAN,
            TokenType.OP_EQUAL_TO,
            TokenType.PUNC_DOT
        ]
        current_gravity: int = 0
        output_ast: ASTNode = ASTNode(self.peek().line, self.peek().col)
        
        while not self.match(TokenType.NEWLINE):
            if self.match(*supposed_suffix):
                pass
            else:
                self.consume()
                self.error("Unexpected Token Found, An Expression must contain suffix `-`, `(`, `{`, `[`, identifier or literal")
        
        return output_ast
    
    def parse_declaration_func_or_val(self):
        if self.peek().token == TokenType.SOF or self.peek().token == TokenType.NEWLINE:
            if self.peek(2).token == TokenType.OP_ASSIGNMENT:
                return self.parse_vardec()
            elif self.peek(2).token == TokenType.PUNC_LEFT_PARENTHESIS:
                pass
                    
        else: self.error("Unexpected syntax found")
        
    def parse_vardec(self, modifier=False):
        modifiers: list[Modifier] = []
        if modifier:
            
            while self.match(
                TokenType.VM_ALLOC,
                TokenType.VM_ATOMIC, 
                TokenType.VM_CONST, 
                TokenType.VM_UNSIGNED, 
                TokenType.VM_VOLATILE
            ):
                modifiers.append(self.parse_modifier(self.consume()))
                
        if self.parse_type(self.peek(), checkout=True) != False:
            
            var_line, var_col = self.peek().line, self.peek().col
            var_type = self.parse_type(self.consume())
            var_name = Identifier(self.peek().line, self.peek().col, self.consume().lexeme)
            self.expect(TokenType.OP_ASSIGNMENT)
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
        while self.peek().token != TokenType.EOF:
            # check
            if self.match(
                TokenType.DT_BOOL, 
                TokenType.DT_BYTE, 
                TokenType.DT_CHAR, 
                TokenType.DT_FLOAT, 
                TokenType.DT_INT, 
                TokenType.DT_NONE, 
                TokenType.DT_PTR
            ):
                return_tree.appendBody(self.parse_declaration_func_or_val())
            if self.match(
                TokenType.VM_ALLOC, 
                TokenType.VM_ATOMIC, 
                TokenType.VM_CONST, 
                TokenType.VM_UNSIGNED, 
                TokenType.VM_VOLATILE
            ):
                return_tree.appendBody(self.parse_vardec(modifier=True))
            
            # catch all (untouch)
            elif self.match(TokenType.NEWLINE, TokenType.SOF): 
                if self.consume().token == TokenType.NEWLINE:
                    print("Newline Found..")
                else:
                    print("Parsing Started...")
            else:
                self.error("Unexpected token found, yo")
                
        
        # return
        return return_tree