"""LeetCode 242: Valid Anagram.

https://leetcode.com/problems/valid-anagram/
"""

from collections import Counter


class Solution:
    def is_anagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
