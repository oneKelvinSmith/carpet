import pytest
from leetcode.valid_anagram import Solution


@pytest.fixture
def solution() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
    ],
)
def test_valid_anagram(solution: Solution, s: str, t: str, expected: bool) -> None:
    assert solution.is_anagram(s, t) == expected
