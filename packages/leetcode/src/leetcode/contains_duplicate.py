"""LeetCode 217: Contains Duplicate.

https://leetcode.com/problems/contains-duplicate/
"""


class Solution:
    def contains_duplicate(self, nums: list[int]) -> bool:
        seen: set[int] = set()
        add_to_seen = seen.add
        for num in nums:
            if num in seen:
                return True

            add_to_seen(num)

        return False
