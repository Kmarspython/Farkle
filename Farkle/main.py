import pygame as p
import random
from Points import *

WIDTH = HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)
DICE_SIZE = HEIGHT // 13
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100
MAX_FPS = 30
IMAGES = {}


def load_images():

    """Loading in images and putting them in the IMAGES dictionary"""

    dice_sprites = ["d1", "d2", "d3", "d4", "d5", "d6"]
    for dice in dice_sprites:
        IMAGES[dice] = p.transform.scale(p.image.load("Farkle/Images/" + dice + ".png"), (DICE_SIZE, DICE_SIZE))


def main():
    """The main loop for the program to run in"""

    # Initialize pygame and font
    p.init()
    p.font.init()
    # Create one font for the button text and a slightly bigger font when the buttons inflate
    my_font = p.font.SysFont("calibri", 30)
    big_font = p.font.SysFont("calibri", 40)
    # Flag for the game loop to run
    running = True
    # Create the screen and clock
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("Light Blue"))
    clock = p.time.Clock()
    # Create the list of the upper dice and the lower dice
    board1 = ["d1", "d1", "d1", "d1", "d1", "d1"]
    board2 = []
    # List of dice that have been selected
    selected_dice = []
    # Rectangles of the dice in board1 to know if they have been clicked
    board1_rects = []
    # List that tells witch dice in board1 should be highlighted
    highlighted_dice = [False, False, False, False, False, False]
    # Initialize the rectangles for the three buttons
    roll = p.Rect(0, 0, 0, 0)
    keep = p.Rect(0, 0, 0, 0)
    done = p.Rect(0, 0, 0, 0)
    # Loading in images
    load_images()
    # Flags that tell if buttons are pressable
    can_roll = True
    can_done = False
    can_select = False
    # Flag to know if the player has farkled
    farkled = False
    # Total accumulated points for the round
    total_points = 0
    # The previous rounds points
    previous_points = 0
    while running:
        # Get the mouse position
        pos = p.mouse.get_pos()
        # Determine if the currently selected dice are able to be scored
        can_keep, points = keeping(selected_dice, one_combos, two_combos, three_combos, four_combos, five_combos, six_combos)
        # Determines the color of each button based on the button flags
        keep_color = p.Color("green") if can_keep == True else p.Color("gray")
        roll_color = p.Color("green") if can_roll == True else p.Color("gray")
        done_color = p.Color("green") if can_done == True else p.Color("gray")
        # Loop that handles all of the clicks
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                # Only can press these buttons if the player has not farkled
                if farkled == False:
                    # Determines if mouse is on the roll button and the player is allowed to roll
                    if button_collision(roll, pos) and can_roll:
                        # This resets the board if all dice are on the lower board
                        if len(board1) == 0:
                            board2 = []
                            board1 = ["d1"] * 6
                        # Randomizes the top board
                        randomize(board1)
                        # So the player cannot roll twice in a roll without scoring dice
                        can_roll = False
                        # Now the player can start selecting dice
                        can_select = True
                        # Resets the highlighted dice list and the selected dice list
                        highlighted_dice = [False] * len(board1)
                        selected_dice = []
                        # You cannot click the done button until you score points on this roll
                        can_done = False
                        # Determines if the player has farkled and changes the flags
                        if has_farkled(super_list(board1)):
                            farkled = True
                            can_done = True
                    # This allows you to select the dice if the flag is true
                    if can_select == True:
                        select_dice(pos, board1_rects, highlighted_dice, selected_dice, board1)
                    # Determines if the mouse is over the keep button and it is selectable
                    if button_collision(keep, pos) and can_keep == True:
                        # Add the selected dice to the bottom board
                        board2 += selected_dice
                        # This gets rid of the selected dice from the top board
                        for r in range(len(highlighted_dice)):
                            if highlighted_dice[r] == True:
                                board1[r] = "remove"
                        board1 = [i for i in board1 if i != "remove"]
                        # Adds the scored points to the total points
                        total_points += points
                        # Resets the highlighted dice list and the selected dice list
                        highlighted_dice = [False] * len(board1)
                        selected_dice = []
                        # Now the player can roll again or be done
                        can_roll = True
                        can_done = True
                # Determines if the mouse is on the done button and it is selectable
                if button_collision(done, pos) and can_done:
                    # Sets points to 0
                    points = 0
                    # If the player has farkled they get no points
                    if farkled == True:
                        previous_points = 0
                        total_points = 0
                    # If the player has not farkled then they get to score the points and it is displayed as previous points
                    else:
                        previous_points = total_points
                        total_points = 0
                    # Resets everything to what it was at the beginning
                    farkled = False
                    can_roll = True
                    can_select = False
                    can_keep = False
                    can_done = False
                    selected_dice = []
                    board1 = ["d1", "d1", "d1", "d1", "d1", "d1"]
                    board2 = []
                    highlighted_dice = [False] * 6
        # Fills the screen
        screen.fill(p.Color("Light Blue"))
        # Draws the dice and stores the rectangles in board1 rects
        board1_rects = draw_dice(board1, board2, screen)
        # Highlights the appropriate dice
        highlight_dice(screen, highlighted_dice, board1_rects)
        # These flags determine if the buttons are inflated or not
        roll_inflate = True if button_collision(roll, pos) and can_roll == True else False
        keep_inflate = True if button_collision(keep, pos) and can_keep == True else False
        done_inflate = True if button_collision(done, pos) and can_done == True else False
        # Creates the roll button
        roll = create_button(screen, my_font, big_font, "Roll", p.Color("black"), (CENTER[0] - 75, CENTER[1] - 50),
                                            BUTTON_WIDTH, BUTTON_HEIGHT, roll_color, roll_inflate)
        # Creates the keep button
        keep = create_button(screen, my_font, big_font, "Keep", p.Color("black"), (CENTER[0] + 75, CENTER[1] - 50),
                                            BUTTON_WIDTH, BUTTON_HEIGHT, keep_color, keep_inflate)
        # Creates the done button
        done = create_button(screen, my_font, big_font, "Done", p.Color("black"), (CENTER[0], HEIGHT - 50),
                             BUTTON_WIDTH, BUTTON_HEIGHT, done_color, done_inflate)
        # Creates the texts on the screen
        create_text(screen, f"Points: {str(points)}", my_font, p.Color("Red"), (WIDTH - 80, 20))
        create_text(screen, f"Points: {str(total_points)}", my_font, p.Color("Red"), (WIDTH - 80, HEIGHT // 2 + 20))
        create_text(screen, f"Previous Points: {str(previous_points)}", my_font, p.Color("Red"), (140, HEIGHT // 2 + 20))
        if farkled == True:
            create_text(screen, "Farkle!", my_font, p.Color("black"), (WIDTH // 2, HEIGHT // 4 + 60))
        # Determines frame rate and updates the screen
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_dice(board1, board2, screen):

    """Draws the dice to the screen with any number of dice from 1 to 6"""

    # Dictionary that helps with the placement of the dice
    onetotwo = {1: 2, 2: 1, 0: 0, 3: 0}
    dice_list = []
    # Draws the top dice to the screen
    for r in range(len(board1)):
        dice = board1[r]
        x1 = 0 if len(board1) >= 3 else len(board1)
        y = DICE_SIZE if r <= 2 else 3 * DICE_SIZE
        x = ((2 * r + 4) * DICE_SIZE) + (DICE_SIZE * onetotwo[x1]) if r <= 2 else ((2 * (r - 3) + 4) * DICE_SIZE) +(DICE_SIZE * onetotwo[len(board1) - 3])
        dice_list.append(p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
        screen.blit(IMAGES[dice], p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
    # Draws the bottom dice to the screen
    for r in range(len(board2)):
        dice = board2[r]
        x1 = 0 if len(board2) >= 3 else len(board2)
        y = 8 * DICE_SIZE if r <= 2 else 10 * DICE_SIZE
        x = ((2 * r + 4) * DICE_SIZE) + (DICE_SIZE * onetotwo[x1]) if r <= 2 else ((2 * (r - 3) + 4) * DICE_SIZE) + (
                    DICE_SIZE * onetotwo[len(board2) - 3])
        p.draw.rect(screen, p.Color("Light Blue"), p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
        screen.blit(IMAGES[dice], p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
    return dice_list

def create_button(screen, font, big_font, text, text_color, button_center, button_width, button_height, button_color, inflate):
    """Creates a button centered at a point with a font rect in the middle"""
    font_surf = font.render(text, False, text_color) if not inflate else big_font.render(text, False, text_color)
    font_width, font_height = font_surf.get_size()
    offset = 15 if inflate else 0
    button_rect = p.Rect.inflate(p.Rect(0, 0, button_width, button_height), offset, offset)
    button_rect.center = button_center
    p.draw.rect(screen, button_color, button_rect)
    font_rect = p.Rect(0, 0, font_width, font_height)
    font_rect.center = button_rect.center
    screen.blit(font_surf, font_rect)
    return button_rect

def create_text(screen, text, font, color, center):
    """Creates text on the screen"""
    font_surf = font.render(text, False, color)
    font_width, font_height = font_surf.get_size()
    font_rect = p.Rect(0, 0, font_width, font_height)
    font_rect.center = center
    screen.blit(font_surf, font_rect)

def button_collision(rect, mouse):
    """Returns true if mouse is over rect"""
    return True if rect.collidepoint(mouse[0], mouse[1]) else False

def select_dice(mouse, board, highlight, selected_dice, board1):
    """Decide what dice are highlighted"""
    for r in range(len(board)):
        if board[r].collidepoint(mouse[0], mouse[1]):
            highlight[r] = not highlight[r]
            if highlight.count(True) > len(selected_dice):
                selected_dice.append(board1[r])
            else:
                selected_dice.remove(board1[r])

def highlight_dice(screen, highlight_bools, board_rects):
    for r in range(len(highlight_bools)):
        if highlight_bools[r] == True:
            s = p.Surface((DICE_SIZE, DICE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("purple"))
            screen.blit(s, board_rects[r])

def randomize(board):
    """Randomizes the list with d1 through d6"""
    for r in range(len(board)):
        board[r] = f"d{random.randint(1,6)}"

if __name__ == "__main__":
    main()


