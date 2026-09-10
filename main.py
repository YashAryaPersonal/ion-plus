from Lexer.post_lexer import *
from Parser.core_parser import *


# <----- Main TEST ----->

if __name__ == "__main__":
    
    with open("test1.ionx", "r") as f:
        source_code: str = f.read()
    
    tokens, last_line, last_col = Scan(source_code, "test2.ionx")
    parser = Parser(tokens, "test2.ionx")
    
    print_tokens(tokens)
    print(parser.parse())