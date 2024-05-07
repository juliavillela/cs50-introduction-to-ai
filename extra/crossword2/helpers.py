from constants import *

def clean(grid:list[list]):
    """
    Returns a copy of grid matrix where FILLER is replaced with None
    """
    clean_grid = []
    for row in grid:
        clean_row = []
        for cell in row:
            if cell == FILLER:
                clean_row.append(EMPTY)
            else:
                clean_row.append(cell)
        clean_grid.append(clean_row)
    return clean_grid

def trim(grid:list[list]):
    """
    Returns a copy of grid matrix where empty columns and empty rows have been removed 
    An empty line is a line where all values == EMPTY

    If called on an empty grid: returns empty grid unchanged.
    """
    # Find the range of rows and columns with non-empty cells
    # grids are assumed to be square
    min_row = min_col = len(grid)
    max_row = max_col = 0
    for row_i, row in enumerate(grid):
        for col_i, cell in enumerate(row):
            if cell is not EMPTY:
                min_row = min(min_row, row_i)
                max_row = max(max_row, row_i)
                min_col = min(min_col, col_i)
                max_col = max(max_col, col_i)

    # Create a new trimmed grid
    trimmed_grid = []
    for row in grid[min_row:max_row + 1]:
        trimmed_grid.append(row[min_col:max_col + 1])

    return trimmed_grid

def validate_word_list(word_list):
    """
    Raises an error if word list does not meet any of the criteria

    A word_list is valid if:
    - it has more than MIN_WORDS and less than MAX_WORDS.
    - no words in list are either too long or too short
    - each word has at least one char in common with another word.
    """
    # word list is of adequate length
    if len(word_list) > MAX_WORDS or len(word_list) < MIN_WORDS:
        raise ValueError(f"word list should have between {MIN_WORDS} and {MAX_WORDS}, not {len(word_list)}")

    # no words are too long
    too_long = [w for w in word_list if len(w)>MAX_WORD_LEN]
    if len(too_long):
        raise ValueError(f"word list contains words that are longer than {MAX_WORD_LEN}: {too_long}")
    
    # no words are too short
    too_short = [w for w in word_list if len(w)<MIN_WORD_LEN]
    if len(too_short):
        raise ValueError(f"word list contains words that are shorter than {MIN_WORD_LEN}: {too_short}")
    
    # words should have at least one char in common with another word        
    for i, word1 in enumerate(word_list):
        found_common = False
        for j, word2 in enumerate(word_list):
            if i != j:  # Skip comparing the word with itself
                if any(char in word2 for char in word1):
                    found_common = True
                    break
        if not found_common:
            raise ValueError(f"word list is impossible. word '{word1}' has no chars in common with other words")
    
    return True