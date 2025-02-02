
#!/usr/bin/env python3
import sys

# Increase recursion limit in case deep search is needed.
sys.setrecursionlimit(10000)

def main():
    # The board is fixed (rows 0..5 correspond to chess rows 1..6, with row0 = a1,...)
    # Board layout (each inner list is a row; row0 is bottom (row1) and row5 is top (row6)):
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
    
    # Pre-calculate knight moves for each square.
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

    # The scoring rule: starting score is A (the integer assigned to letter A).
    # Then, for each knight move from square X to square Y:
    #    if the two squares’ letters are the same, add (value of Y) to the current score;
    #    if different, multiply the current score by (value of Y).
    def update_score(score, from_pos, to_pos, vals):
        # from_pos and to_pos are (row, col). Look up letters in board.
        letter_from = board[from_pos[0]][from_pos[1]]
        letter_to   = board[to_pos[0]][to_pos[1]]
        if letter_from == letter_to:
            return score + vals[letter_to]
        else:
            return score * vals[letter_to]

    # DFS search for a knight path (without revisiting squares) from pos to target.
    # 'score' is the current score; 'path' is the list of positions visited.
    def dfs(pos, target, score, path, visited, vals):
        # Prune if score already exceeds 2024.
        if score > 2024:
            return None
        # If we reached the target, check the score.
        if pos == target:
            if score == 2024:
                return list(path)
            else:
                return None
        # Try all knight moves from current position.
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

    # Convert a board coordinate (r, c) to chess notation (e.g. (0,0) -> "a1")
    def coord_to_str(pos):
        r, c = pos
        return chr(ord('a') + c) + str(r + 1)

    best_solution = None
    best_sum = float('inf')
    # Loop over assignments for A, B, and C (distinct positive integers with sum < 50)
    for A_val in range(1, 50):
        for B_val in range(1, 50):
            if B_val == A_val:
                continue
            for C_val in range(1, 50):
                if C_val == A_val or C_val == B_val:
                    continue
                if A_val + B_val + C_val >= 50:
                    continue
                vals = {'A': A_val, 'B': B_val, 'C': C_val}
                
                # First tour: from a1 to f6.
                # a1 is at (0,0); f6 is at (5,5) because row index + 1 = row number.
                start1, target1 = (0, 0), (5, 5)
                visited1 = {start1}
                path1 = [start1]
                sol1 = dfs(start1, target1, vals['A'], path1, visited1, vals)
                if sol1 is None:
                    continue

                # Second tour: from a6 to f1.
                # a6 is (5,0) [row5, col0] and f1 is (0,5) [row0, col5].
                start2, target2 = (5, 0), (0, 5)
                visited2 = {start2}
                path2 = [start2]
                sol2 = dfs(start2, target2, vals['A'], path2, visited2, vals)
                if sol2 is None:
                    continue

                current_sum = A_val + B_val + C_val
                if current_sum < best_sum:
                    best_solution = (A_val, B_val, C_val, sol1, sol2)
                    best_sum = current_sum
                    print(f"Found solution with A+B+C = {best_sum}: A={A_val}, B={B_val}, C={C_val}")
                    # If you want the very first (minimal) solution, uncomment the next line:
                    # goto DONE
    # If a solution was found, format and print the final answer.
    if best_solution:
        A_val, B_val, C_val, sol1, sol2 = best_solution
        tour1_str = ",".join(coord_to_str(pos) for pos in sol1)
        tour2_str = ",".join(coord_to_str(pos) for pos in sol2)
        # Final answer: first the values for A, B, C, then the a1-to-f6 tour, then the a6-to-f1 tour.
        output = f"{A_val},{B_val},{C_val},{tour1_str},{tour2_str}"
        print("Solution:")
        print(output)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
