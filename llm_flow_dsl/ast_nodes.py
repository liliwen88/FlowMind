from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, List, Optional

from .diagnostics import Span


@dataclass
class Node:
    span: Span


@dataclass
class ExpressionNode(Node):
    pass


@dataclass
class IdentifierExpr(ExpressionNode):
    name: str


@dataclass
class LiteralExpr(ExpressionNode):
    value: Any
    literal_type: str


@dataclass
class MemberExpr(ExpressionNode):
    obj: ExpressionNode
    member: str


@dataclass
class UnaryExpr(ExpressionNode):
    operator: str
    operand: ExpressionNode


@dataclass
class BinaryExpr(ExpressionNode):
    operator: str
    left: ExpressionNode
    right: ExpressionNode


@dataclass
class InputField(Node):
    name: str
    type_name: str


@dataclass
class InputBlock(Node):
    fields: List[InputField]


@dataclass
class SchemaField(Node):
    name: str
    type_name: str


@dataclass
class LlmBlock(Node):
    name: str
    properties: Dict[str, Any]


@dataclass
class ToolCall(Node):
    name: str


@dataclass
class ApprovalCall(Node):
    name: str


@dataclass
class RouteCase(Node):
    key: str
    action: Node


@dataclass
class RouteNode(Node):
    target: ExpressionNode
    cases: List[RouteCase]
    default_action: Optional[Node]


@dataclass
class OutputField(Node):
    name: str
    value: ExpressionNode


@dataclass
class OutputBlock(Node):
    fields: List[OutputField]


@dataclass
class IfNode(Node):
    condition: ExpressionNode
    then_body: List[Node]
    else_body: List[Node]


@dataclass
class FlowNode(Node):
    name: str
    blocks: List[Node]


def node_to_dict(value: Any) -> Any:
    if isinstance(value, Span):
        return value.to_dict()
    if is_dataclass(value):
        data: Dict[str, Any] = {"node_type": value.__class__.__name__}
        for field in fields(value):
            data[field.name] = node_to_dict(getattr(value, field.name))
        return data
    if isinstance(value, list):
        return [node_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: node_to_dict(item) for key, item in value.items()}
    return value
