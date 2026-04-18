import argparse
import json
import sys
from typing import List, Optional, Tuple

from .ast_nodes import node_to_dict
from .diagnostics import Diagnostic
from .lexer import Lexer, LexerError
from .parser import ParseError, Parser
from .runner import RunnerError, run_flow
from .validator import validate_flow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm_flow_dsl")
    sub = parser.add_subparsers(dest="command", required=True)

    parse_cmd = sub.add_parser("parse", help="Parse a .flow file")
    parse_cmd.add_argument("file", help="Path to .flow file")
    parse_cmd.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parse_cmd.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip semantic validation",
    )

    run_cmd = sub.add_parser("run", help="Run a .flow file with local runtime")
    run_cmd.add_argument("file", help="Path to .flow file")
    run_cmd.add_argument("--input-json", help="Path to JSON inputs", default=None)
    run_cmd.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    run_cmd.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip semantic validation",
    )
    run_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Run with dry-run trace mode",
    )
    return parser


def run(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "parse":
        return _run_parse(args.file, pretty=args.pretty, validate=not args.no_validate)
    if args.command == "run":
        return _run_runtime(
            args.file,
            input_json_path=args.input_json,
            pretty=args.pretty,
            validate=not args.no_validate,
            dry_run=args.dry_run,
        )
    parser.error("unknown command")
    return 2


def _run_parse(path: str, pretty: bool, validate: bool) -> int:
    loaded = _load_and_parse(path, validate)
    if loaded is None:
        return 1
    flow, _ = loaded
    ast_payload = node_to_dict(flow)
    if pretty:
        sys.stdout.write(json.dumps(ast_payload, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(json.dumps(ast_payload, ensure_ascii=False) + "\n")
    return 0


def _run_runtime(
    path: str,
    input_json_path: Optional[str],
    pretty: bool,
    validate: bool,
    dry_run: bool,
) -> int:
    loaded = _load_and_parse(path, validate)
    if loaded is None:
        return 1
    flow, _ = loaded
    inputs = {}
    if input_json_path:
        try:
            with open(input_json_path, "r", encoding="utf-8-sig") as f:
                inputs = json.load(f)
        except (OSError, ValueError) as exc:
            payload = {"code": "E_INPUT_JSON", "message": str(exc), "severity": "error"}
            sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
            return 1
        if not isinstance(inputs, dict):
            payload = {
                "code": "E_INPUT_JSON",
                "message": "input JSON must be an object",
                "severity": "error",
            }
            sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
            return 1

    try:
        result = run_flow(flow, inputs=inputs, dry_run=dry_run)
    except RunnerError as exc:
        payload = {"code": "E_RUNTIME", "message": str(exc), "severity": "error"}
        sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return 1

    if pretty:
        sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
    return 0


def _load_and_parse(path: str, validate: bool) -> Optional[Tuple[object, str]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError as exc:
        payload = {"code": "E_IO", "message": str(exc), "severity": "error"}
        sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return None

    try:
        tokens = Lexer(source).tokenize()
        flow = Parser(tokens, source).parse()
    except LexerError as exc:
        sys.stderr.write(json.dumps(exc.diagnostic.to_dict(), ensure_ascii=False) + "\n")
        return None
    except ParseError as exc:
        sys.stderr.write(json.dumps(exc.diagnostic.to_dict(), ensure_ascii=False) + "\n")
        return None

    if validate:
        diagnostics = validate_flow(flow, source)
        if diagnostics:
            _emit_diagnostics(diagnostics)
            return None

    return flow, source


def _emit_diagnostics(diagnostics: List[Diagnostic]) -> None:
    payload = [diag.to_dict() for diag in diagnostics]
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
