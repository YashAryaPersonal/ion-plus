# Ion+ ( [`ion-plus`](https://github.com/YashAryaPersonal/ion-plus) )

Ion+ is a low-level programming language project built in Python, with an architecture designed to eventually support LLVM-based code generation. The project currently focuses on the frontend pipeline: lexing source code, tokenizing language constructs, detecting indentation, and defining a rich AST model for future parsing and execution. Its main focus is to make a easier version of **C++** with OOP.

This project is still in early development, and it is open to contributions from developers who want to help shape the language, improve the parser, expand the syntax, and build the backend.

### [https://github.com/YashAryaPersonal/ion-plus](https://github.com/YashAryaPersonal/ion-plus)

<div align="center">

## We need developers and contributors

Ion+ is still being built, and we would love help from the developer community.
If you are interested in compilers, parsers, AST design, language engineering, **LLVM**, or Python tooling, please contribute, raise issues, propose features, or help build the missing parts. To scale it up like **C++** we need help of all of you **respectful** developers.

</div>

---

## Overview

Ion+ aims to provide a low-level, systems-oriented language with a readable syntax inspired by modern programming language patterns. It is designed to be approachable for developers who want to experiment with language construction while still having low-level features such as memory operations, pointers, bitwise operations, structs, enums, and control flow.

The current repository focuses mainly on the frontend:

- Lexing source code into tokens
- Recognizing keywords, operators, literals, and punctuation
- Managing indentation
- Creating a structured AST representation
- Preparing the project for parsing and backend code generation

The project description in the repository indicates an intended pipeline:

Python frontend -> parser/AST -> backend -> LLVM

This makes Ion+ a compiler-language experiment in progress rather than a fully finished language runtime.

---

## Project Goals

Ion+ aims to support the following core ideas:

- Low-level programming model
- Strong syntax for memory-aware operations
- Type-aware declarations and expressions
- Structures, enums, and custom types
- Bitwise and arithmetic expressions
- Control flow for branching and loops
- A future LLVM backend for code generation and execution
- Hyper powerful and popular strong **OOP low-level language**

The language is intentionally ambitious and educational. It tries to combine syntax patterns from low-level languages with modern programming ergonomics.

---

## Current Status

The project is in the early stages of implementation. At the moment, the following work is present:

- Lexer written with Python regex scanning
- Token enumeration covering keywords and operator families
- Indentation handling for block-based syntax
- Error reporting utilities
- AST definitions for nodes, declarations, expressions, statements, and program structure
- Sample language examples in .ionx files

However, the project does not yet appear to have a complete parser implementation or a working LLVM backend. The parser file exists as a starting point but is not fully developed, and the repository is currently a strong foundation for future compiler work rather than a completed compilable language toolchain.

---

## Architecture and Flow

The intended architecture of the project is:

1. Source file input
2. Lexical analysis
3. Token stream creation
4. Indentation processing
5. Parsing into an AST
6. Semantic validation
7. LLVM IR or backend code generation
8. Final compiled or interpreted execution

This repository currently contains the first half of that pipeline.

### 1. Source Input

The user writes code in files such as:

- test.ionx
- test2.ionx

These are sample programs representing the current language syntax.

### 2. Lexing

The lexer reads the whole source file and converts it into meaningful tokens.

That includes:

- Keywords like if, while, return, struct, enum, sizeof, import
- Data types like int, float, bool, char, byte, ptr, none
- Operators like +, -, *, /, %, ==, <=, >=, +=, -=, etc.
- Literals like integers, floats, strings, booleans, and binary/hex values
- Identifiers and punctuation

This is handled in [Lexer/scanner.py](Lexer/scanner.py).

### 3. Token Definitions

The [Lexer/tokens.py](Lexer/tokens.py) file defines all valid token names in an Enum, making token handling explicit and organized.

Examples include:

- Token categories like COMMENT, NEWLINE, WHITESPACE, EOF, INDENT, DEDENT
- Data types: DT_INT, DT_FLOAT, DT_CHAR, DT_BOOL, DT_BYTE, DT_PTR, DT_NONE
- Keywords: KW_IF, KW_ELSE, KW_WHILE, KW_RETURN, KW_STRUCT, KW_ENUM, KW_IMPORT
- Operators: OP_ADDITION, OP_SUBTRACTION, OP_ASSIGNMENT, OP_EQUAL_TO, OP_LESS_THAN
- Literals: INTEGER_LITERAL, FLOAT_LITERAL, STRING_LITERAL, CHARACTER_LITERAL

This is critical because the parser depends on consistent token categories when it eventually reads the stream.

### 4. Indentation Management

The project is designed around indentation-sensitive block structures, similar to Python-like languages.

This logic lives in [Lexer/post_lexer.py](Lexer/post_lexer.py). It reads the tokens produced by the scanner and inserts INDENT and DEDENT tokens when block scopes open or close. This is important because the language expects blocks such as:

- if conditions
- while loops
- function bodies
- struct or enum definitions

The project includes explicit indentation validation to detect mismatched or invalid indentation.

### 5. AST Definition

The AST layer is defined in [Parser/nodes.py](Parser/nodes.py).

This file declares all the node types representing syntax in the language, including:

- Program root node
- Expression nodes
- Statement nodes
- Declarations and definitions
- Control flow nodes

Examples of AST node categories:

- Literals: Identifier, IntegerLiteral, FloatLiteral, StringLiteral, CharLiteral, BooleanLiteral
- Expressions: BinaryExpression, InfixExpression, UnaryExpression, AssignmentExpression, CallExpression, MemberExpression, SizeOfExpression
- Statements: ExpressionStatement, VariableDeclaration, FunctionDeclaration, StructDeclaration, EnumDeclaration
- Control flow: IfStatement, WhileStatement, ReturnStatement, BreakStatement, ContinueStatement, PassStatement
- Utility: EchoStatement, ImportStatement

This is the real blueprint for the compiler frontend. Once the parser grows, these AST classes will be instantiated from the token stream.

---

## Project Structure

### Root directory

- [main.py](main.py)  
  Main execution file. It calls the scanning pipeline on a target .ionx file and prints tokens.

- [README.md](README.md)  
  Project overview and documentation.

- [LICENSE](LICENSE)  
  License terms for the project.

- [test.ionx](test.ionx)  
  Larger sample language file showing many language constructs.

- [test2.ionx](test2.ionx)  
  Simpler test file focusing on a struct and validation logic.

### Lexer folder

- [Lexer/scanner.py](Lexer/scanner.py)  
  Regex-based lexer that recognizes the language syntax.

- [Lexer/tokens.py](Lexer/tokens.py)  
  Enum definitions for all tokens.

- [Lexer/post_lexer.py](Lexer/post_lexer.py)  
  Indentation and token cleanup stage.

### Parser folder

- [Parser/nodes.py](Parser/nodes.py)  
  Abstract syntax tree definitions.

- [Parser/core_parser.py](Parser/core_parser.py)  
  Parser logic entry point for future implementation.

### Errors folder

- [Errors/err.py](Errors/err.py)  
  Error definitions and reporting utilities.

---

## Sample Language Ideas in the Project

The example source files show that Ion+ is intended to support a low-level, expression-heavy syntax. The sample programs include:

- Struct declarations
- Enum declarations
- Variable declarations with modifiers
- Memory-related keywords such as alloc, addr, free, null
- Pointer syntax with ptr
- Control flow with if, elif, else, while, break, continue, return
- Bitwise operators including band, bor, bxor, bnand, bnot, bshl, bshr
- Built-in sizeof function
- Boolean logic with not, and, or
- Echo output statements

Here is a conceptually representative snippet from the examples:

```ionx
struct Buffer:
    int size
    ptr byte data

?int Buffer.validate(int max_size):
    if size <= 0 or size >= max_size:
        return none

    int index = 0
    while index < size:
        index += 1

    return index
```

This shows the language’s intended block structure and syntax style.

---

## Current Implementation Details

### Lexer behavior

The scanner uses regex rules arranged in phases:

1. Ignore whitespace, comments, and newlines
2. Match multi-character operators
3. Match keywords and data types
4. Match literals and identifiers
5. Match single-character operators and punctuation
6. Catch illegal tokens as a fallback

This is an important part of the compiler pipeline because the scanner has to be precise enough that the parser later sees valid token groups.

### Error handling

The error system is defined in [Errors/err.py](Errors/err.py). It provides custom errors such as:

- IonError
- LexerError
- IndentationError

The system prints a location-aware message with file name, line, and column so that errors are easier to debug during language development.

### Indentation processing

Indentation matters, and the lexer adds INDENT and DEDENT tokens based on the leading spaces before a line. This is useful for block-based syntax and is an important feature for creating Python-like control structures.

---

## How the Project Runs Today

The current project entry point is [main.py](main.py), which does the following:

```python
from Lexer.post_lexer import *

if __name__ == "__main__":
    tokens, last_line, last_col = Scan("test2.ionx")
    print_tokens(tokens)
```

This means the current project behavior is essentially:

- Open a file like test2.ionx
- Scan it with the lexer
- Convert it into tokens
- Print the tokens to the console

This is a useful frontend validation step, and it helps test whether the lexer recognizes syntax correctly before deeper parser and compiler work begins.

---

## What Is Missing

Ion+ is still missing several crucial compiler stages. Important future tasks include:

- Full parser implementation
- Proper AST construction from token streams
- Semantic analysis and symbol resolution
- Type checking
- Function call validation
- Runtime execution model
- LLVM backend integration
- Code generation from AST to LLVM IR
- Test suite for parser and compiler correctness
- Documentation for language syntax and semantics
- **OOP** (Object Orintation Programming) features

This is a major compiler project, and the current repo is a very good starting point for building those features.

---

## Roadmap

A realistic roadmap for this project would look something like this:

### Phase 1: Frontend completion

- Finish parser for declarations, expressions, control flow
- Validate AST correctness
- Produce robust tokenization for all language constructs

### Phase 2: Semantics

- Add symbol table and scoped variable resolution
- Implement type checking
- Validate function signatures and declarations

### Phase 3: Code generation

- Generate LLVM IR
- Map AST nodes to backend instructions
- Support calling conventions and stack management

### Phase 4: Runtime and tooling

- Add CLI compiler commands
- Support compilation and execution
- Provide debug output, syntax diagnostics, and project tooling

### Phase 5: Community growth

- Improve docs and examples
- Add contribution guidelines
- Expand language syntax and compiler test coverage

---

## Why This Project Matters

Ion+ is interesting because it combines the educational side of compiler construction with the practical challenge of building a language from the ground up. It is a valuable project for anyone learning about:

- Lexical analysis
- Tokenization
- Parsing
- Abstract syntax trees
- Compiler architecture
- Low-level language concepts
- LLVM toolchain integration

It is also a strong example of how a language project evolves from a simple lexer to a complete compiler system.

---

## How to Run It

From the project root, run:

```bash
python main.py
```

This currently reads the sample file defined in [main.py](main.py) and prints the tokens.

If you want to test a different source file, update the filename inside the script or extend the project with a command-line argument parser.

---

## Development Opportunities

There are many ways to contribute to Ion+:

- Improve and expand the lexer
- Build the parser
- Define more AST nodes
- Add semantic analysis
- Create tests for language files
- Improve error reporting
- Implement LLVM backend support
- Write better documentation and examples
- Refactor code for readability and structure

This project is a good fit for contributors who want to learn compiler internals while creating something meaningful from scratch.

---

## Call for Contributors

Ion+ is a promising project, but it needs community support to grow into a real language ecosystem.

We are currently looking for help from developers who are interested in:

- compiler design
- parser construction
- AST engineering
- Python language tools
- LLVM backend work
- code generation
- language specification design
- documentation and testing

If you are passionate about building a new language or learning compiler internals, this project is a great place to contribute.

<div align="center">

## Join the project and help build Ion+

Contributors are welcome. If you want to help, open an issue, submit a pull request, improve the parser, write tests, or help shape the language design.

Let’s build the future of Ion+ together.

</div>

---

## License

This project uses the repository license included in [LICENSE](LICENSE). Please review that file for usage and distribution terms. It is made under [Apache 2.0](http://www.apache.org/licenses/).

---

## Final Note

Ion+ is a strong concept and a promising compiler project with a clean foundation. It already includes the building blocks for a language frontend, and it is ready for developers who want to help push it from an early-stage lexer project into a real, complete language implementation.

If you want a serious compiler project with a growing architecture, Ion+ is a good place to contribute.

**Thanks** for all **respectful** developers to read and join.