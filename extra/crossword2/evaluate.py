class CrosswordEval: 
    def __init__(self) -> None:
        pass

    def score_tile(self, tile):
        # if tile has letter
            # if tile is part of a cross -> highest score
            # if tile is part of a block -> lowest score

        pass

    def evaluate(self, grid):

        pass
def score_square(row, col, grid):
    diagonals = [
                    grid[row - 1][col - 1],  # Up-Left
                    grid[row - 1][col + 1],  # Up-Right
                    grid[row + 1][col - 1],  # Down-Left
                    grid[row + 1][col + 1]   # Down-Right
                ]
    horizontal = [
        grid[row-1][col],
        grid[row+1][col]
    ]
    vertical = [
        grid[row][col-1],
        grid[row][col+1]
    ]
    if grid[row][col] and any(horizontal) and any(vertical):
        pass #is intersection
    
    if grid[row][col] and (any(horizontal) or any(vertical)) and any(diagonals):
        pass # is some kind of cluster




def score_grid_2(grid):
    diagonal_penalty = 0
    empty_squares = 0
    total_squares = 0

    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            total_squares += 1
            if grid[row][col] is None:
                empty_squares += 1

            if grid[row][col] is not None:
                diagonals = [
                    grid[row - 1][col - 1],  # Up-Left
                    grid[row - 1][col + 1],  # Up-Right
                    grid[row + 1][col - 1],  # Down-Left
                    grid[row + 1][col + 1]   # Down-Right
                ]
                

def score_grid(grid):
    intentional_intersections_score = 0
    unintentional_clusters_penalty = 0

    # Intentional Intersections Score
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            if grid[row][col] is not None:
                neighbors = [
                    grid[row - 1][col],  # Up
                    grid[row + 1][col],  # Down
                    grid[row][col - 1],  # Left
                    grid[row][col + 1]   # Right
                ]
                diagonals = [
                    grid[row - 1][col - 1],  # Up-Left
                    grid[row - 1][col + 1],  # Up-Right
                    grid[row + 1][col - 1],  # Down-Left
                    grid[row + 1][col + 1]   # Down-Right
                ]
                if all(neighbor is not None for neighbor in neighbors) and all(diagonal is None for diagonal in diagonals):
                    intentional_intersections_score += 1

    # Unintentional Clusters Penalty
    for row in range(len(grid)):
        letter_cluster_length = 0
        for col in range(len(grid[row])):
            if grid[row][col] is not None:
                letter_cluster_length += 1
            elif letter_cluster_length > 1:
                unintentional_clusters_penalty += letter_cluster_length
                letter_cluster_length = 0
        if letter_cluster_length > 1:
            unintentional_clusters_penalty += letter_cluster_length

    # Combine scores with appropriate weights
    overall_score = 5*(intentional_intersections_score) - (unintentional_clusters_penalty)
    return overall_score
