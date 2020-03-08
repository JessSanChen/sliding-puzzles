# sliding-puzzles
Solves sliding puzzles. According to specifications from Artificial Intelligence Lab01. 

# File Descriptions

<b>"sliding_puzzles_p4"</b>
<br>
Progress as of 3/8/2020. 
<br>
Improvements: <br>
- Workable BFS/DFS search function (altered by .popleft() or .pop())
- Returns correct paths
- Both searches done in reasonable time (2-3 seconds for 3x3 puzzles)
- Implements global directory
<br>
Problems:
- Output paths do not match solutions. BFS returns shorter-than-expected paths while DFS returns (far-)longer-than-expected paths.
