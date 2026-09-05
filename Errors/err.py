import sys


class IonError(Exception):
    def __init__(self, msg: str, line: int, col: int, filename: str):
        self.msg = msg
        self.line = line
        self.col = col
        self.filename = filename
        
        
    def __str__(self):
        
        return f"[ION+] \033[91m{self.__class__.__name__}\033[0m in {self.filename} at Line {self.line}, Col {self.col}:\n    -> \033[91m{self.msg}\033[0m"
    

class LexerError(IonError): pass

class IndentationError(IonError): pass

# --- INDEPENDENT METHOD ---

def throw(e: IonError):
    print(e)
    sys.exit(1)
    
    
def appearErr(e: IonError):
    print(e)