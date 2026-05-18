"""LeetCode 27: Remove Element.

https://leetcode.com/problems/remove-element/
"""


class Solution:
    def remove_element(self, nums: list[int], val: int) -> int:
        indices: list[int] = []
        for i, num in enumerate(nums):
            if num == val:
                indices.append(i)

        for ii, i in enumerate(indices):
            relative_index = i - ii
            nums[relative_index:] = nums[relative_index + 1 :]

        return len(nums)
