"""Scaffold a new LeetCode problem solution + test pair.

Title and number are looked up from ROADMAP.md by slug. The slug
argument accepts a slug ('two-sum'), full URL, or a fuzzy partial
title ('longest substr' -> 'longest-substring-without-repeating-characters').

Usage:
    uv run new-problem SLUG_OR_URL_OR_PARTIAL
    uv run new-problem --next

Examples:
    uv run new-problem contains-duplicate
    uv run new-problem https://leetcode.com/problems/two-sum/
    uv run new-problem "longest substr"
    uv run new-problem --next
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from rapidfuzz import fuzz, process

# .../packages/leetcode/src/leetcode/_scaffold.py → .../packages/leetcode
PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PACKAGE_ROOT / "src" / "leetcode"
TESTS_DIR = PACKAGE_ROOT / "tests"
ROADMAP_PATH = PACKAGE_ROOT / "ROADMAP.md"

FUZZY_ACCEPT_THRESHOLD = 75  # rapidfuzz WRatio score; above this we auto-accept


SOLUTION_TEMPLATE = '''"""LeetCode{number_str}{title}.

https://leetcode.com/problems/{slug}/
"""


class Solution:
    pass  # TODO: implement
'''

TEST_TEMPLATE = """import pytest

from leetcode.{module} import Solution


@pytest.fixture
def solution() -> Solution:
    return Solution()


# TODO: replace with real cases and uncomment.
# @pytest.mark.parametrize(
#     ("arg", "expected"),
#     [
#         (..., ...),
#     ],
# )
# def test_{module}(solution: Solution, arg: ..., expected: ...) -> None:
#     assert solution.method(arg) == expected
"""


URL_SLUG_RE = re.compile(r"leetcode\.com/problems/([^/?#]+)")
ROADMAP_ENTRY_RE = re.compile(
    r"- \[(?P<tick>[ x])\] "
    r"\[(?P<title>[^\]]+)\]"
    r"\([^)]*?/problems/(?P<slug>[^/]+)/[^)]*\)"
    r"\s*\(#(?P<number>\d+)\)"
)


def parse_slug(arg: str) -> str:
    """Accept either a slug ('two-sum') or a LeetCode URL."""
    match = URL_SLUG_RE.search(arg)
    return match.group(1) if match else arg


def slug_to_module(slug: str) -> str:
    return slug.replace("-", "_")


def slug_to_title(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.split("-"))


def list_roadmap_entries(*, unticked_only: bool = False) -> list[tuple[str, str, int]]:
    """Return [(title, slug, number), ...] from ROADMAP.md in file order."""
    if not ROADMAP_PATH.exists():
        return []
    out: list[tuple[str, str, int]] = []
    for m in ROADMAP_ENTRY_RE.finditer(ROADMAP_PATH.read_text()):
        if unticked_only and m.group("tick") != " ":
            continue
        out.append((m.group("title"), m.group("slug"), int(m.group("number"))))
    return out


def lookup_in_roadmap(slug: str) -> tuple[str | None, int | None]:
    """Return (title, number) for `slug` if found exactly in ROADMAP.md."""
    for title, candidate_slug, number in list_roadmap_entries():
        if candidate_slug == slug:
            return title, number
    return None, None


def fuzzy_match(query: str, entries: list[tuple[str, str, int]]) -> list[tuple[str, str, float]]:
    """Return [(title, slug, score), ...] sorted by score descending."""
    choices: dict[str, str] = {slug: title for title, slug, _ in entries}
    raw = process.extract(query, choices, scorer=fuzz.WRatio, limit=5)
    return [(title, slug, score) for title, score, slug in raw]


def resolve_slug(arg: str) -> str | None:
    """Resolve arg → canonical slug, using URL parse + exact + fuzzy match."""
    slug = parse_slug(arg)

    title, _ = lookup_in_roadmap(slug)
    if title is not None:
        return slug

    entries = list_roadmap_entries()
    if not entries:
        return slug

    matches = fuzzy_match(arg, entries)
    if matches and matches[0][2] >= FUZZY_ACCEPT_THRESHOLD:
        title, resolved_slug, score = matches[0]
        print(f"matched: '{arg}' → {title} ({resolved_slug}, score {score:.0f})", file=sys.stderr)
        return resolved_slug

    print(f"error: '{arg}' didn't resolve to a problem in ROADMAP.md.", file=sys.stderr)
    if matches:
        print("did you mean:", file=sys.stderr)
        for title, slug, score in matches[:3]:
            print(f"  {title}  ({slug})  [score {score:.0f}]", file=sys.stderr)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new LeetCode problem.")
    parser.add_argument(
        "slug",
        nargs="?",
        help="slug ('two-sum'), URL, or partial title (fuzzy matched against ROADMAP)",
    )
    parser.add_argument(
        "--next",
        action="store_true",
        dest="pick_next",
        help="Pick the first unticked problem from ROADMAP.md",
    )
    parser.add_argument("--number", "-n", type=int, help="LeetCode problem number (override)")
    parser.add_argument(
        "--module",
        "-m",
        help="Python module name (override; default: derived from slug)",
    )
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if args.pick_next and args.slug:
        parser.error("--next and a slug argument are mutually exclusive")
    if not args.pick_next and not args.slug:
        parser.error("provide a slug/URL/partial title, or --next")

    if args.pick_next:
        unticked = list_roadmap_entries(unticked_only=True)
        if not unticked:
            print("error: no unticked problems in ROADMAP.md", file=sys.stderr)
            return 1
        title, slug, number = unticked[0]
        print(f"next unticked: {title} (#{number})", file=sys.stderr)
    else:
        resolved = resolve_slug(args.slug)
        if resolved is None:
            return 1
        slug = resolved

    module: str = args.module or slug_to_module(slug)
    if not module.isidentifier():
        print(
            f"error: '{module}' is not a valid Python module name. "
            f"Pass --module with a valid identifier (e.g. --module three_sum).",
            file=sys.stderr,
        )
        return 1

    roadmap_title, roadmap_number = lookup_in_roadmap(slug)
    title = roadmap_title or slug_to_title(slug)
    number = args.number if args.number is not None else roadmap_number
    number_str = f" {number}: " if number is not None else ": "

    if roadmap_title is None and args.number is None:
        print(
            f"warning: '{slug}' not found in ROADMAP.md; "
            f"using derived title and no problem number.",
            file=sys.stderr,
        )

    solution_path = SRC_DIR / f"{module}.py"
    test_path = TESTS_DIR / f"test_{module}.py"

    if not args.force:
        for path in (solution_path, test_path):
            if path.exists():
                print(
                    f"error: {path.relative_to(PACKAGE_ROOT)} already exists. "
                    f"Use --force to overwrite.",
                    file=sys.stderr,
                )
                return 1

    solution_path.write_text(
        SOLUTION_TEMPLATE.format(slug=slug, number_str=number_str, title=title)
    )
    test_path.write_text(TEST_TEMPLATE.format(module=module))

    print(f"Created {solution_path.relative_to(PACKAGE_ROOT)}")
    print(f"Created {test_path.relative_to(PACKAGE_ROOT)}")
    print(f"\nNext: open {solution_path.relative_to(PACKAGE_ROOT)} and implement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
