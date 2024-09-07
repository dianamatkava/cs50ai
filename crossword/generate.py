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

        for node, words in self.domains.items():
            for word in words.copy():
                if len(word) != node.length:
                    self.domains[node].remove(word)

    def revise(self, x, y) -> bool:
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revise = False
        overlaps = self.crossword.overlaps[x, y]
        for _x in self.domains[x].copy():
            if _x[overlaps[0]] not in [node[overlaps[1]] for node in self.domains[y]]:
                self.domains[x].remove(_x)
                revise = True

        return revise

    def ac3(self, arcs=None) -> bool:
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            arcs = self.get_arcs()

        while len(arcs) > 0:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]):
                    return False
                # for z in self.crossword.neighbors():
        return True

    def get_arcs(self) -> list:
        """Create initial arcs with all possible arcs based on the binary constraints"""

        arcs = []
        for node in self.domains:
            for neighbor in self.crossword.neighbors(node):
                arcs.append((node, neighbor))

        return arcs

    def assignment_complete(self, assignment) -> bool:
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains.keys():
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment) -> bool:
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        status = True

        if len(assignment) < 2:
            return status

        # compare first variable with next
        for var in assignment.keys():
            for var_other in assignment.keys():
                if var == var_other:
                    continue

                # get cross indexes
                indexes = self.crossword.overlaps[var, var_other]
                if not indexes:
                    continue
                else:
                    cross_index_1, cross_index_2 = indexes

                match = []
                for val_index, val in enumerate(assignment[var]):
                    for val_other in assignment[var_other]:
                        try:
                            if val[cross_index_1] != val_other[cross_index_1]:
                                status = False
                            else:
                                match.append(val)
                        except:
                            return False

                    if not match:
                        assignment[var].pop(val_index)

        return status

    def order_domain_values(self, var, assignment) -> list:
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        order_data = {}
        for val in self.domains[var]:

            for other_var in self.crossword.neighbors(var):
                for other_val in self.domains[other_var]:

                    neighbor_index, var_index = self.crossword.overlaps[var, other_var]
                    if val[neighbor_index] != other_val[var_index]:
                        order_data[val] = order_data.get(val, 0) - 1

        return [key for key, value in sorted(order_data.items(), key=lambda item: item[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.x
        """

        unassigned_variables = set(self.domains.keys()) - set(assignment.keys())

        values_num = {}
        for var in unassigned_variables:
            values_num[var] = len(self.domains[var])

        # return the variable with the fewest number of remaining values in its domain.
        return [key for key, value in sorted(values_num.items(), key=lambda value: value[1])][0]

    def backtrack(self, assignment) -> dict | None:
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            if self.consistent(assignment):
                return assignment
            else:
                return None

        variable = self.select_unassigned_variable(assignment)
        domain_values = self.order_domain_values(variable, assignment)
        assignment[variable] = domain_values

        if not self.consistent(assignment):
            del assignment[variable]

        self.backtrack(assignment)


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
    sys.argv.append('./data/structure2.txt')
    sys.argv.append('./data/words2.txt')
    main()
