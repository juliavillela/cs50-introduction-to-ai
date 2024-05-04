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
        self.words = {}
        self.grid = [[EMPTY for _ in range(initial)] for _ in range(initial)]

    def place_word(self, word:str, row:int, col:int, direction:str):
        """
        Adds word and position to self.words.
        updates grid to contain word at placement
        as well as necessary padding

        This method does not check if placement is allowed before altering the grid.
        """
        self.words[word] = ((row,col), direction)
        self._place_chars(word, row, col, direction)
        self._pad_word(word, row, col, direction)
        intersections = self._intersections(word, row, col, direction)
        for (row,col) in intersections:
            self._pad_intersection(row, col)
   
    def can_place_vertical(self, word:str, row:int, col:int):
        """
        Return True if word can be placed at position (row,col) vertically, else False.
        The constraints for placement are:
            1. word must fit the grid
            2. word must be preceded and followed by an empty square
            3. word cannot change any of the characters that have already been placed
        """
        if not self._fits_in_grid(word, row, col, VERTICAL):
            return False
        
        # the square before the start of word and after the end of word should be empty
        prev_empty_or_edge = row == 0 or self.grid[row-1][col] in [EMPTY, FILLER]
        next_empty_or_edge = row + len(word) == len(self.grid) or self.grid[row + len(word)][col] in [EMPTY, FILLER]
        if not (prev_empty_or_edge and next_empty_or_edge):
            return False
        
        # there are no conflicting characters on the cells word will occupy
        for i, letter in enumerate(word):     
            if self.grid[row + i][col] not in [EMPTY, letter]:
                return False

        return True
    
    def can_place_horizontal(self, word:str, row:int, col:int):
        """
        Return True if word can be placed at position (row,col) horizontally, else False.
        The constraints for placement are:
            1. word must fit the grid
            2. word must be preceded and followed by an empty square
            3. word cannot change any of the characters that have already been placed
        """
        if not self._fits_in_grid(word, row, col, HORIZONTAL):
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
    
    def get_center_placement(self, word:str, direction:str):
        """
        Return a tuple (row, col) for word placement that results in 
        word being placed as close to the center of the grid as possible.
        """
        if len(word) > len(self.grid):
            raise ValueError(f'word: "{word}" does not fit the grid')
        center_col = center_row = math.floor(len(self.grid)/2)
        if direction == HORIZONTAL:
            col_offset = math.floor(len(word)/2)
            return (center_row, center_col - col_offset)
        if direction == VERTICAL:
            row_offset = math.floor(len(word)/2)
            return (center_row-row_offset, center_col)
    
    def match_many_char(self, char:str):
        """ 
        Return a list of tuples (row,col) with each occurence of char in grid
        """
        positions = []
        for row_i, row in enumerate(self.grid):
            for col_i, cell in enumerate(row):
                if char == cell:
                    positions.append((row_i, col_i))
        return positions
    
    def trim(self):
        """
        Returns a copy of grid where empty columns and empty rows have been removed 
        An empty line is a line where all values == None

        If called on an empty grid: returns empty grid unchanged.
        """
        # Find the range of rows and columns with non-empty cells
        min_row = min_col = 0
        max_row = max_col = len(self.grid)
        for row_i, row in enumerate(self.grid):
            for col_i, cell in enumerate(row):
                if cell is not EMPTY:
                    min_row = min(min_row, row_i)
                    max_row = max(max_row, row_i)
                    min_col = min(min_col, col_i)
                    max_col = max(max_col, col_i)

        # Create a new trimmed grid
        trimmed_grid = []
        for row in self.grid[min_row:max_row + 1]:
            trimmed_grid.append(row[min_col:max_col + 1])

        return trimmed_grid
    
    def display(self):
        """
        Prints visualization of grid to terminal
        """
        for row in self.grid:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
        
    def _place_chars(self, word:str, row:int, col:int, direction:str):
        """
        Updates grid to contain word characters at placement.
        """
        if not self._fits_in_grid(word, row, col, direction):
            raise ValueError(f'word {word} does not fit in grid')
        
        if direction == HORIZONTAL:
            for i, letter in enumerate(word):
                self.grid[row][col + i] = letter

        elif direction == VERTICAL:
            for i, letter in enumerate(word):
                self.grid[row + i][col] = letter

    def _pad_word(self, word:str, row:int, col:int, direction:str):
        """
        Adds FILLER char to start and end of word
        """
        if direction == HORIZONTAL:
            if col > 0:
                self.grid[row][col-1] = FILLER
            if col + len(word) < len(self.grid):
                self.grid[row][col + len(word)] = FILLER

        elif direction == VERTICAL:
            if row > 0:
                self.grid[row-1][col] = FILLER
            if row + len(word) < len(self.grid):
                self.grid[row + len(word)][col] = FILLER
    
    def _pad_intersection(self, row:int, col:int):
        """
        Adds filler char around intersections
        """
        # up-left
        if row > 0 and col > 0 and self.grid[row-1][col-1] == EMPTY:
            self.grid[row-1][col-1] = FILLER
        #up-rigth
        if row > 0 and col < len(self.grid)-1 and self.grid[row-1][col+1] == EMPTY:
            self.grid[row-1][col+1] = FILLER
        #down-left
        if row < len(self.grid)-1 and col > 0 and self.grid[row+1][col-1] == EMPTY:
            self.grid[row+1][col-1] = FILLER
        #down-rigth
        if row < len(self.grid)-1 and col < len(self.grid)-1 and self.grid[row+1][col+1] == EMPTY:
            self.grid[row+1][col+1] = FILLER 
    
    def _fits_in_grid(self, word:str, row:int, col:int, direction:str):
        """
        Returns True if word fits in grid starting at row column,
        in direction = direction, else False.
        """
        if row < 0 or col < 0:
            return False
        
        if direction == VERTICAL:
            if row + len(word) > len(self.grid):
                return False
            
        if direction == HORIZONTAL:
            if col + len(word) > len(self.grid[0]):
                return False
        return True
    
    def _intersections(self, word:str, row:int, col:int, direction:str):
        """
        returns a list of tupples (row,col) - each tuple represents a cell
        where word intersects with another word in the oposing direction.
        """
        def word_range(word,row,col,direction):
            if direction == VERTICAL:
                return [(row + i, col) for i in range(len(word))]
            if direction == HORIZONTAL:
                return [(row, col + i) for i in range(len(word))]
          
        word1_range = word_range(word, row, col, direction)

        if direction == VERTICAL:
            perpendicular = [w for w in self.words if self.words[w][1] == HORIZONTAL]
        else:
            perpendicular = [w for w in self.words if self.words[w][1] == VERTICAL]

        intersections = []

        for word_2 in perpendicular:
            word2_row, word2_col = self.words[word_2][0]
            word2_direction = self.words[word_2][1]
            word2_range = word_range(word_2,word2_row, word2_col, word2_direction)
            for position in word1_range:
                if position in word2_range:
                    intersections.append(position)
        return intersections

    def width(self):
        return len(self.grid[0])
    
    def height(self):
        return len(self.grid)