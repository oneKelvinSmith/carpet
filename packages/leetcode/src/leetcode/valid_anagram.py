"""LeetCode 242: Valid Anagram.

https://leetcode.com/problems/valid-anagram/
"""


class Solution:
    def is_anagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        return all(a == b for a, b in zip(sorted(s), sorted(t), strict=True))
