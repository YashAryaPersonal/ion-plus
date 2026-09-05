from Lexer.post_lexer import *


# <----- Main TEST ----->

if __name__ == "__main__":
    
    tokens, last_line, last_col = Scan("test2.ionx")
    
    print_tokens(tokens)
    # print(last_line, last_col)