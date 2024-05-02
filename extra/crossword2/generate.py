from random import shuffle
from crossword import CrosswordGrid, VERTICAL, HORIZONTAL

class CrosswordBuilder:
    def __init__(self, words:list, grid_size:int) -> None:
        words.sort(key= lambda w: len(w), reverse=True )
        self.words = words
        self.grid_size = grid_size
        self.grid = None

    def __str__(self):
        return f"crossword generator({self.grid_size}): {self.words}"
    
    def try_to_place(self, word, overlap_col, overlap_row, overlap_index):
        (row, col) = get_absolute_placement(overlap_col, overlap_row, overlap_index, HORIZONTAL)
        if self.grid.can_place_horizontal(word, row, col):
            self.grid.place_word(word, row, col, HORIZONTAL)
            return True
        else:
            # try vertical placement
            (row, col) = get_absolute_placement(overlap_col, overlap_row, overlap_index, VERTICAL)
            if self.grid.can_place_vertical(word, row, col):
                self.grid.place_word(word, row, col, VERTICAL)
                return True
        return False
    
    def iterative_placement(self):
        queue = self.words.copy()
        self.grid = CrosswordGrid(self.grid_size)
        # place first word at the center of the grid
        first_word = queue.pop(0)
        (row,col) = self.grid.get_center_placement(first_word, HORIZONTAL)
        self.grid.place_word(first_word, row, col, HORIZONTAL)
        
        shuffle(queue)
        # limit iteration count to twice the len of words
        max_iterations = 2 * len(queue)
        iteration_count = 0

        while iteration_count < max_iterations and len(queue) != 0:
            iteration_count += 1
            placed = False
            word = queue.pop(0)
            for index, char in enumerate(word):
                match = self.grid.find_char(char)
                if match:
                    placed = self.try_to_place(word, match[0], match[1], index)
                    if placed:
                        break
            if not placed:
                queue.append(word)
        if len(queue):
            return False
        else:
            self.grid.trim()
            return self.grid

    def save(self, filename):
        self.grid.trim()
        text_rows = []
        for row in self.grid.grid:
            text_rows.append([char or " " for char in row])

        with open(f"./{filename}", "w") as txt_file:
            txt_file.writelines([" ".join(row)+"\n" for row in text_rows])

def get_absolute_placement(overlap_col, overlap_row, overlap_index, direction):
    if direction == VERTICAL:
        return (overlap_col - overlap_index, overlap_row)
    else:
        return (overlap_col, overlap_row-overlap_index)

MAX_WORDS = 25
MIN_WORDS = 2

def validate_wordlist(word_list):
    """
    Return True if word_list is valid, else false.
    A word_list is valid if 
    - it has more than MIN_WORDS and less than MAX_WORDS
    - each word has at least one char in common with another word.
    """
    # length is within range
    if len(word_list) < MIN_WORDS or len(word_list) > MAX_WORDS:
        return False
    
    # words should have at least one char in common with another word
    for i, word1 in enumerate(word_list):
        found_common = False
        for j, word2 in enumerate(word_list):
            if i != j:  # Skip comparing the word with itself
                if any(char in word2 for char in word1):
                    found_common = True
                    break
        if not found_common:
            print(f"word '{word1}' has no characters in common with other words")
            return False
    return True

class CrosswordGenerator:
    """
    Use CrosswordBuilder and internal settings to generate valid crossword-grids.
    """
    def __init__(self, words, attempts, min_options, max_grid_size):
        """
        - attempts: how many chances the same builder has to try to generate a valid puzzle
        - min_options: the least amount of grids to collect before scoring the puzzles
        - max_grid_size: how large can the grid be. This number will also determine the threshold
        for a failure in generating a valid grid. 
        """
        
        if not validate_wordlist(words):
            raise ValueError("word list is not valid")
        
        words.sort(key=lambda w: len(w), reverse=True)
        longest = len(words[0])
        
        self.grid_size = longest + 2 # initial grid size
        self.words = words
        self.attempts = attempts

        self.grids = [] # collection of successfully generated grids

        self.min_options = min_options
        self.max_grid_size = max_grid_size
        self.failure_count = 0 # number of times Builder has returned false
        self.success_count = 0 # number of times a Grid has been generated == len(self.grids)


    def generate(self):
        """
        Generate at least min_options of valid puzzles (a valid puzzle is one that contains all words in word-list)
        and store them in self.grids.

        Tries to generate a valid puzzle self.attempt times 
        starting from the smallest grid-size(as defined in the init method)
        if not enough valid puzzles were generated, grid_size is incremented untill max_grid_size

        #TBD : In many scenarios(eg: max_grid_size is close to largest word length) it is possible that no valid grid can be generated 
        and there is no error catch implemented to handle this.
        
        """
        while len(self.grids) < self.min_options:
            builder = CrosswordBuilder(self.words, self.grid_size)
            print("\n-------\n", builder)
            for i in range(self.attempts):
                print("\ngenerate attempt ", i)
                grid = builder.iterative_placement()
                if not grid:
                    self.failure_count += 1
                else:
                    self.success_count += 1
                    self.grids.append(grid)
            self.grid_size += 2
            if self.grid_size > self.max_grid_size:
                return

        for grid in self.grids:
            grid.display()
    
