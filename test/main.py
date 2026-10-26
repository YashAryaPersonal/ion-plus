from rich import print as rich_print
from compiler.Lexer.post_lexer import *
from compiler.Parser.main_parser import *


# <----- Main TEST ----->

if __name__ == "__main__":
    
    filename = "test/test1.ionx"
    
    with open(filename, "r") as f:
        source_code: str = f.read()
    
    tokens, last_line, last_col = Scan(source_code, filename)
    parser = Parser(tokens, filename)
    
    # print_tokens(tokens)
    rich_print(parser.parse())