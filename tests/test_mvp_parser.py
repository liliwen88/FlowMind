import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from llm_flow_dsl.ast_nodes import BinaryExpr, FlowNode, UnaryExpr
from llm_flow_dsl.lexer import Lexer, LexerError
from llm_flow_dsl.parser import ParseError, Parser
from llm_flow_dsl.runner import run_flow
from llm_flow_dsl.validator import validate_flow


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_source(source: str) -> FlowNode:
    tokens = Lexer(source).tokenize()
    return Parser(tokens, source).parse()


class ParserSuccessTests(unittest.TestCase):
    def test_parse_support_triage_example(self) -> None:
        content = (REPO_ROOT / "examples" / "support-triage.flow").read_text(
            encoding="utf-8"
        )
        flow = parse_source(content)
        self.assertEqual(flow.name, "support_triage_v1")
        self.assertGreaterEqual(len(flow.blocks), 4)

    def test_expression_precedence(self) -> None:
        source = textwrap.dedent(
            """
            flow "p" {
              input {
                a: boolean
                b: boolean
                c: boolean
                d: boolean
              }
              if not a == b and c or d {
                tool "x"
              }
            }
            """
        ).strip()
        flow = parse_source(source)
        if_node = flow.blocks[1]
        self.assertIsInstance(if_node.condition, BinaryExpr)
        self.assertEqual(if_node.condition.operator, "or")
        left = if_node.condition.left
        self.assertIsInstance(left, BinaryExpr)
        self.assertEqual(left.operator, "and")
        self.assertIsInstance(left.left, BinaryExpr)
        self.assertEqual(left.left.operator, "==")
        self.assertIsInstance(left.left.left, UnaryExpr)
        self.assertEqual(left.left.left.operator, "not")


class ParserErrorTests(unittest.TestCase):
    def test_parse_error_missing_brace(self) -> None:
        source = 'flow "x" { input { a: string }'
        with self.assertRaises(ParseError) as ctx:
            parse_source(source)
        self.assertEqual(ctx.exception.diagnostic.code, "E_PARSE")
        self.assertGreaterEqual(ctx.exception.diagnostic.span.start_line, 1)

    def test_lexer_error_illegal_char(self) -> None:
        source = 'flow "x" { @ }'
        with self.assertRaises(LexerError) as ctx:
            Lexer(source).tokenize()
        self.assertEqual(ctx.exception.diagnostic.code, "E_LEX_CHAR")


class ValidationTests(unittest.TestCase):
    def test_validation_undefined_identifier(self) -> None:
        source = textwrap.dedent(
            """
            flow "x" {
              input {
                ticket_text: string
              }
              if customer_tier == "enterprise" {
                tool "ok"
              }
            }
            """
        ).strip()
        flow = parse_source(source)
        diagnostics = validate_flow(flow, source)
        self.assertTrue(any(d.code == "E_VAL_UNDEFINED" for d in diagnostics))

    def test_validation_duplicate_route_key(self) -> None:
        source = textwrap.dedent(
            """
            flow "x" {
              input {
                tag: string
              }
              route on tag {
                "billing" -> tool "a"
                "billing" -> tool "b"
              }
            }
            """
        ).strip()
        flow = parse_source(source)
        diagnostics = validate_flow(flow, source)
        self.assertTrue(any(d.code == "E_VAL_ROUTE_DUP_KEY" for d in diagnostics))


class CliTests(unittest.TestCase):
    def test_cli_parse_success(self) -> None:
        cmd = [
            sys.executable,
            "-m",
            "llm_flow_dsl",
            "parse",
            str(REPO_ROOT / "examples" / "support-triage.flow"),
            "--pretty",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["node_type"], "FlowNode")

    def test_cli_parse_validation_error(self) -> None:
        bad_flow = textwrap.dedent(
            """
            flow "x" {
              input {
                ticket_text: string
              }
              if missing_var == "foo" {
                tool "noop"
              }
            }
            """
        ).strip()
        with tempfile.NamedTemporaryFile("w", suffix=".flow", delete=False, encoding="utf-8") as f:
            f.write(bad_flow)
            path = f.name
        cmd = [sys.executable, "-m", "llm_flow_dsl", "parse", path]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stderr)
        self.assertTrue(isinstance(payload, list))
        self.assertEqual(payload[0]["code"], "E_VAL_UNDEFINED")

    def test_cli_no_validate(self) -> None:
        bad_flow = textwrap.dedent(
            """
            flow "x" {
              input {
                ticket_text: string
              }
              if missing_var == "foo" {
                tool "noop"
              }
            }
            """
        ).strip()
        with tempfile.NamedTemporaryFile("w", suffix=".flow", delete=False, encoding="utf-8") as f:
            f.write(bad_flow)
            path = f.name
        cmd = [sys.executable, "-m", "llm_flow_dsl", "parse", path, "--no-validate"]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["node_type"], "FlowNode")

    def test_cli_run_dry_run_success(self) -> None:
        inputs = {
            "ticket_text": "payment failed",
            "customer_tier": "enterprise",
            "region": "cn",
            "__llm__": {
                "classify_intent": {
                    "issue_type": "billing",
                    "urgency": "high",
                    "confidence": 0.93,
                }
            },
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(inputs, f)
            path = f.name
        cmd = [
            sys.executable,
            "-m",
            "llm_flow_dsl",
            "run",
            str(REPO_ROOT / "examples" / "support-triage.flow"),
            "--input-json",
            path,
            "--dry-run",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["flow"], "support_triage_v1")
        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["output"]["routed"], True)
        kinds = [item["kind"] for item in payload["trace"]]
        self.assertIn("route", kinds)
        self.assertIn("tool", kinds)

    def test_cli_run_missing_input(self) -> None:
        cmd = [
            sys.executable,
            "-m",
            "llm_flow_dsl",
            "run",
            str(REPO_ROOT / "examples" / "support-triage.flow"),
            "--dry-run",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stderr)
        self.assertEqual(payload["code"], "E_RUNTIME")

    def test_cli_run_input_json_with_bom(self) -> None:
        data = '{"ticket_text":"x","customer_tier":"free","region":"cn"}'
        with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
            f.write(b"\xef\xbb\xbf")
            f.write(data.encode("utf-8"))
            path = f.name
        cmd = [
            sys.executable,
            "-m",
            "llm_flow_dsl",
            "run",
            str(REPO_ROOT / "examples" / "support-triage.flow"),
            "--input-json",
            path,
            "--dry-run",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)


class RunnerTests(unittest.TestCase):
    def test_run_flow_route_default(self) -> None:
        source = textwrap.dedent(
            """
            flow "x" {
              input {
                kind: string
              }
              route on kind {
                "billing" -> tool "queue_billing"
                default -> tool "queue_general"
              }
              output {
                routed: true
              }
            }
            """
        ).strip()
        flow = parse_source(source)
        result = run_flow(flow, inputs={"kind": "other"}, dry_run=True)
        route_items = [item for item in result["trace"] if item["kind"] == "route"]
        self.assertEqual(route_items[0]["selected"], "default")


if __name__ == "__main__":
    unittest.main()
