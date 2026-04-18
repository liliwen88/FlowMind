from typing import Any, Dict, List, Optional, Set, Tuple

from .ast_nodes import (
    ApprovalCall,
    BinaryExpr,
    FlowNode,
    IdentifierExpr,
    IfNode,
    InputBlock,
    LlmBlock,
    LiteralExpr,
    MemberExpr,
    OutputBlock,
    RouteNode,
    ToolCall,
    UnaryExpr,
)
from .diagnostics import Diagnostic, Span, make_diagnostic


def validate_flow(flow: FlowNode, source: str) -> List[Diagnostic]:
    lines = source.splitlines()
    diagnostics: List[Diagnostic] = []
    scalar_symbols: Set[str] = set()
    object_symbols: Dict[str, Set[str]] = {}
    symbol_definitions: Dict[str, Tuple[str, Span]] = {}  # symbol -> (kind, first_span)

    for block in flow.blocks:
        _validate_statement(
            block,
            lines=lines,
            diagnostics=diagnostics,
            scalar_symbols=scalar_symbols,
            object_symbols=object_symbols,
            symbol_definitions=symbol_definitions,
        )
    return diagnostics


def _validate_statement(
    node: Any,
    lines: List[str],
    diagnostics: List[Diagnostic],
    scalar_symbols: Set[str],
    object_symbols: Dict[str, Set[str]],
    symbol_definitions: Optional[Dict[str, Tuple[str, Span]]] = None,
) -> None:
    if symbol_definitions is None:
        symbol_definitions = {}

    if isinstance(node, InputBlock):
        seen_fields: Dict[str, Span] = {}
        for field in node.fields:
            # Check for duplicate fields within input block
            if field.name in seen_fields:
                diagnostics.append(
                    make_diagnostic(
                        code="E_VAL_DUP_INPUT_FIELD",
                        message="duplicate input field '{0}'".format(field.name),
                        severity="error",
                        span=field.span,
                        source_lines=lines,
                    )
                )
            else:
                seen_fields[field.name] = field.span
            scalar_symbols.add(field.name)
        return

    if isinstance(node, LlmBlock):
        # Check for duplicate llm block names
        if node.name in symbol_definitions:
            kind, first_span = symbol_definitions[node.name]
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_DUP_SYMBOL",
                    message="duplicate symbol '{0}' (already defined as {1})".format(node.name, kind),
                    severity="error",
                    span=node.span,
                    source_lines=lines,
                )
            )
        else:
            symbol_definitions[node.name] = ("llm block", node.span)

        prompt = node.properties.get("prompt")
        if not isinstance(prompt, str):
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_LLM_PROMPT",
                    message="llm block '{0}' must include string prompt".format(node.name),
                    severity="error",
                    span=node.span,
                    source_lines=lines,
                )
            )
        schema = node.properties.get("output_schema")
        if not isinstance(schema, list) or not schema:
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_LLM_SCHEMA",
                    message="llm block '{0}' must include output_schema fields".format(node.name),
                    severity="error",
                    span=node.span,
                    source_lines=lines,
                )
            )
        else:
            object_symbols[node.name] = set(field.name for field in schema)
        return

    if isinstance(node, IfNode):
        _validate_expression(
            node.condition,
            lines=lines,
            diagnostics=diagnostics,
            scalar_symbols=scalar_symbols,
            object_symbols=object_symbols,
        )
        for stmt in node.then_body:
            _validate_statement(
                stmt,
                lines=lines,
                diagnostics=diagnostics,
                scalar_symbols=scalar_symbols,
                object_symbols=object_symbols,
                symbol_definitions=symbol_definitions,
            )
        for stmt in node.else_body:
            _validate_statement(
                stmt,
                lines=lines,
                diagnostics=diagnostics,
                scalar_symbols=scalar_symbols,
                object_symbols=object_symbols,
                symbol_definitions=symbol_definitions,
            )
        return

    if isinstance(node, RouteNode):
        _validate_expression(
            node.target,
            lines=lines,
            diagnostics=diagnostics,
            scalar_symbols=scalar_symbols,
            object_symbols=object_symbols,
        )
        seen: Set[str] = set()
        for case in node.cases:
            if case.key in seen:
                diagnostics.append(
                    make_diagnostic(
                        code="E_VAL_ROUTE_DUP_KEY",
                        message="duplicate route key '{0}'".format(case.key),
                        severity="error",
                        span=case.span,
                        source_lines=lines,
                    )
                )
            seen.add(case.key)
            _validate_statement(
                case.action,
                lines=lines,
                diagnostics=diagnostics,
                scalar_symbols=scalar_symbols,
                object_symbols=object_symbols,
                symbol_definitions=symbol_definitions,
            )
        if node.default_action is not None:
            _validate_statement(
                node.default_action,
                lines=lines,
                diagnostics=diagnostics,
                scalar_symbols=scalar_symbols,
                object_symbols=object_symbols,
                symbol_definitions=symbol_definitions,
            )
        return

    if isinstance(node, ToolCall):
        if not node.name:
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_TOOL_NAME",
                    message="tool statement must include non-empty name",
                    severity="error",
                    span=node.span,
                    source_lines=lines,
                )
            )
        return

    if isinstance(node, ApprovalCall):
        if not node.name:
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_APPROVAL_NAME",
                    message="approval statement must include non-empty name",
                    severity="error",
                    span=node.span,
                    source_lines=lines,
                )
            )
        return

    if isinstance(node, OutputBlock):
        seen_fields: Dict[str, Span] = {}
        for field in node.fields:
            # Check for duplicate fields within output block
            if field.name in seen_fields:
                diagnostics.append(
                    make_diagnostic(
                        code="E_VAL_DUP_OUTPUT_FIELD",
                        message="duplicate output field '{0}'".format(field.name),
                        severity="error",
                        span=field.span,
                        source_lines=lines,
                    )
                )
            else:
                seen_fields[field.name] = field.span
            _validate_expression(
                field.value,
                lines=lines,
                diagnostics=diagnostics,
                scalar_symbols=scalar_symbols,
                object_symbols=object_symbols,
            )
        return


def _validate_expression(
    expr: Any,
    lines: List[str],
    diagnostics: List[Diagnostic],
    scalar_symbols: Set[str],
    object_symbols: Dict[str, Set[str]],
) -> None:
    if isinstance(expr, LiteralExpr):
        return
    if isinstance(expr, IdentifierExpr):
        if expr.name not in scalar_symbols and expr.name not in object_symbols:
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_UNDEFINED",
                    message="undefined identifier '{0}'".format(expr.name),
                    severity="error",
                    span=expr.span,
                    source_lines=lines,
                )
            )
        return
    if isinstance(expr, MemberExpr):
        root, chain = _flatten_member(expr)
        if root not in scalar_symbols and root not in object_symbols:
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_UNDEFINED",
                    message="undefined identifier '{0}'".format(root),
                    severity="error",
                    span=expr.span,
                    source_lines=lines,
                )
            )
            return
        if root in scalar_symbols and chain:
            diagnostics.append(
                make_diagnostic(
                    code="E_VAL_MEMBER",
                    message="identifier '{0}' is not an object".format(root),
                    severity="error",
                    span=expr.span,
                    source_lines=lines,
                )
            )
            return
        if root in object_symbols and chain:
            first_member = chain[0]
            if first_member not in object_symbols[root]:
                diagnostics.append(
                    make_diagnostic(
                        code="E_VAL_MEMBER",
                        message="unknown field '{0}.{1}'".format(root, first_member),
                        severity="error",
                        span=expr.span,
                        source_lines=lines,
                    )
                )
        return
    if isinstance(expr, UnaryExpr):
        _validate_expression(
            expr.operand,
            lines=lines,
            diagnostics=diagnostics,
            scalar_symbols=scalar_symbols,
            object_symbols=object_symbols,
        )
        return
    if isinstance(expr, BinaryExpr):
        _validate_expression(
            expr.left,
            lines=lines,
            diagnostics=diagnostics,
            scalar_symbols=scalar_symbols,
            object_symbols=object_symbols,
        )
        _validate_expression(
            expr.right,
            lines=lines,
            diagnostics=diagnostics,
            scalar_symbols=scalar_symbols,
            object_symbols=object_symbols,
        )
        return


def _flatten_member(expr: MemberExpr) -> Tuple[str, List[str]]:
    chain: List[str] = [expr.member]
    target = expr.obj
    while isinstance(target, MemberExpr):
        chain.append(target.member)
        target = target.obj
    if isinstance(target, IdentifierExpr):
        chain.reverse()
        return target.name, chain
    return "<unknown>", []

