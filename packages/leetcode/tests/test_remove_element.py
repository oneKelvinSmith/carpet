import pytest
from leetcode.remove_element import Solution


@pytest.fixture
def solution() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("nums", "val", "expected"),
    [
        ([3, 2, 2, 3], 3, 2),
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5),
    ],
)
def test_remove_element(solution: Solution, nums: list[int], val: int, expected: int) -> None:
    assert solution.remove_element(nums, val) == expected
