"""LeetCode 217: Contains Duplicate.

https://leetcode.com/problems/contains-duplicate/
"""


class Solution:
    def contains_duplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) != len(nums)
