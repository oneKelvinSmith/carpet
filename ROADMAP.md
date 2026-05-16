# LeetCode Practice Roadmap

The curriculum below follows the [NeetCode 150](https://neetcode.io/roadmap),
the de facto starter list for LeetCode practice. Each problem has a video
walkthrough on neetcode.io if you get stuck.

Tick problems off as you finish them: `- [ ]` → `- [x]`.

## Workflow

To start a new problem, scaffold it:

```bash
uv run python scripts/new_problem.py <slug> --number <N>
# e.g. uv run python scripts/new_problem.py contains-duplicate --number 217
```

This creates `src/leetcode/<slug>.py` and `tests/leetcode/test_<slug>.py`
with boilerplate. Then implement, run `pytest tests/leetcode/test_<slug>.py`,
and tick the problem here.

For slugs that aren't valid Python module names (e.g. `3sum`), pass
`--module`: `uv run python scripts/new_problem.py 3sum --number 15 --module three_sum`.

---

## Arrays & Hashing

- [ ] [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) (#217)
- [ ] [Valid Anagram](https://leetcode.com/problems/valid-anagram/) (#242)
- [x] [Two Sum](https://leetcode.com/problems/two-sum/) (#1)
- [ ] [Group Anagrams](https://leetcode.com/problems/group-anagrams/) (#49)
- [ ] [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) (#347)
- [ ] [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) (#271)
- [ ] [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) (#238)
- [ ] [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) (#36)
- [ ] [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) (#128)

## Two Pointers

- [ ] [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) (#125)
- [ ] [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) (#167)
- [ ] [3Sum](https://leetcode.com/problems/3sum/) (#15)
- [ ] [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) (#11)
- [ ] [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) (#42)

## Sliding Window

- [ ] [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) (#121)
- [ ] [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) (#3)
- [ ] [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) (#424)
- [ ] [Permutation in String](https://leetcode.com/problems/permutation-in-string/) (#567)
- [ ] [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) (#76)
- [ ] [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) (#239)

## Stack

- [ ] [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) (#20)
- [ ] [Min Stack](https://leetcode.com/problems/min-stack/) (#155)
- [ ] [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) (#150)
- [ ] [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) (#22)
- [ ] [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) (#739)
- [ ] [Car Fleet](https://leetcode.com/problems/car-fleet/) (#853)
- [ ] [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) (#84)

## Binary Search

- [ ] [Binary Search](https://leetcode.com/problems/binary-search/) (#704)
- [ ] [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) (#74)
- [ ] [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) (#875)
- [ ] [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) (#153)
- [ ] [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) (#33)
- [ ] [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) (#981)
- [ ] [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) (#4)

## Linked List

- [ ] [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) (#206)
- [ ] [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) (#21)
- [ ] [Reorder List](https://leetcode.com/problems/reorder-list/) (#143)
- [ ] [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) (#19)
- [ ] [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) (#138)
- [ ] [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) (#2)
- [ ] [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) (#141)
- [ ] [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) (#287)
- [ ] [LRU Cache](https://leetcode.com/problems/lru-cache/) (#146)
- [ ] [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) (#23)
- [ ] [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) (#25)

## Trees

- [ ] [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) (#226)
- [ ] [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) (#104)
- [ ] [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) (#543)
- [ ] [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) (#110)
- [ ] [Same Tree](https://leetcode.com/problems/same-tree/) (#100)
- [ ] [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) (#572)
- [ ] [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) (#235)
- [ ] [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) (#102)
- [ ] [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) (#199)
- [ ] [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) (#1448)
- [ ] [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) (#98)
- [ ] [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) (#230)
- [ ] [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) (#105)
- [ ] [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) (#124)
- [ ] [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) (#297)

## Heap / Priority Queue

- [ ] [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) (#703)
- [ ] [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) (#1046)
- [ ] [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) (#973)
- [ ] [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) (#215)
- [ ] [Task Scheduler](https://leetcode.com/problems/task-scheduler/) (#621)
- [ ] [Design Twitter](https://leetcode.com/problems/design-twitter/) (#355)
- [ ] [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) (#295)

## Backtracking

- [ ] [Subsets](https://leetcode.com/problems/subsets/) (#78)
- [ ] [Combination Sum](https://leetcode.com/problems/combination-sum/) (#39)
- [ ] [Permutations](https://leetcode.com/problems/permutations/) (#46)
- [ ] [Subsets II](https://leetcode.com/problems/subsets-ii/) (#90)
- [ ] [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) (#40)
- [ ] [Word Search](https://leetcode.com/problems/word-search/) (#79)
- [ ] [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) (#131)
- [ ] [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) (#17)
- [ ] [N-Queens](https://leetcode.com/problems/n-queens/) (#51)

## Tries

- [ ] [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) (#208)
- [ ] [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) (#211)
- [ ] [Word Search II](https://leetcode.com/problems/word-search-ii/) (#212)

## Graphs

- [ ] [Number of Islands](https://leetcode.com/problems/number-of-islands/) (#200)
- [ ] [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) (#695)
- [ ] [Clone Graph](https://leetcode.com/problems/clone-graph/) (#133)
- [ ] [Walls and Gates](https://leetcode.com/problems/walls-and-gates/) (#286)
- [ ] [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) (#994)
- [ ] [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) (#417)
- [ ] [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) (#130)
- [ ] [Course Schedule](https://leetcode.com/problems/course-schedule/) (#207)
- [ ] [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) (#210)
- [ ] [Redundant Connection](https://leetcode.com/problems/redundant-connection/) (#684)
- [ ] [Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) (#323)
- [ ] [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) (#261)
- [ ] [Word Ladder](https://leetcode.com/problems/word-ladder/) (#127)

## Advanced Graphs

- [ ] [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) (#332)
- [ ] [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) (#1584)
- [ ] [Network Delay Time](https://leetcode.com/problems/network-delay-time/) (#743)
- [ ] [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) (#778)
- [ ] [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) (#269)
- [ ] [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) (#787)

## 1-D Dynamic Programming

- [ ] [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) (#70)
- [ ] [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) (#746)
- [ ] [House Robber](https://leetcode.com/problems/house-robber/) (#198)
- [ ] [House Robber II](https://leetcode.com/problems/house-robber-ii/) (#213)
- [ ] [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) (#5)
- [ ] [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) (#647)
- [ ] [Decode Ways](https://leetcode.com/problems/decode-ways/) (#91)
- [ ] [Coin Change](https://leetcode.com/problems/coin-change/) (#322)
- [ ] [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) (#152)
- [ ] [Word Break](https://leetcode.com/problems/word-break/) (#139)
- [ ] [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) (#300)
- [ ] [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) (#416)

## 2-D Dynamic Programming

- [ ] [Unique Paths](https://leetcode.com/problems/unique-paths/) (#62)
- [ ] [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) (#1143)
- [ ] [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) (#309)
- [ ] [Coin Change II](https://leetcode.com/problems/coin-change-ii/) (#518)
- [ ] [Target Sum](https://leetcode.com/problems/target-sum/) (#494)
- [ ] [Interleaving String](https://leetcode.com/problems/interleaving-string/) (#97)
- [ ] [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) (#329)
- [ ] [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) (#115)
- [ ] [Edit Distance](https://leetcode.com/problems/edit-distance/) (#72)
- [ ] [Burst Balloons](https://leetcode.com/problems/burst-balloons/) (#312)
- [ ] [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) (#10)

## Greedy

- [ ] [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) (#53)
- [ ] [Jump Game](https://leetcode.com/problems/jump-game/) (#55)
- [ ] [Jump Game II](https://leetcode.com/problems/jump-game-ii/) (#45)
- [ ] [Gas Station](https://leetcode.com/problems/gas-station/) (#134)
- [ ] [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) (#846)
- [ ] [Merge Triplets to Form Target Triplet](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) (#1899)
- [ ] [Partition Labels](https://leetcode.com/problems/partition-labels/) (#763)
- [ ] [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) (#678)

## Intervals

- [ ] [Insert Interval](https://leetcode.com/problems/insert-interval/) (#57)
- [ ] [Merge Intervals](https://leetcode.com/problems/merge-intervals/) (#56)
- [ ] [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) (#435)
- [ ] [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) (#252)
- [ ] [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) (#253)
- [ ] [Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/) (#1851)

## Math & Geometry

- [ ] [Rotate Image](https://leetcode.com/problems/rotate-image/) (#48)
- [ ] [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) (#54)
- [ ] [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) (#73)
- [ ] [Happy Number](https://leetcode.com/problems/happy-number/) (#202)
- [ ] [Plus One](https://leetcode.com/problems/plus-one/) (#66)
- [ ] [Pow(x, n)](https://leetcode.com/problems/powx-n/) (#50)
- [ ] [Multiply Strings](https://leetcode.com/problems/multiply-strings/) (#43)
- [ ] [Detect Squares](https://leetcode.com/problems/detect-squares/) (#2013)

## Bit Manipulation

- [ ] [Single Number](https://leetcode.com/problems/single-number/) (#136)
- [ ] [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) (#191)
- [ ] [Counting Bits](https://leetcode.com/problems/counting-bits/) (#338)
- [ ] [Reverse Bits](https://leetcode.com/problems/reverse-bits/) (#190)
- [ ] [Missing Number](https://leetcode.com/problems/missing-number/) (#268)
- [ ] [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) (#371)
- [ ] [Reverse Integer](https://leetcode.com/problems/reverse-integer/) (#7)

---

## Bonus — Top Interview 150 extras

Problems started from LeetCode's [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/)
list that aren't on NeetCode 150.

- [x] [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) (#88)
- [ ] [Remove Element](https://leetcode.com/problems/remove-element/) (#27) — *in progress*
