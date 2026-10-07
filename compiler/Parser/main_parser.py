from compiler.Parser.nodes import * 
from compiler.Lexer.tokens import *
from compiler.Errors.err import *
from compiler.Parser.core_parser import *


class Parser(SecondaryMethodsParser):
    def parse_declaration_func_or_val(self):
        if self.peek(-1).token == Tokens.SOF or self.peek(-1).token == Tokens.NEWLINE:
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
            var_value = self.parse_literal(self.peek(), self.consume().lexeme)
            
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
            elif self.match(Tokens.SOF, Tokens.NEWLINE, use_consume=True): pass
            else: self.error("Unexpected token found")
                
        
        # return
        return return_tree