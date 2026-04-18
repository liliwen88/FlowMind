import copy
from typing import Any, Dict, List, Optional

from .ast_nodes import (
    ApprovalCall,
    BinaryExpr,
    FlowNode,
    IdentifierExpr,
    IfNode,
    InputBlock,
    LiteralExpr,
    LlmBlock,
    MemberExpr,
    OutputBlock,
    RouteNode,
    ToolCall,
    UnaryExpr,
)


class RunnerError(Exception):
    pass


def run_flow(flow: FlowNode, inputs: Optional[Dict[str, Any]] = None, dry_run: bool = True) -> Dict[str, Any]:
    state: Dict[str, Any] = {}
    if inputs:
        state.update(inputs)
    trace: List[Dict[str, Any]] = []
    output: Dict[str, Any] = {}
    step = 0

    def next_step() -> int:
        nonlocal step
        step += 1
        return step

    def append_trace(kind: str, status: str, detail: Dict[str, Any]) -> None:
        item = {"step": next_step(), "kind": kind, "status": status}
        item.update(detail)
        trace.append(item)

    def eval_expr(expr: Any) -> Any:
        if isinstance(expr, LiteralExpr):
            return expr.value
        if isinstance(expr, IdentifierExpr):
            if expr.name not in state:
                raise RunnerError("undefined runtime identifier '{0}'".format(expr.name))
            return state[expr.name]
        if isinstance(expr, MemberExpr):
            root = eval_expr(expr.obj)
            if not isinstance(root, dict):
                raise RunnerError("member access expects object value")
            if expr.member not in root:
                raise RunnerError("unknown member '{0}'".format(expr.member))
            return root[expr.member]
        if isinstance(expr, UnaryExpr):
            if expr.operator == "not":
                return not bool(eval_expr(expr.operand))
            raise RunnerError("unsupported unary operator '{0}'".format(expr.operator))
        if isinstance(expr, BinaryExpr):
            left = eval_expr(expr.left)
            right = eval_expr(expr.right)
            op = expr.operator
            if op == "or":
                return bool(left) or bool(right)
            if op == "and":
                return bool(left) and bool(right)
            if op == "==":
                return left == right
            if op == "!=":
                return left != right
            if op == "<":
                return left < right
            if op == "<=":
                return left <= right
            if op == ">":
                return left > right
            if op == ">=":
                return left >= right
            if op == "in":
                return left in right
            if op == "not in":
                return left not in right
            raise RunnerError("unsupported binary operator '{0}'".format(op))
        raise RunnerError("unsupported expression node at runtime")

    def make_default_value(type_name: str) -> Any:
        mapping = {
            "string": "",
            "number": 0,
            "boolean": False,
            "object": {},
            "array": [],
        }
        return copy.deepcopy(mapping.get(type_name, None))

    def exec_statement(stmt: Any) -> None:
        if isinstance(stmt, InputBlock):
            missing: List[str] = []
            for field in stmt.fields:
                if field.name not in state:
                    missing.append(field.name)
            if missing:
                raise RunnerError("missing required inputs: {0}".format(", ".join(missing)))
            append_trace(
                "input",
                "ok",
                {"fields": [field.name for field in stmt.fields]},
            )
            return

        if isinstance(stmt, LlmBlock):
            schema = stmt.properties.get("output_schema", [])
            override_llm = state.get("__llm__", {})
            if isinstance(override_llm, dict) and stmt.name in override_llm:
                result_obj = copy.deepcopy(override_llm[stmt.name])
            else:
                result_obj = {}
                for field in schema:
                    result_obj[field.name] = make_default_value(field.type_name)
            state[stmt.name] = result_obj
            append_trace(
                "llm",
                "dry_run" if dry_run else "ok",
                {
                    "name": stmt.name,
                    "prompt": stmt.properties.get("prompt", ""),
                    "result": result_obj,
                },
            )
            return

        if isinstance(stmt, IfNode):
            condition = bool(eval_expr(stmt.condition))
            append_trace(
                "if",
                "ok",
                {"condition": condition},
            )
            body = stmt.then_body if condition else stmt.else_body
            for nested in body:
                exec_statement(nested)
            return

        if isinstance(stmt, RouteNode):
            route_value = eval_expr(stmt.target)
            selected = None
            action = None
            for case in stmt.cases:
                if route_value == case.key:
                    selected = case.key
                    action = case.action
                    break
            if action is None and stmt.default_action is not None:
                selected = "default"
                action = stmt.default_action
            append_trace(
                "route",
                "ok",
                {"target": route_value, "selected": selected},
            )
            if action is not None:
                exec_statement(action)
            return

        if isinstance(stmt, ToolCall):
            append_trace(
                "tool",
                "dry_run" if dry_run else "ok",
                {"name": stmt.name},
            )
            return

        if isinstance(stmt, ApprovalCall):
            append_trace(
                "approval",
                "dry_run" if dry_run else "ok",
                {"name": stmt.name},
            )
            return

        if isinstance(stmt, OutputBlock):
            for field in stmt.fields:
                output[field.name] = eval_expr(field.value)
            append_trace("output", "ok", {"fields": list(output.keys())})
            return

        raise RunnerError("unsupported statement node at runtime")

    for block in flow.blocks:
        exec_statement(block)

    return {
        "flow": flow.name,
        "dry_run": dry_run,
        "output": output,
        "state": state,
        "trace": trace,
    }

