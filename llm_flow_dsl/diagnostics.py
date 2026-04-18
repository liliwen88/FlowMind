from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Span:
    start_line: int
    start_col: int
    end_line: int
    end_col: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "start_line": self.start_line,
            "start_col": self.start_col,
            "end_line": self.end_line,
            "end_col": self.end_col,
        }


@dataclass
class Diagnostic:
    code: str
    message: str
    severity: str
    span: Span
    snippet: str
    pointer: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "line": self.span.start_line,
            "column": self.span.start_col,
            "span": self.span.to_dict(),
            "snippet": self.snippet,
            "pointer": self.pointer,
        }


def build_snippet(source_lines: List[str], span: Span) -> Dict[str, str]:
    if span.start_line <= 0 or span.start_line > len(source_lines):
        return {"snippet": "", "pointer": ""}

    line = source_lines[span.start_line - 1].rstrip("\n")
    start = max(1, span.start_col)
    end = max(start, span.end_col)
    width = max(1, end - start)
    pointer = " " * (start - 1) + "^" + "~" * (width - 1)
    return {"snippet": line, "pointer": pointer}


def make_diagnostic(
    code: str,
    message: str,
    severity: str,
    span: Span,
    source_lines: Optional[List[str]] = None,
) -> Diagnostic:
    if source_lines is None:
        snippet = ""
        pointer = ""
    else:
        render = build_snippet(source_lines, span)
        snippet = render["snippet"]
        pointer = render["pointer"]

    return Diagnostic(
        code=code,
        message=message,
        severity=severity,
        span=span,
        snippet=snippet,
        pointer=pointer,
    )

