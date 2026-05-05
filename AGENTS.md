# AI Agent Guide: llm-flow-dsl

## Project Overview

**llm-flow-dsl** is a domain-specific language (DSL) and execution engine for orchestrating LLM decisions with business constraints. It enables product teams to express policy, risk control, and business logic around LLM calls in one readable language.

**Key positioning**: Domain language for AI decisions under business constraints—not a prompt framework, not just workflow automation.

**MVP scope**: Parser + local runner + validation + tests for flow blocks: `input`, `llm`, `route`, `if/else`, `tool`, `approval`, `output`.

See: [README.md](README.md), [product-strategy.md](docs/product-strategy.md)

## Quick Start

```bash
# Parse a flow file into AST (JSON)
python -m llm_flow_dsl parse examples/support-triage.flow --pretty

# Parse + validate
python -m llm_flow_dsl parse examples/support-triage.flow --validate --pretty

# Run a flow locally with dry-run mode
python -m llm_flow_dsl run examples/support-triage.flow --input-json input.json --dry-run --pretty

# Run tests
python -m pytest tests/test_mvp_parser.py -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full dev setup (fork, branch, PR process).

## Architecture

### Core Modules

| Module | Responsibility |
|--------|-----------------|
| [lexer.py](llm_flow_dsl/lexer.py) | Tokenization: converts `.flow` source to `Token` stream. Supports `//` and `#` comments. `LexerError` for syntax issues. |
| [parser.py](llm_flow_dsl/parser.py) | AST generation: uses Pratt parser for expression precedence. `not in` is a single binary operator. `ParseError` with diagnostic spans. |
| [ast_nodes.py](llm_flow_dsl/ast_nodes.py) | AST definitions: dataclasses for all node types. `node_to_dict()` utility converts to JSON. `LlmBlock.properties` stores raw Python values (not AST nodes). |
| [runner.py](llm_flow_dsl/runner.py) | Flow execution: evaluates AST nodes, executes LLM/tool/approval blocks. Dry-run injects `__llm__` override for deterministic LLM output. `RunnerError` for runtime issues. |
| [validator.py](llm_flow_dsl/validator.py) | Semantic validation: duplicate symbol checks, schema checks, undefined identifier resolution, unsafe config detection. |
| [diagnostics.py](llm_flow_dsl/diagnostics.py) | Error reporting: `Span`, `Diagnostic` with `build_snippet()` and `make_diagnostic()` helpers for user-friendly messages with source pointers. |
| [cli.py](llm_flow_dsl/cli.py) | CLI: `parse` + `run` subcommands with argparse; errors emitted as JSON on stderr. |

### Control Flow

```
.flow file → Lexer (tokens) → Parser (AST) → Validator (checks) → Runner (execution)
```

## DSL Structure

See: [grammar-spec.md](docs/grammar-spec.md) for formal EBNF.

**Top-level**: Flow definition with unique name.

**Blocks**: `input` (declare inputs), `llm` (LLM call with schema), `if/else` (conditional routing), `route` (pattern matching), `tool` (call external tool), `approval` (human decision), `output` (final result).

**Expressions**: Member access (`.`), unary (`not`), comparisons (`==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not in`), logical operators (`and`, `or`).

**Example**: [examples/support-triage.flow](examples/support-triage.flow)

## Common Patterns

### 1. Error Handling with Spans
All nodes carry a `Span(start_line, start_col, end_line, end_col)`. Use in diagnostics for precise error locations:
```python
diagnostic = make_diagnostic(node.span, f"Unknown symbol: {name}", "error")
raise ParseError(diagnostic)
```

### 2. Pratt Parser for Expressions
[parser.py](llm_flow_dsl/parser.py) uses precedence climbing. Pattern:
```python
def _parse_expr(self, min_prec=0):
    left = self._parse_primary()
    while self._current_prec() >= min_prec:
        # Apply operator
    return left
```

### 3. Dataclass AST Nodes
Nodes inherit from `Node` and include span + type-hinted fields:
```python
@dataclass
class IfNode(Node):
    condition: ExpressionNode
    then_stmts: List[StatementNode]
    else_stmts: Optional[List[StatementNode]]
```

### 4. Diagnostics with Source Pointers
Use `build_snippet()` and `make_diagnostic()` from [diagnostics.py](llm_flow_dsl/diagnostics.py) for user-friendly error messages:
```python
lines = source.split("\n")
snippet = build_snippet(lines, node.span)
diagnostic = make_diagnostic("E001", f"Unknown symbol: {name}", "error", node.span, lines)
raise ParseError(diagnostic)
```

### 5. Deterministic Runner Tests
Inject `__llm__` into inputs to override LLM output in dry-run mode:
```python
result = run_flow(flow, inputs={"__llm__": {"sentiment": "positive"}}, dry_run=True)
```

### 6. Testing Patterns
- Parse source strings with `Lexer(source).tokenize()` then `Parser(tokens, source).parse()`.
- Use `unittest` framework (single test file: `tests/test_mvp_parser.py`).
- CLI tests use `subprocess.run` with `sys.executable -m llm_flow_dsl`.
- No external mocking library—use `__llm__` override for deterministic LLM stubs.
- Example: [tests/test_mvp_parser.py](tests/test_mvp_parser.py)

## Development Workflow

### Adding a New DSL Block Type
1. Add grammar rule to [docs/grammar-spec.md](docs/grammar-spec.md) (EBNF).
2. Define AST node in [ast_nodes.py](llm_flow_dsl/ast_nodes.py) (dataclass extending `Node`).
3. Add tokenization rules in [lexer.py](llm_flow_dsl/lexer.py) if new keywords.
4. Implement parser method in [parser.py](llm_flow_dsl/parser.py) (e.g., `_parse_approval_stmt`).
5. Add runner logic in [runner.py](llm_flow_dsl/runner.py).
6. Update [validator.py](llm_flow_dsl/validator.py) if new validation rules needed.
7. Write tests in [tests/test_mvp_parser.py](tests/test_mvp_parser.py).

### Adding a New Operator or Expression Type
1. Update grammar in [docs/grammar-spec.md](docs/grammar-spec.md).
2. Define AST node in [ast_nodes.py](llm_flow_dsl/ast_nodes.py).
3. Add token type in [lexer.py](llm_flow_dsl/lexer.py) if needed.
4. Extend Pratt precedence table in [parser.py](llm_flow_dsl/parser.py).
5. Add evaluation logic in [runner.py](llm_flow_dsl/runner.py) (typically `_eval` method).
6. Test in [tests/test_mvp_parser.py](tests/test_mvp_parser.py).

### Fixing a Parser Error
1. Look at error span in diagnostic (line, col).
2. Check token stream: `Lexer(source).tokenize()` to see if lexing is correct.
3. Trace parser call stack in [parser.py](llm_flow_dsl/parser.py)—look for `_expect`, `_peek`, `_advance`.
4. If grammar ambiguity, check Pratt precedence in [parser.py](llm_flow_dsl/parser.py).
5. Add test case to [tests/test_mvp_parser.py](tests/test_mvp_parser.py) before fixing.

## Conventions

- **Type hints**: All functions and variables typed with `Optional`, `List`, `Dict`, etc.
- **Dataclasses**: AST nodes are frozen or unfrozen depending on mutability needs.
- **Error types**: `LexerError`, `ParseError`, `RunnerError`—each carries diagnostic context.
- **File extensions**: `.flow` for DSL files.
- **CLI**: Subcommands (`parse`, `run`) with flags like `--pretty`, `--dry-run`.
- **Naming**: Private methods prefixed with `_`; public API documented.
- **`not in`**: Treated as a single binary operator in parser and lexer, not two separate tokens.
- **`LlmBlock.properties`**: Stores raw Python values (strings, dicts, lists), not AST nodes.
- **Output**: CLI emits JSON payloads on stdout, diagnostics/errors on stderr.
- **Comments**: Both `//` and `#` line comments supported in `.flow` files.

## Key Files at a Glance

```
llm_flow_dsl/
  __init__.py           (package marker)
  __main__.py           (entry point for `python -m llm_flow_dsl`)
  cli.py                (argparse CLI, error formatting)
  lexer.py              (tokenizer, Token class)
  parser.py             (Pratt parser, AST builder)
  ast_nodes.py          (dataclass definitions)
  runner.py             (flow executor, expression evaluator)
  validator.py          (semantic analysis)
  diagnostics.py        (Span, Diagnostic, error reporting)
tests/
  test_mvp_parser.py    (parser + runner tests)
examples/
  support-triage.flow   (reference example)
  duplicate-symbols.flow (edge case example)
docs/
  grammar-spec.md       (EBNF formal grammar)
  product-strategy.md   (business vision)
  roadmap.md            (roadmap)
.cursor/
  rules/
    karpathy-guidelines.mdc (Karpathy behavioral guidelines for LLM coding)
SKILL.md                  (Karpathy guidelines skill definition)
```

## When to Modify Each File

- **Grammar changes** → Update `docs/grammar-spec.md`, then `ast_nodes.py`, `lexer.py`, `parser.py`, `validator.py`.
- **Runner logic** → `runner.py` (evaluation, execution flow).
- **Error messages** → `diagnostics.py` and error classes in `lexer.py`, `parser.py`, `runner.py`.
- **CLI features** → `cli.py` (new subcommands, flags).
- **Tests** → `tests/test_mvp_parser.py` (always add test *before* fixing bugs).

## Notes for AI Agents

1. **Always check spans**: Use `node.span` when reporting errors—users expect accurate line/col info.
2. **Dataclass order matters**: AST node fields are often positional; preserve order when refactoring.
3. **Pratt precedence is fragile**: When adding operators, carefully test associativity and precedence against expected behavior.
4. **Deterministic tests**: Use fixtures or mocks; do not call external LLMs in CI tests.
5. **Link, don't duplicate**: Refer to [docs/grammar-spec.md](docs/grammar-spec.md) instead of restating grammar rules.
6. **`not in` awareness**: `not in` is a single binary operator in both lexer and parser. Do not tokenize it as two separate tokens.
7. **`LlmBlock.properties`**: Contains raw Python values (e.g., `{"prompt": "..." , "output_schema": {...}}`), NOT AST nodes. Handle accordingly in runner and validator.
8. **CLI stderr protocol**: All diagnostics and errors go to stderr as JSON. stdout is reserved for successful JSON payloads.
9. **Karpathy guidelines**: The project has Karpathy behavioral guidelines in `.cursor/rules/karpathy-guidelines.mdc` and `SKILL.md`. Follow them: think before coding, keep changes surgical, define success criteria.
10. **Single test file**: All tests live in `tests/test_mvp_parser.py` using `unittest`. Add new test classes there rather than creating separate test files.
