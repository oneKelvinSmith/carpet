"""LeetCode 27: Remove Element.

https://leetcode.com/problems/remove-element/
"""


class Solution:
    def remove_element(self, nums: list[int], val: int) -> int:
        shifts: int = 0

        for i in range(len(nums)):
            relative_index = i - shifts
            num = nums[relative_index]
            if num == val:
                nums[relative_index:] = nums[relative_index + 1 :]
                shifts += 1

        return len(nums)
