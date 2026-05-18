"""LeetCode 27: Remove Element.

https://leetcode.com/problems/remove-element/
"""


class Solution:
    def remove_element(self, nums: list[int], val: int) -> int:
        k = 0

        for num in nums:
            if num != val:
                nums[k] = num
                k += 1

        return k
