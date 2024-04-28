from crossword import CrosswordGrid, VERTICAL, HORIZONTAL

class CrosswordGenerator:
    def __init__(self, words:list, grid_size) -> None:
        # words.sort(key= lambda w: len(w), reverse=True )
        self.words = words
        self.grid = CrosswordGrid(grid_size)

    def try_to_place(self, word, overlap_col, overlap_row, overlap_index):
        print("trying to place ", word)
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
        print("could not place", word)
        return False
    
    def iterative_placement(self):
        # place first word
        first_word = self.words.pop(0)
        (row,col) = self.grid.get_center_placement(first_word, HORIZONTAL)
        self.grid.place_word(first_word, row, col, HORIZONTAL)
        self.grid.display()

        while len(self.words):
            word = self.words.pop(0)
            print(word)
            for index, char in enumerate(word):
                match = self.grid.find_char(char)
                if match:
                    placed = self.try_to_place(word, match[0], match[1], index)
                    if placed:
                        self.grid.display()
                        break
        
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

word_list = [
    "scooby",
    "eva",
    "onilda",
    "peido",
    "grude",
    "dengo",
    "mafalda",
    "caneca",
]

word_list_2 = [
    "proletariado",
    "meiosdeproducao",
    "maisvalia",
    "lucro",
    "capital",
    "burguesia",
    "classesocial",
    "tempo",
    "maodeobra",
]

# word_list.extend(word_list_2)
generator = CrosswordGenerator(word_list_2, 18)
generator.iterative_placement()
generator.save("test.txt")