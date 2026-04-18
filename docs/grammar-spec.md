# llm-flow-dsl Grammar Spec (MVP)

This document defines the minimal runnable grammar implemented in the Python parser.

## Top-level

```ebnf
flow         := "flow" STRING "{" statement* "}"
statement    := input_block
             | llm_block
             | if_stmt
             | route_stmt
             | tool_stmt
             | approval_stmt
             | output_block
```

## Blocks and statements

```ebnf
input_block  := "input" "{" input_field* "}"
input_field  := IDENT ":" IDENT

llm_block    := "llm" IDENT "{" llm_prop* "}"
llm_prop     := IDENT ":" literal
             | "output_schema" ":" schema_obj

schema_obj   := "{" schema_field (","? schema_field)* "}"
schema_field := IDENT ":" IDENT

if_stmt      := "if" expr "{" statement* "}" ("else" "{" statement* "}")?

route_stmt   := "route" "on" expr "{" route_case* route_default? "}"
route_case   := STRING "->" (tool_stmt | approval_stmt)
route_default:= "default" "->" (tool_stmt | approval_stmt)

tool_stmt    := "tool" STRING
approval_stmt:= "approval" STRING

output_block := "output" "{" output_field (","? output_field)* "}"
output_field := IDENT ":" expr
```

## Expressions (Pratt precedence)

Higher precedence binds stronger.

1. Member access: `.`
2. Unary: `not`
3. Comparisons: `== != < <= > >= in not in`
4. Boolean `and`
5. Boolean `or`

```ebnf
expr         := or_expr
or_expr      := and_expr ("or" and_expr)*
and_expr     := cmp_expr ("and" cmp_expr)*
cmp_expr     := unary_expr (cmp_op unary_expr)*
cmp_op       := "==" | "!=" | "<" | "<=" | ">" | ">=" | "in" | "not in"
unary_expr   := "not" unary_expr | member_expr
member_expr  := primary ("." IDENT)*
primary      := IDENT | STRING | NUMBER | BOOLEAN | "(" expr ")"
BOOLEAN      := "true" | "false"
```

## Validation rules (MVP)

- Undefined identifiers in expressions are errors.
- Route case keys cannot repeat.
- Route default branch cannot repeat.
- `llm` block must have:
  - `prompt` as string
  - `output_schema` with at least one field
- `tool` and `approval` names must be non-empty strings.

