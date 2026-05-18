"""LeetCode 27: Remove Element.

https://leetcode.com/problems/remove-element/
"""


class Solution:
    def remove_element(self, nums: list[int], val: int) -> int:
        matches: list[int] = []

        for num in nums:
            if num != val:
                matches.append(num)

        nums = matches

        return len(nums)
