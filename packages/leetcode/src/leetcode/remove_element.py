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
                nums.pop(relative_index)
                shifts += 1

        return len(nums)
