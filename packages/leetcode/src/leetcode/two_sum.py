"""LeetCode 1: Two Sum.

Given an array of integers `nums` and an integer `target`, return the indices
of the two numbers that add up to target. Each input has exactly one solution,
and you may not use the same element twice.
"""


class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
