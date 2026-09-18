#!/usr/bin/env python3
"""Deterministic memory inventory helper for memory-curation skill.

Scans markdown memory files and prints a markdown issue table.
Does not modify files. Product-agnostic: pass paths explicitly.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List

PROJECT_HINT = re.compile(
    r"(?i)([A-Za-z]:\\|/)([\w./\\-]+)|\b(api|endpoint|module|package|dependency|version|repo|commit|branch)\b"
    r"|\b(v?\d+\.\d+(\.\d+)?)\b"
)
PROGRESS_HINT = re.compile(
    r"(?i)\b(todo|wip|进度|待办|下一步|临时|draft|in progress|tbd|fixme)\b"
)
PREF_HINT = re.compile(
    r"(?i)(以后都|所有项目|全局|always|never|prefer|preference|回复|语言|不要默认|workflow|禁令|"
    r"记忆|检索|注入|scope|curation|协作|隔离|按需)"
)
PLACEHOLDER = re.compile(
    r"(?i)^\s*(\(\s*(暂无|none|tbd)\s*\)|—|-|todo|tbd|\(\s*暂无其他全局事实\s*\))\s*$"
)
BULLET = ("- ", "* ", "+ ")


def iter_entries(text: str, path: Path, scope_guess: str) -> Iterable[Dict[str, str]]:
    lines = text.splitlines()
    front: Dict[str, str] = {}
    buf: List[str] = []
    start = 1
    heading = ""

    def make_row(body: str, line_no: int) -> Dict[str, str]:
        issues: List[str] = []
        claim_lines = [
            ln for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("#")
        ]
        claim = (claim_lines[0] if claim_lines else body)[:120]
        fm_scope = front.get("scope", "")
        if PLACEHOLDER.match(body.strip()):
            issues.append("placeholder")
        if PROGRESS_HINT.search(body) and scope_guess in ("user", "project"):
            issues.append("progress-in-longterm")
        if scope_guess == "user" and PROJECT_HINT.search(body) and not PREF_HINT.search(body):
            issues.append("project-like-in-user")
        if scope_guess == "project" and PREF_HINT.search(body) and not PROJECT_HINT.search(body):
            issues.append("possible-user-pref")
        if path.name.upper().startswith("MEMORY") and not fm_scope and scope_guess != "user":
            issues.append("no-entry-scope-meta")
        if len(body) > 400:
            issues.append("too-long")
        return {
            "file": str(path),
            "line": str(line_no),
            "scope_guess": scope_guess,
            "fm_scope": fm_scope,
            "heading": heading,
            "claim": claim.replace("|", "/"),
            "issues": ",".join(issues) if issues else "-",
        }

    def flush(end_line: int) -> List[Dict[str, str]]:
        nonlocal buf, start
        body = "\n".join(buf).strip()
        buf = []
        if not body:
            start = end_line
            return []
        if body.startswith("#") and "\n" not in body:
            start = end_line
            return []
        row = make_row(body, start)
        start = end_line
        return [row]

    i = 0
    while i < len(lines):
        line = lines[i]
        if i == 0 and line.strip() == "---":
            i += 1
            while i < len(lines) and lines[i].strip() != "---":
                if ":" in lines[i]:
                    k, v = lines[i].split(":", 1)
                    front[k.strip().lower()] = v.strip()
                i += 1
            i += 1
            continue

        if line.startswith("#"):
            for row in flush(i + 1):
                yield row
            heading = line.lstrip("#").strip()
            start = i + 1
            i += 1
            continue

        if not line.strip():
            i += 1
            continue

        if line.lstrip().startswith(BULLET):
            # one bullet == one entry
            for row in flush(i + 1):
                yield row
            start = i + 1
            buf = [line]
            i += 1
            continue

        if not buf:
            start = i + 1
        buf.append(line)
        i += 1

    for row in flush(len(lines) + 1):
        yield row


def collect(path: Path, scope_guess: str) -> List[Dict[str, str]]:
    if not path or not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return list(iter_entries(text, path, scope_guess))


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventory memory markdown files for curation flags")
    ap.add_argument("--user", type=Path, help="User-layer MEMORY.md")
    ap.add_argument("--project-agents", type=Path, help="Project AGENTS.md")
    ap.add_argument("--project-memory", type=Path, help="Project MEMORY.md if any")
    ap.add_argument("--session", type=Path, help="Session notes.md")
    args = ap.parse_args()

    rows: List[Dict[str, str]] = []
    if args.user:
        rows += collect(args.user, "user")
    if args.project_agents:
        rows += collect(args.project_agents, "project")
    if args.project_memory:
        rows += collect(args.project_memory, "project")
    if args.session:
        rows += collect(args.session, "session")

    flagged = [r for r in rows if r["issues"] != "-"]
    print("## Inventory (script)")
    print()
    print(f"- entries: {len(rows)}")
    print(f"- flagged: {len(flagged)}")
    print()
    print("| id | file:line | scope_guess | claim | issues |")
    print("|---|---|---|---|---|")
    for idx, r in enumerate(rows, 1):
        if r["issues"] == "-":
            continue
        print(
            f"| E-{idx:02d} | `{Path(r['file']).name}:{r['line']}` | {r['scope_guess']} | {r['claim']} | {r['issues']} |"
        )
    if not flagged:
        print("| — | — | — | no script-flagged issues | — |")
    print()
    print("Script flags are hints. Final scope uses the judgment tree + user confirmation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
