import itertools
import random
from functools import reduce


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # add cell to moves_made
        self.moves_made.add(cell)
        print(f"move {cell} added to moves made")
        # mark cell as safe
        self.mark_safe(cell)

        # create new sentence for move

        # find neighbouring cells that are not save or made moves
        neighbours = set()
        (i, j) = cell
        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if col in range(0, self.width) and row in range(0, self.height):
                    if (row, col) != (i, j) and (row, col) not in self.moves_made and (row, col) not in self.safes:
                        neighbours.add((row, col))
        # create a new sentence and add it to knowledge
        new_sentence = Sentence(neighbours, count)
        # mark mines in new sentence
        for m in self.mines:
            new_sentence.mark_mine(m)
        self.knowledge.append(new_sentence)
        
        # update existing sentences
        def update_existing_knowledge():           
            new_information = True
            while new_information:
                new_information = False
                for sentence in self.knowledge:
                    if len(sentence.known_safes()) > 0:
                        for c in list(sentence.known_safes()): 
                            self.mark_safe(c)
                        new_information = True
                    if len(sentence.known_mines()) > 0:
                        for c in list(sentence.known_mines()): 
                            self.mark_mine(c)
                        new_information = True
                # remove empty sentences
                self.knowledge = filter(lambda x: len(x.cells) > 0, self.knowledge)
                # remove repeated sentences
                self.knowledge = reduce(lambda x, y: x + [y] if y not in x else x, self.knowledge, [])
        
        update_existing_knowledge()

        # deduce new information from existing sentences
        new_knowledge = []
        # loop through every combination of sentences looking for subsets
        for sentence_a in self.knowledge:
            for sentence_b in self.knowledge:
                if sentence_a != sentence_b:
                    if sentence_a.cells.issuperset(sentence_b.cells):
                        leftover_cells = sentence_a.cells.difference(sentence_b.cells)
                        leftover_count = sentence_a.count - sentence_b.count
                        new_knowledge.append(Sentence(leftover_cells, leftover_count))
        # add new information to knowledge
        self.knowledge = self.knowledge + new_knowledge
        
        # update again with new information
        update_existing_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_options = self.safes.difference(self.moves_made)
        if len(safe_options) > 0:
            return safe_options.pop()
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        options = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    options.add((i,j))
        return options.pop()
