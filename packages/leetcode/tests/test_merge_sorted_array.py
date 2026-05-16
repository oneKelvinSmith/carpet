import pytest
from leetcode.merge_sorted_array import Solution


@pytest.fixture
def solution() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("nums1", "m", "nums2", "n", "expected"),
    [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
    ],
)
def test_merge_sorted_array(
    solution: Solution, nums1: list[int], m: int, nums2: list[int], n: int, expected: list[int]
) -> None:
    solution.merge(nums1, m, nums2, n)
    assert nums1 == expected
