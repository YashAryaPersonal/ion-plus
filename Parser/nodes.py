from dataclasses import dataclass, field

# --- Roots ---

@dataclass
class ASTNode: 
    line: int
    col: int

type Body = list[ASTNode]

@dataclass
class Program(ASTNode):
    name: str
    body: Body
    line: int = 0
    col: int = 0
    

# --- Types, Modifiers & Operators ---

@dataclass
class Type:
    is_custom: bool = False
    
type TypeInput = list[Type]
    
class Int(Type): pass
class Float(Type): pass
class Bool(Type): pass
class Byte(Type): pass
class Char(Type): pass
class Ptr(Type): pass
class NoneType(Type): pass

@dataclass
class Modifier:
    pass

class Atomic(Modifier): pass
class Alloc(Modifier): pass
class Volatile(Modifier): pass
class Unsigned(Modifier): pass
class Const(Modifier): pass

@dataclass
class Operator:
    pass

class EqualTo(Operator): pass
class LessThanEq(Operator): pass
class GreterThanEq(Operator): pass
class Addition(Operator): pass
class Multiplication(Operator): pass
class Division(Operator): pass
class LessThan(Operator): pass
class GreaterThan(Operator): pass
class Substraction(Operator): pass

@dataclass
class BitwiseOperator:
    pass

class BitAnd(BitwiseOperator): pass
class BitOr(BitwiseOperator): pass
class BitNand(BitwiseOperator): pass
class BitXor(BitwiseOperator): pass
class BitNor(BitwiseOperator): pass
class ShiftLeft(BitwiseOperator): pass
class ShiftRight(BitwiseOperator): pass

@dataclass
class AssignmentOperator:
    pass

class IncrementOperator(AssignmentOperator): pass
class DecrementOperator(AssignmentOperator): pass
class AdditionalOperator(AssignmentOperator): pass
class MultiplicationalOperator(AssignmentOperator): pass
class DivisionalOperator(AssignmentOperator): pass
class SubstractionalOperators(AssignmentOperator): pass


# --- Literals (Terminal Nodes) ---

@dataclass
class Identifier(ASTNode):
    value: str

@dataclass
class IntegerLiteral(ASTNode):
    value: int

@dataclass
class FloatLiteral(ASTNode):
    value: float

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class CharLiteral(ASTNode):
    value: str

@dataclass
class BooleanLiteral(ASTNode):
    value: bool


# --- Expressions ---

@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: BitwiseOperator
    right: ASTNode
    
@dataclass
class InfixExpression(ASTNode):
    left: ASTNode
    operator: Operator
    right: ASTNode

@dataclass
class UnaryExpression(ASTNode):
    operator: Operator
    right: ASTNode

@dataclass
class AssignmentExpression(ASTNode):
    assignee: ASTNode
    operator: AssignmentOperator
    value: ASTNode

@dataclass
class CallExpression(ASTNode):
    function: ASTNode
    arguments: list[ASTNode]

@dataclass
class MemberExpression(ASTNode):
    object: ASTNode
    property: ASTNode

@dataclass
class SizeOfExpression(ASTNode):
    argument: ASTNode 


# --- Statements & Declarations ---

@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode
    
@dataclass
class VariableDeclaration(ASTNode):
    type: TypeInput
    identifier: Identifier
    value: ASTNode | None = None
    modifiers: list[Modifier] = field(default_factory=list)
    
@dataclass
class Parameter(ASTNode):
    type: TypeInput
    identifier: Identifier

@dataclass
class FunctionDeclaration(ASTNode):
    return_type: TypeInput
    identifier: Identifier
    parameters: list[Parameter]
    body: Body
    
@dataclass
class StructDeclaration(ASTNode):
    identifier: Identifier
    properties: list[VariableDeclaration]

@dataclass
class EnumDeclaration(ASTNode):
    identifier: Identifier
    members: list[Identifier]


# --- Control Flow Statements ---

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    body: Body
    alternative: ASTNode | None = None 
    
@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Body
    
@dataclass
class ReturnStatement(ASTNode):
    return_value: ASTNode | None = None

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass

@dataclass
class PassStatement(ASTNode):
    pass


# --- Utility Statements ---

@dataclass
class EchoStatement(ASTNode):
    expression: ASTNode

@dataclass
class ImportStatement(ASTNode):
    module: Identifier
    items: list[Identifier] | None = None