from typing import Any, Dict, List, Optional, Set, Tuple

from .ast_nodes import (
    ApprovalCall,
    BinaryExpr,
    FlowNode,
    IdentifierExpr,
    IfNode,
    InputBlock,
    InputField,
    LiteralExpr,
    LlmBlock,
    MemberExpr,
    OutputBlock,
    OutputField,
    RouteCase,
    RouteNode,
    SchemaField,
    ToolCall,
    UnaryExpr,
)
from .diagnostics import Span, make_diagnostic
from .lexer import Token


class ParseError(Exception):
    def __init__(self, diagnostic):
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


def _span_join(a: Span, b: Span) -> Span:
    return Span(a.start_line, a.start_col, b.end_line, b.end_col)


class Parser:
    def __init__(self, tokens: List[Token], source: str):
        self.tokens = tokens
        self.source = source
        self.lines = source.splitlines()
        self.index = 0

    def parse(self) -> FlowNode:
        flow = self._parse_flow()
        self._expect_kind("EOF", "expected end of file")
        return flow

    def _current(self) -> Token:
        return self.tokens[self.index]

    def _peek(self, offset: int = 1) -> Token:
        target = self.index + offset
        if target >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[target]

    def _advance(self) -> Token:
        token = self._current()
        self.index += 1
        return token

    def _match_keyword(self, value: str) -> Optional[Token]:
        token = self._current()
        if token.kind == "KEYWORD" and token.value == value:
            self._advance()
            return token
        return None

    def _match_symbol(self, value: str) -> Optional[Token]:
        token = self._current()
        if token.kind == "SYMBOL" and token.value == value:
            self._advance()
            return token
        return None

    def _expect_keyword(self, value: str, message: Optional[str] = None) -> Token:
        token = self._current()
        if token.kind == "KEYWORD" and token.value == value:
            return self._advance()
        raise self._error(
            token,
            message
            or "expected keyword '{0}', got '{1}'".format(value, token.value or token.kind),
        )

    def _expect_symbol(self, value: str, message: Optional[str] = None) -> Token:
        token = self._current()
        if token.kind == "SYMBOL" and token.value == value:
            return self._advance()
        raise self._error(
            token,
            message
            or "expected symbol '{0}', got '{1}'".format(value, token.value or token.kind),
        )

    def _expect_kind(self, kind: str, message: str) -> Token:
        token = self._current()
        if token.kind == kind:
            return self._advance()
        raise self._error(token, message)

    def _expect_ident(self, message: str = "expected identifier") -> Token:
        token = self._current()
        if token.kind == "IDENT":
            return self._advance()
        raise self._error(token, message)

    def _expect_string(self, message: str = "expected string literal") -> Token:
        token = self._current()
        if token.kind == "STRING":
            return self._advance()
        raise self._error(token, message)

    def _error(self, token: Token, message: str) -> ParseError:
        diagnostic = make_diagnostic(
            code="E_PARSE",
            message=message,
            severity="error",
            span=token.span,
            source_lines=self.lines,
        )
        return ParseError(diagnostic)

    def _parse_flow(self) -> FlowNode:
        start = self._expect_keyword("flow")
        name_token = self._expect_string("expected flow name string after 'flow'")
        self._expect_symbol("{")
        blocks = self._parse_block_statements(stop_symbols={"}"})
        end = self._expect_symbol("}")
        return FlowNode(
            span=_span_join(start.span, end.span),
            name=name_token.value,
            blocks=blocks,
        )

    def _parse_block_statements(self, stop_symbols: Set[str]) -> List[Any]:
        nodes: List[Any] = []
        while True:
            token = self._current()
            if token.kind == "EOF":
                break
            if token.kind == "SYMBOL" and token.value in stop_symbols:
                break
            nodes.append(self._parse_statement())
        return nodes

    def _parse_statement(self) -> Any:
        token = self._current()
        if token.kind != "KEYWORD":
            raise self._error(token, "expected statement keyword")
        if token.value == "input":
            return self._parse_input_block()
        if token.value == "llm":
            return self._parse_llm_block()
        if token.value == "if":
            return self._parse_if_node()
        if token.value == "route":
            return self._parse_route_node()
        if token.value == "tool":
            return self._parse_tool_call()
        if token.value == "approval":
            return self._parse_approval_call()
        if token.value == "output":
            return self._parse_output_block()
        raise self._error(token, "unsupported statement keyword '{0}'".format(token.value))

    def _parse_input_block(self) -> InputBlock:
        start = self._expect_keyword("input")
        self._expect_symbol("{")
        fields: List[InputField] = []
        while not self._match_symbol("}"):
            name = self._expect_ident("expected input field name")
            self._expect_symbol(":")
            type_token = self._expect_ident("expected input field type identifier")
            span = _span_join(name.span, type_token.span)
            fields.append(InputField(span=span, name=name.value, type_name=type_token.value))
        end_span = self.tokens[self.index - 1].span
        return InputBlock(span=_span_join(start.span, end_span), fields=fields)

    def _parse_llm_block(self) -> LlmBlock:
        start = self._expect_keyword("llm")
        name = self._expect_ident("expected llm block name")
        self._expect_symbol("{")
        properties: Dict[str, Any] = {}
        while not self._match_symbol("}"):
            key = self._expect_ident("expected llm property key")
            self._expect_symbol(":")
            if key.value == "output_schema":
                properties[key.value] = self._parse_schema_object()
            else:
                properties[key.value] = self._parse_simple_value()
        end_span = self.tokens[self.index - 1].span
        return LlmBlock(
            span=_span_join(start.span, end_span),
            name=name.value,
            properties=properties,
        )

    def _parse_schema_object(self) -> List[SchemaField]:
        self._expect_symbol("{", "expected '{' for output_schema")
        fields: List[SchemaField] = []
        while not self._match_symbol("}"):
            key = self._expect_ident("expected output_schema field name")
            self._expect_symbol(":")
            type_token = self._expect_ident("expected output_schema field type")
            span = _span_join(key.span, type_token.span)
            fields.append(SchemaField(span=span, name=key.value, type_name=type_token.value))
            self._match_symbol(",")
        return fields

    def _parse_if_node(self) -> IfNode:
        start = self._expect_keyword("if")
        condition = self._parse_expression(0)
        then_body = self._parse_braced_body()
        else_body: List[Any] = []
        end_span = then_body[-1].span if then_body else condition.span
        if self._match_keyword("else") is not None:
            else_body = self._parse_braced_body()
            if else_body:
                end_span = else_body[-1].span
        return IfNode(
            span=_span_join(start.span, end_span),
            condition=condition,
            then_body=then_body,
            else_body=else_body,
        )

    def _parse_route_node(self) -> RouteNode:
        start = self._expect_keyword("route")
        self._expect_keyword("on", "expected keyword 'on' after route")
        target = self._parse_expression(0)
        self._expect_symbol("{")
        cases: List[RouteCase] = []
        default_action = None
        seen_default = False
        while not self._match_symbol("}"):
            if self._match_keyword("default") is not None:
                arrow = self._expect_symbol("->", "expected '->' after default")
                if seen_default:
                    raise self._error(arrow, "duplicate route default branch")
                default_action = self._parse_route_action()
                seen_default = True
            else:
                key = self._expect_string("expected route branch key string")
                self._expect_symbol("->", "expected '->' after route key")
                action = self._parse_route_action()
                case_span = _span_join(key.span, action.span)
                cases.append(RouteCase(span=case_span, key=key.value, action=action))
        end_span = self.tokens[self.index - 1].span
        return RouteNode(
            span=_span_join(start.span, end_span),
            target=target,
            cases=cases,
            default_action=default_action,
        )

    def _parse_route_action(self) -> Any:
        token = self._current()
        if token.kind == "KEYWORD" and token.value == "tool":
            return self._parse_tool_call()
        if token.kind == "KEYWORD" and token.value == "approval":
            return self._parse_approval_call()
        raise self._error(token, "route action must be tool or approval statement")

    def _parse_tool_call(self) -> ToolCall:
        start = self._expect_keyword("tool")
        name = self._expect_string("expected tool name string")
        return ToolCall(span=_span_join(start.span, name.span), name=name.value)

    def _parse_approval_call(self) -> ApprovalCall:
        start = self._expect_keyword("approval")
        name = self._expect_string("expected approval name string")
        return ApprovalCall(span=_span_join(start.span, name.span), name=name.value)

    def _parse_output_block(self) -> OutputBlock:
        start = self._expect_keyword("output")
        self._expect_symbol("{")
        fields: List[OutputField] = []
        while not self._match_symbol("}"):
            key = self._expect_ident("expected output field name")
            self._expect_symbol(":")
            value_expr = self._parse_expression(0)
            fields.append(
                OutputField(
                    span=_span_join(key.span, value_expr.span),
                    name=key.value,
                    value=value_expr,
                )
            )
            self._match_symbol(",")
        end_span = self.tokens[self.index - 1].span
        return OutputBlock(span=_span_join(start.span, end_span), fields=fields)

    def _parse_braced_body(self) -> List[Any]:
        self._expect_symbol("{", "expected '{' to start block")
        body = self._parse_block_statements(stop_symbols={"}"})
        self._expect_symbol("}", "expected '}' to close block")
        return body

    def _parse_simple_value(self) -> Any:
        token = self._current()
        if token.kind == "STRING":
            return self._advance().value
        if token.kind == "NUMBER":
            value = self._advance().value
            return float(value) if "." in value else int(value)
        if token.kind == "KEYWORD" and token.value in {"true", "false"}:
            self._advance()
            return token.value == "true"
        raise self._error(token, "expected literal value")

    def _parse_expression(self, min_bp: int) -> Any:
        left = self._nud()
        while True:
            op, lbp, rbp, op_span = self._peek_infix_operator()
            if op is None or lbp < min_bp:
                break
            if op == ".":
                self._advance()
                member = self._expect_ident("expected property name after '.'")
                left = MemberExpr(
                    span=_span_join(left.span, member.span),
                    obj=left,
                    member=member.value,
                )
                continue
            if op == "not in":
                self._advance()
                self._advance()
            else:
                self._advance()
            right = self._parse_expression(rbp)
            left = BinaryExpr(
                span=_span_join(left.span, right.span),
                operator=op,
                left=left,
                right=right,
            )
        return left

    def _nud(self) -> Any:
        token = self._current()
        if token.kind == "SYMBOL" and token.value == "(":
            open_token = self._advance()
            expr = self._parse_expression(0)
            close_token = self._expect_symbol(")", "expected ')' to close grouped expression")
            expr.span = _span_join(open_token.span, close_token.span)
            return expr
        if token.kind == "KEYWORD" and token.value == "not":
            op = self._advance()
            operand = self._parse_expression(70)
            return UnaryExpr(
                span=_span_join(op.span, operand.span),
                operator="not",
                operand=operand,
            )
        if token.kind == "IDENT":
            ident = self._advance()
            return IdentifierExpr(span=ident.span, name=ident.value)
        if token.kind == "STRING":
            lit = self._advance()
            return LiteralExpr(span=lit.span, value=lit.value, literal_type="string")
        if token.kind == "NUMBER":
            lit = self._advance()
            value = float(lit.value) if "." in lit.value else int(lit.value)
            return LiteralExpr(span=lit.span, value=value, literal_type="number")
        if token.kind == "KEYWORD" and token.value in {"true", "false"}:
            lit = self._advance()
            value = lit.value == "true"
            return LiteralExpr(span=lit.span, value=value, literal_type="boolean")
        raise self._error(token, "unexpected token in expression")

    def _peek_infix_operator(self) -> Tuple[Optional[str], int, int, Span]:
        token = self._current()
        if token.kind == "SYMBOL" and token.value == ".":
            return ".", 90, 91, token.span
        if token.kind == "KEYWORD":
            if token.value == "or":
                return "or", 10, 11, token.span
            if token.value == "and":
                return "and", 20, 21, token.span
            if token.value == "in":
                return "in", 30, 31, token.span
            if token.value == "not" and self._peek().kind == "KEYWORD" and self._peek().value == "in":
                span = _span_join(token.span, self._peek().span)
                return "not in", 30, 31, span
        if token.kind == "SYMBOL" and token.value in {"==", "!=", "<", "<=", ">", ">="}:
            return token.value, 30, 31, token.span
        return None, -1, -1, token.span

