# Author: FILL IN
# Class: COMP 141
# Project: Image Processing
# Pledge: FILL IN
# Description: FILL IN

from cs1.ppm import display_ppm
from cs1.notebooks import *

# Returns the name of the output file, based on the original file name and the filter.
# original_filename: the name of the original file, like "lynx.ppm".
# filter_num: the number of the filter that was applied (an integer from 1 to 9).
# Examples:
#   make_output_filename("rhodes.ppm", 9) returns "rhodes_grayscale.ppm"
#   make_output_filename("lynx.ppm", 8) returns "lynx_flip_horizontally.ppm"
def make_output_filename(original_filename, filter_num):
    mods = ["negate_red", "negate_green", "negate_blue",
            "negate_all", "remove_red", "remove_green",
            "remove_blue", "flip_horizontally", "grayscale"]
    # Write your code here.

# Returns a new list where each value in lst has been negated.
# To negate a value, subtract it from 255.
# lst: a list of integers.
# Example: negate([1, 2, 3, 200, 100, 150]) returns [254, 253, 252, 55, 155, 105]
def negate(lst):
    pass # remove this line (including the "pass") when you start to write this function.

# Returns a new list of the same length as lst, where every value is 0.
# (To flatten a value, set it equal to 0.)
# lst: a list of integers.
# Example: flatten([1, 2, 3, 200, 100, 150]) returns [0, 0, 0, 0, 0, 0]
def flatten(lst):
    pass # remove this line (including the "pass") when you start to write this function.

# Returns a new list with the values of lst in reverse order.
# lst: a list of integers.
# Example: flip([1, 2, 3, 200, 100, 150]) returns [150, 100, 200, 3, 2, 1]
def flip(lst):
    pass # remove this line (including the "pass") when you start to write this function.

# Returns a new list where each value is the average of the red, green, and blue
# values at the same index.  The averages must be integers, so use // to divide.
# red, green, blue: three lists of integers, all the same length.
# Example: if red[0] is 30, green[0] is 100, and blue[0] is 74, the average is
# (30 + 100 + 74) // 3 = 68, so the returned list has 68 at index 0.
def grayscale(red, green, blue):
    pass # remove this line (including the "pass") when you start to write this function.

# Returns a list of the integer values for one color from one line of a PPM file.
# values: a list of strings from one line of a PPM file.
# start: the index of the first value to use (0 for red, 1 for green, 2 for blue).
# The values on a line go red, green, blue, red, green, blue, and so on.
# Examples, if values is ["255", "0", "10", "0", "128", "20"]:
#   get_channel(values, 0) returns [255, 0]   (the red values)
#   get_channel(values, 1) returns [0, 128]   (the green values)
#   get_channel(values, 2) returns [10, 20]   (the blue values)
# Hint: the values are strings, so use int to convert each one to an integer.
def get_channel(values, start):
    pass # remove this line (including the "pass") when you start to write this function.

# Returns a string with all of the values in a list, each followed by a space,
# so it can be written as one line of a PPM file.
# values: a list of integers.
# Example: make_line([0, 0, 10, 255, 128, 20]) returns "0 0 10 255 128 20 "
# Hint: use str to convert each number to a string before you concatenate it.
def make_line(values):
    pass # remove this line (including the "pass") when you start to write this function.

# Applies a filter to one row of pixels.
# values: a list of strings from one line of a PPM file.
# filter_num: the number of the filter to apply (an integer from 1 to 9).
# Returns a new list of integers with the filter applied, in the same
# red, green, blue, red, green, blue, ... order.
# Example: process_list(["255", "0", "10", "0", "128", "20"], 1) returns [0, 0, 10, 255, 128, 20]
#   (filter 1 is negate red, so only the red values, 255 and 0, changed)
def process_list(values, filter_num):
    pass # remove this line (including the "pass") when you start to write this function.

    # Algorithm:  (You can remove all these comments when you're done.)
    # Use get_channel to get the red, green, and blue lists.
    #
    # Call the right filter function on the right lists for filter_num.  For example,
    # to negate red, call negate on the red list to get the new red list.
    #
    # Put the three lists back together into one new list, in the order red, green,
    # blue, red, green, blue, and so on.  Return the new list.
    #
    # Hints and notes: Work through the example above on paper before you start coding!

# The main function is partly written for you.  You need to add two loops: an input
# validation loop, and a loop that reads the input file and writes the output file.
# The comments below tell you where they go.
def main():
    # get input from user
    input_filename = input("PPM file? ")
    print("Filters:")
    print("1. Negate red")
    print("2. Negate green")
    print("3. Negate blue")
    print("4. Negate all")
    print("5. Remove red")
    print("6. Remove green")
    print("7. Remove blue")
    print("8. Flip horizontally")
    print("9. Grayscale")
    filter_num = int(input("Select a filter: "))

    # Write an input validation loop here, so the user can only enter a filter
    # number from 1 to 9.

    # get output filename
    output_filename = make_output_filename(input_filename, filter_num)

    # open both files
    input_file = open(input_filename, "r")
    output_file = open(output_filename, "w")

    # Write a loop here that reads the input file one line at a time, and writes
    # the new image to the output file.
    #
    # Algorithm:  (You can remove all these comments when you're done.)
    # Make a for loop over the input file.  Inside the loop:
    #   rstrip the line (remove the newline from the end).
    #
    #   The first 3 lines are the header.  Write them to the output file unchanged.
    #
    #   Every line after the header is one row of pixels.  Use process_list and
    #   make_line to write the filtered row to the output file.
    #
    # Hints and notes: line.split(" ") splits a line into a list of strings.  rstrip
    # took the newline off each line you read, so add "\n" to the end of each line
    # you write.  If you're having trouble, try test.ppm with filter 1 first, and
    # compare your output file to the one shown in the notebook.

    # close both files, print filename, and display image
    input_file.close()
    output_file.close()
    print("Output file with filter", filter_num, "applied is named", output_filename)
    display_ppm(output_filename)

main()
