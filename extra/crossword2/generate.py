from random import shuffle
from crossword import CrosswordGrid, VERTICAL, HORIZONTAL

class CrosswordGenerator:
    def __init__(self, words:list, grid_size:int) -> None:
        words.sort(key= lambda w: len(w), reverse=True )
        self.words = words
        self.grid = CrosswordGrid(grid_size)

    def __str__(self):
        return f"crossword generator: {self.words}"
    def try_to_place(self, word, overlap_col, overlap_row, overlap_index):
        # print("trying to place ", word)
        (row, col) = get_absolute_placement(overlap_col, overlap_row, overlap_index, HORIZONTAL)
        if self.grid.can_place_horizontally(word, row, col):
            self.grid.place_word(word, row, col, HORIZONTAL)
            return True
        else:
            # try vertical placement
            (row, col) = get_absolute_placement(overlap_col, overlap_row, overlap_index, VERTICAL)
            if self.grid.can_place_verticaly(word, row, col):
                self.grid.place_word(word, row, col, VERTICAL)
                return True
        # print("could not place", word)
        return False
    
    def get_next_word(self):
        shuffle(self.words)
        return self.words.pop(0)

    def iterative_placement(self):
        queue = self.words.copy()
        # place first word
        first_word = queue.pop(0)
        (row,col) = self.grid.get_center_placement(first_word, HORIZONTAL)
        self.grid.place_word(first_word, row, col, HORIZONTAL)
        # self.grid.display()

        shuffle(queue)
        max_iterations = 2 * len(queue)
        iteration_count = 0

        while iteration_count < max_iterations and len(queue) != 0:
            iteration_count += 1
            placed = False
            word = queue.pop(0)
            print(word)
            for index, char in enumerate(word):
                match = self.grid.find_char(char)
                if match:
                    placed = self.try_to_place(word, match[0], match[1], index)
                    if placed:
                        # self.grid.display()
                        break
            if not placed:
                queue.append(word)
        if len(queue):
            return False
        else:
            self.grid.trim()
            return self.grid
        # self.grid.display()
        # print("could not place", self.words)
        # print("placed", self.grid.placed_words)

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