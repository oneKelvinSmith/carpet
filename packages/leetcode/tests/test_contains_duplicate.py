import pytest
from leetcode.contains_duplicate import Solution


@pytest.fixture
def solution() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
    ],
)
def test_contains_duplicate(solution: Solution, nums: list[int], expected: bool) -> None:
    assert solution.contains_duplicate(nums) == expected
