from compiler.Lexer.tokens import TokenType, Token
from compiler.Lexer.scanner import *
from compiler.Errors.err import *


def Indent_manager(tokens: list[Token], filename) -> list[Token]:
    final_tokens = [] 
    indent_level = [0]
    is_line_start = True
    current_indent_spaces = 0
    indent_line = 0
    indent_col = 0
    
    for tok in tokens:
        if tok.token == TokenType.NEWLINE:
            final_tokens.append(tok)
            is_line_start = True
            current_indent_spaces = 0
            indent_col = tok.col
            
        elif tok.token == TokenType.WHITESPACE and is_line_start:
            current_indent_spaces = int(tok.lexeme)
            indent_line = tok.line - 1
        
        elif tok.token == TokenType.COMMENT or tok.token == TokenType.WHITESPACE and not is_line_start:
            pass
        
        else:        
            if is_line_start:
                if current_indent_spaces > indent_level[-1]:
                    indent_level.append(current_indent_spaces)
                    final_tokens.append(Token(TokenType.INDENT, current_indent_spaces, indent_line, indent_col))
                    
                while current_indent_spaces < indent_level[-1]:
                    indent_level.pop()
                    final_tokens.append(Token(TokenType.DEDENT, indent_level[-1], indent_line, indent_col))
                    
                if not indent_level[-1] == current_indent_spaces:
                    throw(IndentationError("Unmatched Indentation Found", tok.line, tok.col, filename))
                    
                is_line_start = False
                
            final_tokens.append(tok)
            
    while len(indent_level) > 1:
        final_tokens.append(Token(TokenType.DEDENT, indent_level[-1], indent_line, indent_col))
        indent_level.pop()
        
    return final_tokens
            
            
        
        
def Scan(source_code: str, filename: str, unindented: bool = False): 
    if not source_code[-1] == "\n":
        source_code += "\n"
    
    if "\r\n" in source_code:
        source_code = source_code.replace("\r\n", "\n")
        
    output = lexer.scan(source_code)
    tokens: list[Token] = output[0]
    illegal_token = False
    
    for tok in tokens:
        if tok.token == TokenType.ILLEGAL:
            appearErr(LexerError(f"Unknown Character Found: {tok.lexeme}", tok.line, tok.col, filename))
            illegal_token = True
            
    if illegal_token:
        sys.exit(1)
        
    tokens.append(Token(TokenType.EOF, -1, handler.current_line, handler.current_col))
    indented_form = [Token(TokenType.SOF, -1, 1, 0)] + Indent_manager(tokens, filename)
            
    return_val = indented_form, handler.current_line, handler.current_col
    
    if unindented: return_val = [Token(TokenType.SOF, -1, 1, 0)] + tokens, handler.current_line, handler.current_col
    
    # reset
    handler.current_line = 0
    handler.current_col = 0
            
    return return_val