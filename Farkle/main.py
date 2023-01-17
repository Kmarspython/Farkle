import pygame as p

WIDTH = HEIGHT = 600
DICE_SIZE = HEIGHT // 13
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100
MAX_FPS = 15
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
    myfont = p.font.SysFont("Comic Sans MS", 30)
    running = True
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("Light Blue"))
    clock = p.time.Clock()
    board = ["d1", "d2", "d3", "d4", "d5"]
    roll_color = p.Color("Green")
    keep_color = p.Color("Green")
    load_images()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    if len(board) < 6:
                        board.append("d1")
                elif e.key == p.K_n:
                    if len(board) != 0:
                        board.pop()
                elif e.key == p.K_h:
                    roll_color = p.Color("Gray") if roll_color == p.Color("Green") else p.Color("Green")
        screen.fill(p.Color("Light Blue"))
        draw_dice(board, screen)
        roll, roll_text = create_button(screen, roll_color, BUTTON_WIDTH, BUTTON_HEIGHT,
                      (WIDTH // 2) - BUTTON_WIDTH // 2 - BUTTON_WIDTH * .75, (HEIGHT // 2) - BUTTON_HEIGHT // 2 - 25,
                      myfont, "Roll", p.Color("Black"))
        keep, keep_text = create_button(screen, keep_color, BUTTON_WIDTH, BUTTON_HEIGHT,
                      (WIDTH // 2) - BUTTON_WIDTH // 2 + BUTTON_WIDTH * .75, (HEIGHT // 2) - BUTTON_HEIGHT // 2 - 25,
                      myfont, "Keep", p.Color("Black"))
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_dice(board, screen):
    """Draws the dice to the screen with any number of dice from 1 to 6"""
    for r in range(len(board)):
        dice = board[r]
        onetotwo = {1:2, 2:1, 0:0, 3:0}
        x1 = 0 if len(board) >= 3 else len(board)
        y = (4 // 2 - 1) * DICE_SIZE if r <= 2 else (8 // 2 - 1) * DICE_SIZE
        x = ((2 * r + 4) * DICE_SIZE) + (DICE_SIZE * onetotwo[x1]) if r <= 2 else ((2 * (r - 3) + 4) * DICE_SIZE) +(DICE_SIZE * onetotwo[len(board) - 3])
        p.draw.rect(screen, p.Color("Light Blue"), p.Rect((x, y, DICE_SIZE, DICE_SIZE)))
        screen.blit(IMAGES[dice], p.Rect((x, y, DICE_SIZE, DICE_SIZE)))

def create_button(screen, button_color, button_width, button_height, button_x, button_y, font, text, text_color):
    font_surf = font.render(text, False, text_color)
    font_width, font_height = font_surf.get_size()
    return p.draw.rect(screen, button_color, [button_x, button_y, button_width, BUTTON_HEIGHT]), screen.blit(font_surf, ((button_x + (button_width - font_width) / 2), button_y + (button_height - font_height) / 2))

if __name__ == "__main__":
    main()


