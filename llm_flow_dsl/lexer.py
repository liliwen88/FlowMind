from dataclasses import dataclass
from typing import List, Optional

from .diagnostics import Span, make_diagnostic


KEYWORDS = {
    "flow",
    "input",
    "llm",
    "if",
    "else",
    "route",
    "on",
    "tool",
    "approval",
    "output",
    "and",
    "or",
    "not",
    "in",
    "default",
    "true",
    "false",
}


@dataclass
class Token:
    kind: str
    value: str
    span: Span


class LexerError(Exception):
    def __init__(self, diagnostic):
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.lines = source.splitlines()
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.col = 1

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while not self._is_eof():
            ch = self._peek()
            if ch in " \t\r\n":
                self._consume_whitespace()
                continue
            if ch == "/" and self._peek(1) == "/":
                self._consume_line_comment()
                continue
            if ch == "#":
                self._consume_line_comment()
                continue
            if ch == '"':
                tokens.append(self._read_string())
                continue
            if ch.isdigit():
                tokens.append(self._read_number())
                continue
            if self._is_ident_start(ch):
                tokens.append(self._read_identifier_or_keyword())
                continue
            token = self._read_symbol()
            if token is None:
                span = Span(self.line, self.col, self.line, self.col + 1)
                raise LexerError(
                    make_diagnostic(
                        code="E_LEX_CHAR",
                        message="Unexpected character: {0}".format(ch),
                        severity="error",
                        span=span,
                        source_lines=self.lines,
                    )
                )
            tokens.append(token)

        eof_span = Span(self.line, self.col, self.line, self.col)
        tokens.append(Token("EOF", "", eof_span))
        return tokens

    def _is_eof(self) -> bool:
        return self.index >= self.length

    def _peek(self, offset: int = 0) -> str:
        target = self.index + offset
        if target >= self.length:
            return "\0"
        return self.source[target]

    def _advance(self) -> str:
        ch = self.source[self.index]
        self.index += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _consume_whitespace(self) -> None:
        while not self._is_eof() and self._peek() in " \t\r\n":
            self._advance()

    def _consume_line_comment(self) -> None:
        while not self._is_eof() and self._peek() != "\n":
            self._advance()

    def _read_string(self) -> Token:
        start_line = self.line
        start_col = self.col
        self._advance()  # open quote
        chars: List[str] = []
        while not self._is_eof():
            ch = self._advance()
            if ch == '"':
                span = Span(start_line, start_col, self.line, self.col)
                return Token("STRING", "".join(chars), span)
            if ch == "\\":
                if self._is_eof():
                    break
                esc = self._advance()
                mapping = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
                chars.append(mapping.get(esc, esc))
            else:
                chars.append(ch)

        span = Span(start_line, start_col, self.line, self.col)
        raise LexerError(
            make_diagnostic(
                code="E_LEX_STRING",
                message="Unterminated string literal",
                severity="error",
                span=span,
                source_lines=self.lines,
            )
        )

    def _read_number(self) -> Token:
        start_line = self.line
        start_col = self.col
        chars: List[str] = []
        has_dot = False
        while not self._is_eof():
            ch = self._peek()
            if ch.isdigit():
                chars.append(self._advance())
                continue
            if ch == "." and not has_dot and self._peek(1).isdigit():
                has_dot = True
                chars.append(self._advance())
                continue
            break

        span = Span(start_line, start_col, self.line, self.col)
        return Token("NUMBER", "".join(chars), span)

    def _is_ident_start(self, ch: str) -> bool:
        return ch.isalpha() or ch == "_"

    def _is_ident_part(self, ch: str) -> bool:
        return ch.isalnum() or ch == "_"

    def _read_identifier_or_keyword(self) -> Token:
        start_line = self.line
        start_col = self.col
        chars: List[str] = []
        while not self._is_eof() and self._is_ident_part(self._peek()):
            chars.append(self._advance())
        value = "".join(chars)
        kind = "KEYWORD" if value in KEYWORDS else "IDENT"
        span = Span(start_line, start_col, self.line, self.col)
        return Token(kind, value, span)

    def _read_symbol(self) -> Optional[Token]:
        start_line = self.line
        start_col = self.col
        ch = self._peek()
        ch2 = ch + self._peek(1)
        multi = {"->", "<=", ">=", "==", "!="}
        if ch2 in multi:
            self._advance()
            self._advance()
            span = Span(start_line, start_col, self.line, self.col)
            return Token("SYMBOL", ch2, span)
        single = {"{", "}", "(", ")", ":", ",", ".", "<", ">"}
        if ch in single:
            self._advance()
            span = Span(start_line, start_col, self.line, self.col)
            return Token("SYMBOL", ch, span)
        return None

