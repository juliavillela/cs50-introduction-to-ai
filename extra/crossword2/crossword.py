import math
from constants import *
from helpers import word_range
class CrosswordGrid:
    """
    Represents a crossword puzzle.

    placed_words is a dict containing all the words that have been placed in the grid
    and their respective position: a tuple of ints (row, col) for the first char in word, 
    and direction: VERTICAL or HORIZONTAL

    grid is a two-dimentional list of rows and columns where each item represents a cell in the puzzle.
    """
    def __init__(self, initial:int):
        """
        Initializes an empty crossword with max width and length equal to initial.
        """
        self.placed_words = {}
        self.grid = [[EMPTY for _ in range(initial)] for _ in range(initial)]

    def display(self):
        """
        Prints visualization of grid to terminal
        """
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
        """
        Adds word and position to placed_words and
        updates grid to contain word at placement.

        This method does not check if placement is allowed before altering the grid.
        """
        self.placed_words[word] = ((row,col), direction)
        
        if direction == HORIZONTAL:
            #pad word start and end
            if col > 0:
                self.grid[row][col-1] = FILLER
            if col + len(word) < len(self.grid):
                self.grid[row][col + len(word)] = FILLER

            for i, letter in enumerate(word):
                self.grid[row][col + i] = letter

        elif direction == VERTICAL:
            if row > 0:
                self.grid[row-1][col] = FILLER
            if row + len(word) < len(self.grid):
                self.grid[row + len(word)][col] = FILLER

            for i, letter in enumerate(word):
                self.grid[row + i][col] = letter
        
        self.display()
        intersections = self.intersections(word, row, col, direction)
        for (row,col) in intersections:
            self.pad_intersection(row, col)
        print("word: ", word, " has intersections: ", intersections)

    def pad_intersection(self, row, col):
        # up-left
        if row > 0 and col > 0 and self.grid[row-1][col-1] == EMPTY:
            self.grid[row-1][col-1] = FILLER
        #up-rigth
        if row > 0 and col < len(self.grid) and self.grid[row-1][col+1] == EMPTY:
            self.grid[row-1][col+1] = FILLER
        #down-left
        if row < len(self.grid) and col > 0 and self.grid[row+1][col-1] == EMPTY:
            self.grid[row+1][col-1] = FILLER
        #down-rigth
        if row < len(self.grid) and col < len(self.grid) and self.grid[row+1][col+1] == EMPTY:
            self.grid[row+1][col+1] = FILLER

    def can_place_vertical(self, word, row, col):
        """
        Return True if word can be placed at position (row,col) vertically, else False.
        The constraints for placement are:
            1. word must fit the grid
            2. word must be preceded and followed by an empty square
            3. word cannot change any of the characters that have already been placed
        """
        # word fits in the grid
        if row < 0 or col < 0:
            return False
        if row + len(word) >= len(self.grid):
            return False
        
        # the square before the start of word and after the end of word should be empty
        prev_empty_or_edge = row == 0 or self.grid[row-1][col] in [EMPTY, FILLER]
        next_empty_or_edge = row + len(word) == len(self.grid) or self.grid[row + len(word)][col] in [EMPTY, FILLER]
        if not (prev_empty_or_edge and next_empty_or_edge):
            return False
        
        # there are no conflicting characters on the cells word will occupy
        for i, letter in enumerate(word):     
            if self.grid[row + i][col] not in [None, letter]:
                return False

        return True
    
    def can_place_horizontal(self, word, row, col):
        """
        Return True if word can be placed at position (row,col) horizontally, else False.
        The constraints for placement are:
            1. word must fit the grid
            2. word must be preceded and followed by an empty square
            3. word cannot change any of the characters that have already been placed
        """
        # word fits in the grid
        if row < 0 or col < 0:
            return False
        if col + len(word) >= len(self.grid):
            return False
        
        # the square before the start of word and after the end of word should be empty
        prev_empty_or_edge = col == 0 or self.grid[row][col-1] in [EMPTY, FILLER]
        next_empty_or_edge = col + len(word) == len(self.grid) or self.grid[row][col + len(word)] in [EMPTY, FILLER]
        if not (prev_empty_or_edge and next_empty_or_edge):
            return False
        
        # there are no conflicting characters on the cells word will occupy
        for i, letter in enumerate(word):
            if self.grid[row][col + i] not in [None, letter]:
                return False
        return True

    def get_center_placement(self, word, direction):
        """
        Return a tuple (row, col) for word placement that results in 
        word being placed as close to the center of the grid as possible.
        """
        center_col = center_row = math.floor(len(self.grid)/2)
        if direction == HORIZONTAL:
            col_offset = math.floor(len(word)/2)
            return (center_row, center_col - col_offset)
        if direction == VERTICAL:
            row_offset = math.floor(len(word)/2)
            return (center_row-row_offset, center_col)

    def trim(self):
        """
        Trims empty columns and empty rows from grid matrix. 
        An empty line is a line where all values == None
        """
        # Find the range of rows and columns with non-empty cells
        min_row = min_col = len(self.grid)
        max_row = max_col = 0
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

    def intersections(self, word, row, col, direction):
        """
        Returns a list of tuples (row,col) where an intersection occurs between word
        and other perpendicular words.
        """
        # set of cells word occupies
        word1_range = word_range(word,row, col, direction)

        # list of perpedicular words to check for intersection
        if direction == VERTICAL:
            perpendicular = [w for w in self.placed_words if self.placed_words[w][1] == HORIZONTAL]
        else:
            perpendicular = [w for w in self.placed_words if self.placed_words[w][1] == VERTICAL]

        # list of intersection cells
        intersections = []

        for word_2 in perpendicular:
            # set ofcells word_2 occupies
            word2_row, word2_col = self.placed_words[word_2][0]
            word2_direction = self.placed_words[word_2][1]
            word2_range = word_range(word_2, word2_row, word2_col, word2_direction)

            intersections.extend(word1_range.intersection(word2_range))

        return intersections
    
    def width(self):
        return len(self.grid[0])
    
    def height(self):
        return len(self.grid)