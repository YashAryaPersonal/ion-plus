from .tokens import Tokens, TokenStruct
import re
import sys
from Errors.err import *


# ----- Class -----

class IonTokenHandler():
    def __init__(self):
        self.current_line: int = 1
        self.current_col: int = 1
        
    def handle_token(self, scanner, lexeme: str, token: Tokens):
        return_value = TokenStruct(token, lexeme, self.current_line, self.current_col) 
        self.current_col += len(lexeme)
        
        if "\n" in lexeme:
            self.current_line += lexeme.count("\n")
            self.current_col = len(lexeme.split("\n")[-1])
        
        return return_value
    
    def handle_token_len(self, scanner, lexeme: str, token: Tokens):
        return_value = TokenStruct(token, len(lexeme), self.current_line, self.current_col) 
        self.current_col += len(lexeme)
            
        return return_value
    
    def handle_newline(self, scanner, lexeme):
        return_value = TokenStruct(Tokens.NEWLINE, len(lexeme), self.current_line, self.current_col)   
        self.current_line += len(lexeme)
        self.current_col = 1
        
        return return_value
    

# ------ Rule ------

handler = IonTokenHandler()

lexer = re.Scanner([
    
    # --- Phase 1: Ignore ---
    (r"\n+", lambda s,t: handler.handle_newline(s,t)),
    (r"#.*|/\*[\s\S]*?\*/", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.COMMENT)),
    (r"[ \t]+", lambda s,t: handler.handle_token_len(scanner=s, lexeme=t, token=Tokens.WHITESPACE)),
    
    # --- Phase 2: Multi-Char Ops ---
    (r"==", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_EQUAL_TO)),
    (r"<=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_LESS_THAN_EQ)),
    (r">=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_GREATER_THAN_EQ)),
    (r"\+=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_SUBSTRACTIONAL_ASSIGNMENT)),
    (r"-=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_SUBSTRACTIONAL_ASSIGNMENT)),
    (r"\*=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_MULTIPLICATIONAL_ASSIGNMENT)),
    (r"/=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_DIVISIONAL_ASSIGNMENT)),
    (r"\+\+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_INCREMENT)),
    (r"--", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_DECREMENT)),
    
    # --- Phase 3: Word Boundaries (Variable Modifiers) ---
    (r"\batomic\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.VM_ATOMIC)),
    (r"\balloc\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.VM_ALLOC)),
    (r"\bvolatile\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.VM_VOLATILE)),
    (r"\bunsigned\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.VM_UNSIGNED)),
    (r"\bconst\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.VM_CONST)),
    
    # --- Phase 3: Word Boundaries (Data Types) ---
    (r"\bint\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_INT)),
    (r"\bfloat\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_FLOAT)),
    (r"\bchar\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_CHAR)),
    (r"\bbool\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_BOOL)),
    (r"\bbyte\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_BYTE)),
    (r"\bptr\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_PTR)),
    (r"\bnone\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.DT_NONE)),
    
    # --- Phase 3: Word Boundaries (Core Keywords) ---
    (r"\baddr\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_ADDR)),
    (r"\bat\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_AT)),
    (r"\bfree\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_FREE)),
    (r"\bnull\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_NULL)),
    (r"\bstruct\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_STRUCT)),
    (r"\benum\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_ENUM)),
    (r"\btypedef\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_TYPEDEF)),
    (r"\bas\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_AS)),
    (r"\bif\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_IF)),
    (r"\belif\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_ELIF)),
    (r"\becho\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_ECHO)),
    (r"\belse\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_ELSE)),
    (r"\bwhile\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_WHILE)),
    (r"\bbreak\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BREAK)),
    (r"\bcontinue\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_CONTINUE)),
    (r"\breturn\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_RETURN)),
    (r"\bpass\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_PASS)),
    (r"\band\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_AND)),
    (r"\bor\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_OR)),
    (r"\bnot\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_NOT)),
    (r"\bTrue\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.LITERAL_BOOLEAN_TRUE)),
    (r"\bFalse\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.LITERAL_BOOLEAN_FALSE)),
    (r"\bband\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_AND)),
    (r"\bbor\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_OR)),
    (r"\bbxor\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_XOR)),
    (r"\bbnand\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_NAND)),
    (r"\bbnot\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_NOT)),
    (r"\bbshl\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_SHIFT_LEFT)),
    (r"\bbshr\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_BITWISE_SHIFT_RIGHT)),
    (r"\bimport\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_IMPORT)),
    (r"\bfrom\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_FROM)),
    (r"\bsizeof\b", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.KW_SIZEOF)),
    
    # --- Phase 4: Literals ---
    (r"\d+\.\d+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.FLOAT_LITERAL)),
    (r"\d+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.INTEGER_LITERAL)),
    (r"\".*?\"", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.STRING_LITERAL)),
    (r"'.'", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.BINARY_LITERAL)),
    (r"0b[01]+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.HEXADECIMAL_LITERAL)),
    (r"0x[0-9a-fA-F]+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.CHARACTER_LITERAL)),
    
    # --- Phase 5: Identifiers ---
    (r"[a-zA-Z_][a-zA-Z0-9_]*", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.IDENTIFIER)),
    
    # --- Phase 6: Single-Char Ops & Punctuation ---
    (r"\+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_ADDITION)),
    (r"-", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_SUBTRACTION)),
    (r"\*", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_MULTIPLICATION)),
    (r"/", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_DIVISION)),
    (r"%", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_MODULO)),
    (r"=", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_ASSIGNMENT)),
    (r"<", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_LESS_THAN)),
    (r">", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.OP_GREATER_THAN)),
    (r",", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_COMMA)),
    (r"\.", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_DOT)),
    (r":", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_COLON)),
    (r";", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_SEMICOLON)),
    (r"\?", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_NULLABLE)),
    (r"\|", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_PIPE)),
    (r"\(", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_LEFT_PARENTHESIS)),
    (r"\)", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_RIGHT_PARENTHESIS)),
    (r"\[", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_LEFT_BRACKET)),
    (r"\]", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_RIGHT_BRACKET)),
    (r"\{", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_LEFT_BRACE)),
    (r"\}", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.PUNC_RIGHT_BRACE)),

    # --- Phase 7: Catch All (Safety Net) ---
    (r"\S+", lambda s,t: handler.handle_token(scanner=s, lexeme=t, token=Tokens.ILLEGAL))
])
    
# ----- Independent Methods -----

def print_tokens(tokensList: list[TokenStruct]):
    if not tokensList == -1:
        for tokens in tokensList:
            print(tokens.token.value, end=", ")
            
            if isinstance(tokens.lexeme, str):
                print(f'"{tokens.lexeme}"', end=", ")
            else:
                print(tokens.lexeme, end=", ")
                
            print("line: ", end="")
            print(tokens.line, end=", ")
            print("col: ", end="")
            print(tokens.col)

