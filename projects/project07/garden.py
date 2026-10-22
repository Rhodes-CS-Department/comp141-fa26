# Name:
# Date: 
# Class: 
# Pledge:  
# Description: 

# Returns the number of small plants (*) in this garden.
# garden: a string containing a row of plants.
def count_small(garden):
    pass # remove this line (including the 'pass') when starting to write this function.


# Returns the number of big plants (^) in this garden.
# garden: a string containing a row of plants.
def count_big(garden):
    pass # remove this line (including the 'pass') when starting to write this function.


# Returns the number of dormant plants (.) in this garden.
# garden: a string containing a row of plants.
def count_dormant(garden):
    pass # remove this line (including the 'pass') when starting to write this function.


# Creates the next generation of a garden of Plant A from the current generation.
# garden: a string containing a row of plants.
# Returns a string containing the next generation of the garden.  This string should
# be the same length as the previous generation.
def next_generation_A(garden):
    newgarden = ""   # Use this variable to hold the next generation of the garden.
    
    # Algorithm:  (You can remove all these comments when you're done.)
    # Make a for loop over the garden variable.  Inside the loop:
    #   Examine each character within the string, checking to see if it's alive 
    #   or dormant, and what its left and right neighbors are.
    # 
    #   Use string concatenation to attach a new character (* or .) to 
    #   newgarden that represents the next generation of the current plant.
    
    # Hints and notes: Remember that the far left and far right plants are always
    # dormant. Handle these plants separately since they don't have both neighbors.
    
    return newgarden


# Runs the simulation for plant A for the given number of generations, given a
# starting garden. Note that this function doesn't return anything.
def run_garden_A(garden, generations):
    pass # delete this line when you start writing this function.
    # Algorithm for this simulation:
    #   Count the number of dormant and alive (small) plants in the starting garden.
    #     Do this by calling count_dormant and count_small on the garden.
    #   Print the starting garden, along with the number of dormant and alive plants
    #     (all on the same line).
    #   Call next_generation_A on the current garden to generate the next garden 
    #     (be sure to capture the return value --- that's the next generation!).
    #   Call count_dormant and count_small on the next generation garden.
    #   Again, print the garden and the number of dormant and alive plants.
    #   Put all of this in a loop to print numgens generations, not including the first.
    #     (So if numgens = 30, there will be 31 lines of total output)

    
# Creates the next generation of a garden of Plant B from the current generation.
# garden: a string containing a row of plants.
# nsize: the size of the neighborhood that Plant B will use.
# Returns a string containing the next generation of the garden.  This string should
# be the same length as the previous generation.
def next_generation_B(garden, nsize):
    newgarden = ""   # Use this variable to hold the next generation of the garden.
    
    # Algorithm:  (You can remove all these comments when you're done.)
    # Make a for loop over the garden variable.  Inside the loop:
    #
    #   Use a string slice to calculate the neighborhood garden and save this
    #   into a separate variable.
    #
    #   Call your count_small and count_big functions on the neighborhood to count
    #   the total number of alive plants.
    #
    #   Check if the total number of alive plants is even or odd, figure out
    #   what the next generation of the current plant should be, and concatenate
    #   it to newgarden.
    
    # Hints and notes: Remember that, like for Plant A, the far left and far 
    # right plants are always dormant, but the number of plants on the left
    # and right that stay dormant depend on the neighborhood size.  As before,
    # handle these plants separately inside the loop, since you can't compute
    # a neighborhood for them.

    return newgarden


# Runs the simulation for plant B for the given number of generations, given a
# starting garden. nsize is the size of the neighborhood. 
# Note that this function doesn't return anything.
def run_garden_B(garden, nsize, generations):
    pass # delete this line when you start writing this function.
    # Algorithm for this simulation:
    #   Do the same stuff as for Plant A, but when printing each garden, also 
    #     print the number of dormant, small, and big plants (all on one line).
    

def main():
    ptype = input("Are you growing plant A or B? ")
    garden = input("What is the starting garden? ")
    sidenum = int(input("How many dormant plants are on either side? "))
    numgens = int(input("How many generations do you want to see? (not including the first) "))

    # Write a line of code here using string concatenation to attach the correct 
    # number of dormant plants (periods) to either side of the garden variable.
    # Hint: You can make a string consisting of a certain number of one character
    # by using the * operator.  
    # Example:  
    #    s1 = "A" * 3    # makes a string of 3 A's
    #    s2 = "abc" * 5  # makes the string "abcabcabcabcabc" (5 copies of abc)
    
    # Now, call the correct function based on the plant type and the garden you
    # just created.

    
main()