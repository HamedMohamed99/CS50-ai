import sys
import re

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        for x in self.domains :
            m = self.domains[x].copy()
            for i in m :
                if len(i) != int(str(x)[-2:]) :
                    self.domains[x].remove(i)


        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        if self.crossword.overlaps[x,y] == None :
            return False
        else : 
            words = self.domains[x].copy()
            for word in words :
                checked = 0
                for comp in  self.domains[y] :
                    if word[self.crossword.overlaps[x,y][0]] == comp[self.crossword.overlaps[x,y][1]] :
                        checked = 1

                if checked == 0 :
                    self.domains[x].remove(word)
            return True


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        for loop in range (2) :
            for v in self.crossword.overlaps :
                x = v[0] 
                y = v[1]
                if self.crossword.overlaps[x,y] != None :
                    words = self.domains[x].copy()
                    for word in words :
                        checked = 0
                        for comp in  self.domains[y] :
                            if word[self.crossword.overlaps[x,y][0]] == comp[self.crossword.overlaps[x,y][1]] :
                                checked = 1

                        if checked == 0 :
                            self.domains[x].remove(word)
                            if self.domains[x] == None :
                                return False
    
        return True
        
        
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        check = 0
        for var in assignment.values() :
            if len (var) == 1 :
                check += 1
        if check == len(assignment) :
            return True
        else :
            return False


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment :
            copy1 = assignment[var].copy()
            for word in copy1 :
                for other in  assignment :
                    if assignment[other] != assignment[var]  :
                        copy2 = assignment[other].copy()
                        for other_word in copy2 :
                            if word == other_word :
                                if len(assignment[var]) < len(assignment[other]) :
                                    assignment[other].remove(word)
                                    if assignment[other] == None :
                                        return False
                                else :
                                    assignment[var].remove(word)
                                    if assignment[var] == None :
                                        return False

        return True

       

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        xxx = 0
        m={}
        for v in self.crossword.overlaps :
                if self.crossword.overlaps[v[0],v[1]] != None :
                    words = self.domains[v[0]].copy()
                    for word in words :
                        checked = 0
                        for comp in  self.domains[v[1]] :
                            if word[self.crossword.overlaps[v[0],v[1]][0]] != comp[self.crossword.overlaps[v[0],v[1]][1]] :
                                checked += 1

                        m[word] = checked
                    m = sorted(m.items(), key=lambda x: x[1])
                    
                    wl=[]
                    for new in m :
                        wl.append(new[0])
                    self.domains[v[0]] = wl
                   
                    m={}
                   

                        
            
        varl=[]
        for var in self.domains :
            for v in self.crossword.overlaps :
                if not v[0] in varl :
                    x = v[0] 
                    y = v[1]
                    if self.crossword.overlaps[x,y] != None :
                        words = self.domains[x].copy()
                        for word in words :
                            checked = 0
                            for comp in  self.domains[y] :

                                if word[self.crossword.overlaps[x,y][0]] == comp[self.crossword.overlaps[x,y][1]] :
                                    checked = 1

                            if checked == 0 :
                                self.domains[x].remove(word)

            for var2 in self.domains :
                copy1 = self.domains[var2].copy()
                for word in copy1 :
                    for other in  self.domains :
                        if self.domains[other] != self.domains[var2]  :
                            copy2 = self.domains[other].copy()
                            for other_word in copy2 :
                                if word == other_word :
                                    if len(self.domains[var2]) < len(self.domains[other]) :
                                        self.domains[other].remove(word)
                                        
                                    else :
                                        self.domains[var2].remove(word)
            
            beta = list(self.domains[var])[0]             
            self.domains[var] = []
            self.domains[var].append(beta)
            assignment[var] = beta
            varl.append(var)
            print(xxx)
            xxx += 1

        
        return assignment


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
