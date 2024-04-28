import math
EMPTY = None

HORIZONTAL = "HOR"
VERTICAL = "VER"

class CrosswordGrid:
    def __init__(self, initial):
        self.placed_words = []
        self.grid = [[EMPTY for _ in range(initial)] for _ in range(initial)]

    def display(self):
        for row in self.grid:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
    
    def find_char(self, char):
        """
        Return a tuple with location of the first occurence of char in grid
        (row, col) if present, else return None
        """
        for row_i, row in enumerate(self.grid):
            for col_i, cell in enumerate(row):
                if char == cell:
                    return (row_i, col_i)
        return None
    
    def place_word(self, word, row, col, direction):
        self.placed_words.append(word)
        if direction == HORIZONTAL:
            for i, letter in enumerate(word):
                self.grid[row][col + i] = letter
        elif direction == VERTICAL:
            for i, letter in enumerate(word):
                self.grid[row + i][col] = letter

    def can_place_verticaly(self, word, row, col):
        if row < 0 or col < 0:
            return False
        # word fits in the grid
        if row + len(word) >= len(self.grid):
            return False
        
        for i, letter in enumerate(word):
            # there are no conflicting characters on the cells word will occupy
            if self.grid[row + i][col] not in [None, letter]:
                return False

        return True
    
    def can_place_horizontally(self, word, row, col):
        if row < 0 or col < 0:
            return False
        if col + len(word) >= len(self.grid):
            return False
        for i, letter in enumerate(word):
            if self.grid[row][col + i] not in [None, letter]:
                return False
        return True

    def get_center_placement(self, word, direction):
        center_col = center_row = math.floor(len(self.grid)/2)
        if direction == HORIZONTAL:
            col_offset = math.floor(len(word)/2)
            return (center_row, center_col - col_offset)
        if direction == VERTICAL:
            row_offset = math.floor(len(word)/2)
            return (center_row-row_offset, center_col)
        
    def trim(self):
        # Find the range of rows and columns with non-empty cells
        min_row = min_col = float('inf')
        max_row = max_col = float('-inf')
        for row_i, row in enumerate(self.grid):
            for col_i, cell in enumerate(row):
                if cell is not None:
                    min_row = min(min_row, row_i)
                    max_row = max(max_row, row_i)
                    min_col = min(min_col, col_i)
                    max_col = max(max_col, col_i)

        # Create a new trimmed grid
        trimmed_grid = []
        for row in self.grid[min_row:max_row + 1]:
            trimmed_grid.append(row[min_col:max_col + 1])

        # Update the grid attribute
        self.grid = trimmed_grid
    


test = CrosswordGrid(25)

(row, col) = test.get_center_placement("proletariado", HORIZONTAL)
print(row, col)
test.place_word("proletariado", row, col, HORIZONTAL)
test.display()