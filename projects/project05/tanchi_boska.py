# Author: FILL IN
# Class: COMP 141
# Project: Tanchi Boska
# Pledge: FILL IN
# Description: FILL IN
from cs1.graphics import *
from random import randint


def draw_title():
    # draws the title screen, including the background color, the title, and perhaps a little drawing or logo
    pass


## example. use it if you want, or make your own!
def draw_corn(x, y):
    set_color("yellow")
    draw_filled_oval(x, y, 70, 20)
    set_color("black")
    draw_oval(x, y, 70, 20) # creates an outline
    set_color("green")
    draw_filled_polygon(x - 80, y, x - 50, y - 20, x + 20, y - 30)
    set_color("black")
    draw_polygon(x - 80, y, x - 50, y - 20, x + 20, y - 30) # creates an outline
    set_color("green")
    draw_filled_polygon(x - 80, y, x - 50, y + 20, x + 20, y + 30)
    set_color("black")
    draw_polygon(x - 80, y, x - 50, y + 20, x + 20, y + 30) # creates an outline


## DO NOT MODIFY UNLESS YOU KNOW WHAT YOU'RE DOING
def play_game():
    kernels = int(input("How many kernels will you play with? "))
    white_points = int(input("How many points are white kernels worth? "))
    current_round = 1
    player_1_score = 0
    player_2_score = 0
    while current_round <= 3:
        draw_round(current_round, 0, 0) # display a blank round screen (no kernels)
        draw_scores(player_1_score, player_2_score) # draw_round clears the screen: redraw the scores
        input("Player 1: press Enter to throw kernels. ")
        player_1_score += take_turn(current_round, kernels, white_points) 
        draw_scores(player_1_score, player_2_score) # the scores may change
        input("Player 2: press Enter to throw kernels. ")
        player_2_score += take_turn(current_round, kernels, white_points)
        draw_scores(player_1_score, player_2_score) # the scores may change
        current_round += 1
        input("Press enter to finish the round.")
    if player_1_score > player_2_score:
        return "Player 1"
    elif player_1_score < player_2_score:
        return "Player 2"
    else:
        return "Tie"
## ## ## ## ## ## ## ## ## 


def take_turn(current_round, kernels, white_points):
    # randomly chooses some kernels to be white and the rest to be black

    # calculates the score of the turn
    score = 0
    # draws the round
    
    # returns the score of this turn
    return score


def draw_round(current_round, white_kernels, black_kernels):
    # clears canvas

    # draws the round number at the top

    # draws all the white kernels in one row
    
    # draws all the black kernels in another row

    # hint: see Lab 5 graphics solutions for examples on spacing things using a for loop
    pass


def draw_kernel(x, y, color):
    # draws a single kernel of a given color at x, y
    pass


def draw_scores(score1, score2):
    # draw the scores at the bottom of the screen
    pass


def draw_game_over(winner):
    # clears canvas

    # draws the winner of the game
    pass


## DO NOT MODIFY UNLESS YOU KNOW WHAT YOU'RE DOING
def main():
    open_canvas(500, 200)
    draw_title()
    winner = play_game()
    draw_game_over(winner)
## ## ## ## ## ## ## ## ## 

main()
