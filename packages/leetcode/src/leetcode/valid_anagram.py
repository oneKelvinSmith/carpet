"""LeetCode 242: Valid Anagram.

https://leetcode.com/problems/valid-anagram/
"""


class Solution:
    def is_anagram(self, s: str, t: str) -> bool:
        return len(set(s) - set(t)) == 0
