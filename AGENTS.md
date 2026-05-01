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

# Run a flow locally with dry-run mode
python -m llm_flow_dsl run examples/support-triage.flow --input-json input.json --dry-run --pretty

# Run tests
python -m pytest tests/test_mvp_parser.py -v
```

## Architecture

### Core Modules

| Module | Responsibility |
|--------|-----------------|
| [lexer.py](llm_flow_dsl/lexer.py) | Tokenization: converts `.flow` source to Token stream. LexerError for syntax issues. |
| [parser.py](llm_flow_dsl/parser.py) | AST generation: uses Pratt parser for expression precedence. ParseError with diagnostic spans. |
| [ast_nodes.py](llm_flow_dsl/ast_nodes.py) | AST definitions: dataclasses for ExpressionNode, BlockNode. Each has a `Span` for error reporting. |
| [runner.py](llm_flow_dsl/runner.py) | Flow execution: evaluates AST nodes, executes LLM/tool/approval blocks. RunnerError for runtime issues. |
| [validator.py](llm_flow_dsl/validator.py) | Semantic validation: schema checks, symbol resolution, unsafe config detection. |
| [diagnostics.py](llm_flow_dsl/diagnostics.py) | Error reporting: `Span`, `Diagnostic` with line/col context for user-friendly messages. |
| [cli.py](llm_flow_dsl/cli.py) | CLI: parse + run subcommands with argparse; error handling and JSON output. |

### Control Flow

```
.flow file → Lexer (tokens) → Parser (AST) → Validator (checks) → Runner (execution)
```

## DSL Structure

See: [grammar-spec.md](docs/grammar-spec.md) for formal EBNF.

**Top-level**: Flow definition with unique name.

**Blocks**: `input` (declare inputs), `llm` (LLM call with schema), `if/else` (conditional routing), `route` (pattern matching), `tool` (call external tool), `approval` (human decision), `output` (final result).

**Expressions**: Member access (`.`), unary (`not`), comparisons (`==`, `!=`, `<`, `<=`, `>`, `>=`, `in`), logical operators (`and`, `or`).

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

### 4. Testing Patterns
- Parse source strings with `Lexer(source).tokenize()` then `Parser(tokens, source).parse()`.
- Use `unittest` framework; fixtures in `tests/`.
- Deterministic stubs for LLM/tool calls in runner tests.
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
