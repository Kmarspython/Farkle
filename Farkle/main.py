import pygame as p
import random

WIDTH = HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)
DICE_SIZE = HEIGHT // 13
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100
MAX_FPS = 30
IMAGES = {}

def load_images():
    """Loading in images and putting them in the IMAGES dictionary"""
    diceSprites = ["d1", "d2", "d3", "d4", "d5", "d6"]
    for dice in diceSprites:
        IMAGES[dice] = p.transform.scale(p.image.load("Farkle/Images/" + dice + ".png"), (DICE_SIZE, DICE_SIZE))

def main():
    """The main loop for the program to run in"""
    p.init()
    p.font.init()
    my_font = p.font.SysFont("calibri", 30)
    big_font = p.font.SysFont("calibri", 40)
    running = True
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("Light Blue"))
    clock = p.time.Clock()
    board1 = ["d1", "d1", "d1", "d1", "d1", "d1"]
    board1_rects = []
    board2 = []
    selected_dice = []
    highlighted_dice = [False, False, False, False, False, False]
    roll_color = p.Color("Green")
    keep_color = p.Color("Green")
    roll = p.Rect(0, 0, 0, 0)
    keep = p.Rect(0, 0, 0, 0)
    roll_inflate = False
    keep_inflate = False
    load_images()
    can_roll = True
    can_select = False
    while running:
        pos = p.mouse.get_pos()
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if button_collision(roll, pos) and can_roll:
                    randomize(board1)
                    can_roll = False
                    can_select = True
                if can_select == True:
                    select_dice(pos, board1_rects, highlighted_dice, selected_dice, board1)
                if button_collision(keep, pos):
                    board2 += selected_dice
                    for r in range(len(highlighted_dice)):
                        if highlighted_dice[r] == True:
                            board1[r] = "remove"
                    board1 = [i for i in board1 if i != "remove"]
                    highlighted_dice = [False] * len(board1)
                    selected_dice = []
                    can_roll = True
                print(highlighted_dice)
                print(selected_dice)
            elif e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    if len(board1) < 6:
                        board1.append(board2.pop())
                        highlighted_dice.append(False)
                elif e.key == p.K_n:
                    if len(board1) != 0:
                        board2.append(board1.pop())
                        highlighted_dice.pop()
                elif e.key == p.K_h:
                    roll_inflate = not roll_inflate
                elif e.key == p.K_g:
                    keep_inflate = not keep_inflate
        screen.fill(p.Color("Light Blue"))
        board1_rects = draw_dice(board1, board2, screen)
        highlight_dice(screen, highlighted_dice, board1_rects)
        roll_inflate = True if button_collision(roll, pos) else False
        keep_inflate = True if button_collision(keep, pos) else False

        roll, roll_text = create_button(screen, my_font, big_font, "Roll", p.Color("black"), (CENTER[0] - 75, CENTER[1] - 25),
                                            BUTTON_WIDTH, BUTTON_HEIGHT, roll_color, roll_inflate)
        keep, keep_text = create_button(screen, my_font, big_font, "Keep", p.Color("black"), (CENTER[0] + 75, CENTER[1] - 25),
                                            BUTTON_WIDTH, BUTTON_HEIGHT, keep_color, keep_inflate)

        clock.tick(MAX_FPS)
        p.display.flip()

def draw_dice(board1, board2, screen):
    """Draws the dice to the screen with any number of dice from 1 to 6"""
    onetotwo = {1: 2, 2: 1, 0: 0, 3: 0}
    dice_list = []
    for r in range(len(board1)):
        dice = board1[r]
        x1 = 0 if len(board1) >= 3 else len(board1)
        y = DICE_SIZE if r <= 2 else 3 * DICE_SIZE
        x = ((2 * r + 4) * DICE_SIZE) + (DICE_SIZE * onetotwo[x1]) if r <= 2 else ((2 * (r - 3) + 4) * DICE_SIZE) +(DICE_SIZE * onetotwo[len(board1) - 3])
        dice_list.append(p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
        p.draw.rect(screen, p.Color("Light Blue"), dice_list[r])
        screen.blit(IMAGES[dice], p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
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
    return button_rect, font_rect

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


