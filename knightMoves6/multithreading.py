
#!/usr/bin/env python3
import sys
import itertools
import concurrent.futures
import time

# Increase recursion limit in case deep search is needed.
sys.setrecursionlimit(10000)

# -----------------------
# Board setup
# -----------------------
# The board is fixed (rows 0..5 correspond to chess rows 1..6, with row0 = a1, row5 = a6).
# Board layout (each inner list is a row; row0 is a1... row5 is a6):
#   a    b    c    d    e    f
#6: A    B    B    C    C    C   -> row5
#5: A    B    B    C    C    C   -> row4
#4: A    A    B    B    C    C   -> row3
#3: A    A    B    B    C    C   -> row2
#2: A    A    A    B    B    C   -> row1
#1: A    A    A    B    B    C   -> row0
board = [
    ['A', 'A', 'A', 'B', 'B', 'C'],  # row0 = a1, b1, c1, d1, e1, f1
    ['A', 'A', 'A', 'B', 'B', 'C'],  # row1 = a2, b2, c2, d2, e2, f2
    ['A', 'A', 'B', 'B', 'C', 'C'],  # row2 = a3, b3, c3, d3, e3, f3
    ['A', 'A', 'B', 'B', 'C', 'C'],  # row3 = a4, b4, c4, d4, e4, f4
    ['A', 'B', 'B', 'C', 'C', 'C'],  # row4 = a5, b5, c5, d5, e5, f5
    ['A', 'B', 'B', 'C', 'C', 'C']   # row5 = a6, b6, c6, d6, e6, f6
]

# -----------------------
# Precompute knight moves
# -----------------------
knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                (1, 2), (1, -2), (-1, 2), (-1, -2)]
neighbors = {}
for r in range(6):
    for c in range(6):
        nbrs = []
        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 6 and 0 <= nc < 6:
                nbrs.append((nr, nc))
        neighbors[(r, c)] = nbrs

# -----------------------
# Scoring and DFS functions
# -----------------------
def update_score(score, from_pos, to_pos, vals):
    """
    Given the current score, update it for the move from from_pos to to_pos.
    If the move is between two squares with the same letter, add the letter’s value.
    Otherwise, multiply by that value.
    """
    letter_from = board[from_pos[0]][from_pos[1]]
    letter_to   = board[to_pos[0]][to_pos[1]]
    if letter_from == letter_to:
        return score + vals[letter_to]
    else:
        return score * vals[letter_to]

def dfs(pos, target, score, path, visited, vals):
    """
    Recursively search for a knight’s path (without revisiting squares) from pos to target.
    Prune branches where score > 2024.
    """
    if score > 2024:
        return None
    if pos == target:
        if score == 2024:
            return list(path)
        else:
            return None
    for nxt in neighbors[pos]:
        if nxt in visited:
            continue
        new_score = update_score(score, pos, nxt, vals)
        if new_score > 2024:
            continue
        visited.add(nxt)
        path.append(nxt)
        result = dfs(nxt, target, new_score, path, visited, vals)
        if result is not None:
            return result
        path.pop()
        visited.remove(nxt)
    return None

def coord_to_str(pos):
    """Convert board coordinates (r, c) to chess notation (e.g. (0,0) -> 'a1')."""
    r, c = pos
    return chr(ord('a') + c) + str(r + 1)

# -----------------------
# Candidate search function
# -----------------------
def candidate_search(candidate):
    """
    Given a candidate assignment for A, B, and C, attempt to find:
      - a knight’s trip from a1 (0,0) to f6 (5,5) and
      - a knight’s trip from a6 (5,0) to f1 (0,5),
    each scoring exactly 2024 points.
    If successful, return a tuple (A+B+C, solution_string) in the required format.
    """
    A_val, B_val, C_val = candidate
    vals = {'A': A_val, 'B': B_val, 'C': C_val}
    
    # First tour: from a1 (0,0) to f6 (5,5)
    start1, target1 = (0, 0), (5, 5)
    visited1 = {start1}
    path1 = [start1]
    sol1 = dfs(start1, target1, vals['A'], path1, visited1, vals)
    if sol1 is None:
        return None

    # Second tour: from a6 (5,0) to f1 (0,5)
    start2, target2 = (5, 0), (0, 5)
    visited2 = {start2}
    path2 = [start2]
    sol2 = dfs(start2, target2, vals['A'], path2, visited2, vals)
    if sol2 is None:
        return None

    tour1_str = ",".join(coord_to_str(pos) for pos in sol1)
    tour2_str = ",".join(coord_to_str(pos) for pos in sol2)
    output = f"{A_val},{B_val},{C_val},{tour1_str},{tour2_str}"
    return (A_val + B_val + C_val, output)

# -----------------------
# Main function using multiprocessing
# -----------------------
def main():
    start_time = time.time()
    candidates = []
    # Loop over all distinct positive integers A, B, C with A+B+C < 50.
    for A_val in range(1, 50):
        for B_val in range(1, 50):
            if B_val == A_val:
                continue
            for C_val in range(1, 50):
                if C_val == A_val or C_val == B_val:
                    continue
                if A_val + B_val + C_val >= 50:
                    continue
                candidates.append((A_val, B_val, C_val))
    
    best_sum = float('inf')
    best_solution = None

    # Use a process pool to search candidates in parallel.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Map candidate_search over all candidate assignments.
        results = list(executor.map(candidate_search, candidates))
        for res in results:
            if res is not None:
                current_sum, sol_output = res
                if current_sum < best_sum:
                    best_sum = current_sum
                    best_solution = sol_output
                    print(f"Found solution with A+B+C = {best_sum}: {sol_output}")
                    # Optionally, uncomment the next line to stop at the first solution.
                    # break

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Elapsed time: {elapsed:.2f} seconds")
    if best_solution is None:
        print("No solution found.")
    else:
        print("Final solution:")
        print(best_solution)

if __name__ == '__main__':
    main()
