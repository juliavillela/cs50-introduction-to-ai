import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var  in self.domains:
            words = self.domains[var].copy()
            for w in words:
                if len(w) is not var.length:
                    self.domains[var].remove(w)
        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        # if x and y variables share a square
        # intersecting char must be the same
        overlap = self.crossword.overlaps[x,y]
        if overlap:
            # all possible words for y
            options_for_y = self.domains[y]
            overlap_i = overlap[1]
            # all possible characters for y in overlapping square
            overlap_char = set([word[overlap_i] for word in options_for_y])
            
            # filter out of x.domain the words that don't match one of the possible overlapping chars
            overlap_j = overlap[0]
            options = self.domains[x].copy()
            for word in options:
                if word[overlap_j] not in overlap_char:
                    self.domains[x].remove(word)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs or []
        
        if arcs is None:
            for var in self.domains:
                neighbors = self.crossword.neighbors(var)
                for n in neighbors:
                    queue.append((var, n))

        while len(queue):
            # deque from index 0
            (x,y) = queue.pop(0)
            revise = self.revise(x, y)
            if revise:
                # check if there are still viable options in x
                options = self.domains[x]
                if len(options) == 0:
                    return False
                # because value of x has been revised
                # add other neighbors to queue
                other_neighbors = list(self.crossword.neighbors(x))
                # y has already been taken into account, so no need to add it to the queue
                other_neighbors.remove(y)
                for n in other_neighbors:
                    queue.append((n, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            # all variables are present in dictionary
            if var not in assignment:
                return False
            # and each of them corresponds to truthy value
            if not assignment[var]:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # all words are different
        words = list(assignment.values())
        word_set = set(words)
        if len(word_set) != len(words):
            return False
        
        for var, word in assignment.items():
            # all words fit within their variable
            if var.length != len(word):
                return False
            
            # there are no conflicts between neighbors
            neighbors = self.crossword.neighbors(var)
            for n in neighbors:
                if n in assignment:
                    # assumes overlap will return a tuple, not None because 
                    # variables are known to be neighbors
                    (var_overlap, n_overlap) = self.crossword.overlaps[var, n]
                    # both chars should be the same
                    if assignment[var][var_overlap] != assignment[n][n_overlap]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def count_eliminated_options(word):
            """
            Return an integer representing how many words would be eliminated
            in all neighbors' domains if this word is assigned to variable var
            """
            eliminated_word_count = 0
            # go through each neigbour to calculate how many options 
            # would be eliminated by assining value word to variable var
            for neighbor in self.crossword.neighbors(var):
                initial_options  = list(self.domains[neighbor])
                (var_overlap, n_overlap) = self.crossword.overlaps[var,neighbor]
                # filter out the words in domain where intersecting characters do not match
                end_options = list(filter(lambda x: x[n_overlap] == word[var_overlap], initial_options))
                # add difference to eliminated_word_count
                eliminated_word_count += len(initial_options) - len(end_options)
            return eliminated_word_count
        
        ordered_words = list(self.domains[var])
        ordered_words.sort(key = count_eliminated_options)
        return ordered_words

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [var for var in self.domains if var not in assignment]
        if len(unassigned) == 1:
            return unassigned[0]
        # sort from shortest to longest domain
        unassigned.sort(key = lambda x: len(self.domains[x]))
        # if not tie return shortest domain
        if len(self.domains[unassigned[0]]) != len(self.domains[unassigned[1]]):
            return unassigned[0] 
        # if there is a tie
        unassigned  = [unassigned[0], unassigned[1]]
        # sort by degree (number of neighbors)
        unassigned.sort(key = lambda x: len(self.crossword.neighbors(x)))
        
        return unassigned[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if assignment complete:
        if self.assignment_complete(assignment):
            return assignment
        
        else:
            # select optmized next variable
            var = self.select_unassigned_variable(assignment)
            # get optimized ordered words list
            words = self.order_domain_values(var, assignment)

            for word in words:
                # if value consistent with assignment:
                # assing value to variable
                test_assignement = assignment.copy()
                test_assignement[var] = word
                if self.consistent(test_assignement):
                    # continue working on the possiblity of this assignement
                    result =  self.backtrack(test_assignement)
                    # maintain arc-consistency for arcs that concert variable var
                    arcs = [(n, var) for n in self.crossword.neighbors(var)]
                    success = self.ac3(arcs)
                    if success:
                        return result
            # failure-case could not find a solution
            return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
