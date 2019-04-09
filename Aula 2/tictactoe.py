from pygame.locals import *
from random import choice, shuffle, randint
import pygame
import sys


def random_colour():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    return (r,g,b)

### define some colours
BLACK = random_colour()
WHITE = random_colour()
YELLOW = random_colour()
GRENA = random_colour()
RANDOM = random_colour()
DARK_GRAY = random_colour()

BARWIDTH = 15
SQUARESIZE = 90
MENU_WIDTH = 170
WIDTH = 3*SQUARESIZE + 2*BARWIDTH
HEIGHT = 3*SQUARESIZE + 2*BARWIDTH
_WIDTH = 2*BARWIDTH + 3*SQUARESIZE + MENU_WIDTH
_HEIGHT = 2*BARWIDTH + 3*SQUARESIZE
BUTTONTEXT_COLOUR = GRENA
BUTTONBG_COLOUR = random_colour()
BG_COLOUR = DARK_GRAY
BAR_COLOUR = random_colour()

screen = pygame.display.set_mode((_WIDTH, _HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

class Menu(object):
    """This class will take care of the main menu:
        choosing 1player or 2player mode and the difficulty
        of the 1player mode"""
    def __init__(self, surface, dims):
        """Initialize the GUI elements and save them for later"""
        self.surface = surface
        self.w, self.h = dims

        # initialize the fonts if needed
        if not pygame.font.get_init():
            pygame.font.init()
        # use this for maximum compatibility
        df = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(df, 30)

        # flag the options
        self.players = None
        self.difficulty = None
        # flag the screen we are in; available screens are
        ### player_menu
        ### difficulty_menu
        self.screen = "player_menu"

        ### CREATE ALL BUTTONS
        # x and y paddings between text and button borders
        xbuttonpad = 25
        ybuttonpad = 15
        youterpadding = 25  # minimum distance between two buttons

        ## create the buttons to choose between 1 and 2 players
        # find the text that is wider and use its width
        one_player = self.font.render("1 player", True, BUTTONTEXT_COLOUR)
        two_players = self.font.render("2 players", True, BUTTONTEXT_COLOUR)
        w = max(one_player.get_width(), two_players.get_width()) + 2*xbuttonpad
        h = one_player.get_height() + 2*ybuttonpad
        # create "canvas" for the buttons and draw them
        surf1 = pygame.Surface((w,h))
        surf2 = pygame.Surface((w,h))
        surf1.fill(BUTTONBG_COLOUR)
        surf2.fill(BUTTONBG_COLOUR)
        surf1.blit(one_player, (w//2-one_player.get_width()//2, ybuttonpad))
        surf2.blit(two_players, (w//2-two_players.get_width()//2, ybuttonpad))
        # save the buttons and adjust their final position
        self.one_player_b = surf1
        self.two_players_b = surf2
        self.one_player_r = self.one_player_b.get_rect()
        self.two_players_r = self.two_players_b.get_rect()
        # center them vertically
        total_height = 2*h + youterpadding
        y = self.h//2 - total_height//2
        self.one_player_r.top = y
        self.two_players_r.top = y + h + youterpadding
        # center them horizontally
        x = self.w//2 - w//2
        self.one_player_r.left = x
        self.two_players_r.left = x

        ## create the buttons to choose the difficulty of the game
        # create a "back" button as well
        # again find the wider text
        easy = self.font.render("Easy", True, BUTTONTEXT_COLOUR)
        normal = self.font.render("Normal", True, BUTTONTEXT_COLOUR)
        hard = self.font.render("Hard", True, BUTTONTEXT_COLOUR)
        w = max([easy.get_width(), normal.get_width(), hard.get_width()]) + \
                    2*xbuttonpad
        h = easy.get_height() + 2*ybuttonpad
        # create the canvas and draw them
        easy_surf = pygame.Surface((w,h))
        easy_surf.fill(BUTTONBG_COLOUR)
        easy_surf.blit(easy, (round(w//2-easy.get_width()//2), ybuttonpad))
        normal_surf = pygame.Surface((w,h))
        normal_surf.fill(BUTTONBG_COLOUR)
        normal_surf.blit(normal, (w//2-normal.get_width()//2, ybuttonpad))
        hard_surf = pygame.Surface((w,h))
        hard_surf.fill(BUTTONBG_COLOUR)
        hard_surf.blit(hard, (w//2-hard.get_width()//2, ybuttonpad))
        # adjust their final positions and save them
        self.easy_b = easy_surf
        self.easy_r = easy_surf.get_rect()
        self.normal_b = normal_surf
        self.normal_r = normal_surf.get_rect()
        self.hard_b = hard_surf
        self.hard_r = hard_surf.get_rect()
        # find the total height and calcule each button's y position
        total_height = 2*youterpadding + 3*h
        y = self.h//2 - total_height//2
        self.easy_r.top = y
        self.normal_r.top = y + h + youterpadding
        self.hard_r.top = y + 2*h + 2*youterpadding
        # find their x position
        x = self.w//2 - w//2
        self.easy_r.left = self.normal_r.left = self.hard_r.left = x
        back = self.font.render(" << ", True, BUTTONTEXT_COLOUR)
        surf = pygame.Surface((back.get_width()+2*xbuttonpad//2, back.get_height() + 2*ybuttonpad//2))
        surf.fill(BUTTONBG_COLOUR)
        surf.blit(back, (xbuttonpad//2, ybuttonpad//2))
        self.back_b = surf
        self.back_r = surf.get_rect()
        # push the "back" button to the bottom right
        self.back_r.bottom = self.h - 20
        self.back_r.right = self.w - 20

    def draw_player_menu(self):
        """Draw all the buttons to choose between 1 and 2 players"""
        self.surface.fill(BG_COLOUR)
        self.surface.blit(self.one_player_b, self.one_player_r)
        self.surface.blit(self.two_players_b, self.two_players_r)

    def handle_player_menu_click(self, ev):
        """Handle clicks in the menu where we choose 1P/2P"""
        if self.one_player_r.collidepoint(ev.pos):
            self.screen = "difficulty_menu"
            self.players = 1
        elif self.two_players_r.collidepoint(ev.pos):
            self.players = 2

    def draw_difficulty_menu(self):
        """Draw all the buttons to choose the difficulty for 1P mode"""
        self.surface.fill(BG_COLOUR)
        # auto-magically draw all the buttons
        # assumes the surfaces end with _b and the rectangles with _r
        buttons = ["easy", "normal", "hard", "back"]
        for b in buttons:
            self.surface.blit(getattr(self, b+"_b"), getattr(self, b+"_r"))

    def handle_difficulty_menu_click(self, ev):
        """Handle clicks in the menu where the player chooses the difficulty"""
        if self.back_r.collidepoint(ev.pos):
            self.screen = "player_menu"
            self.players = None
        else:
            for i,b in enumerate(["easy", "normal", "hard"]):
                rect = getattr(self, b+"_r")
                if rect.collidepoint(ev.pos):
                    self.difficulty = i

    def handle_click(self, ev):
        """Dispatch all clicks to the right functions"""
        handle = getattr(self, "handle_"+self.screen+"_click")
        return handle(ev)

    def draw(self):
        """Draws the right screen"""
        draw_func = getattr(self, "draw_"+self.screen)
        draw_func()

class Game(object):
    """Wrapper class to hold functionality relating the board, players, info"""
    def __init__(self, surface, players, difficulty=None):
        """Initialize GUI elements and some logic of the game"""
        self.surface = surface
        self.players = players[::]
        self.symbols = ["x", "o"]
        shuffle(self.symbols)   # randomly assign the symbols
        self.to_move = 0
        self.difficulty = difficulty
        self.board = [["" for i in range(3)] for j in range(3)]
        self.still_playing = True

        # initialize the fonts if needed
        if not pygame.font.get_init():
            pygame.font.init()
        # use this for maximum compatibility
        df = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(df, 30)
        ## create "restart" and "menu" buttons
        xbuttonpad = 15
        ybuttonpad = 8
        restart = self.font.render("restart", True, BUTTONTEXT_COLOUR)
        menu = self.font.render("< menu", True, BUTTONTEXT_COLOUR)
        # find the wider
        w = max(restart.get_width(), menu.get_width()) + 2*xbuttonpad
        h = restart.get_height() + 2*ybuttonpad
        # create the canvas and draw them
        restart_surf = pygame.Surface((w,h))
        restart_surf.fill(BUTTONBG_COLOUR)
        restart_surf.blit(restart, ((w//2 - restart.get_width()//2), ybuttonpad))
        menu_surf = pygame.Surface((w,h))
        menu_surf.fill(BUTTONBG_COLOUR)
        menu_surf.blit(menu, ((w//2 - menu.get_width()//2), ybuttonpad))
        self.restart_b = restart_surf
        self.restart_r = restart_surf.get_rect()
        self.restart_r.top = SQUARESIZE//2 - h//2
        self.restart_r.right = _WIDTH - MENU_WIDTH//2 + w//2
        self.menu_b = menu_surf
        self.menu_r = menu_surf.get_rect()
        self.menu_r.bottom = _HEIGHT - SQUARESIZE//2 + h//2
        self.menu_r.right = self.restart_r.right

        # check if the NPC is the first move
        if self.players[self.to_move] == "NPC":
            self.get_NPC_move()

    def get_NPC_move(self):
        """NPC makes a move"""
        if not self.still_playing:
            return
        diffs = ["easy", "normal", "hard"]
        d = diffs[self.difficulty]
        npc_play = getattr(self, "get_"+d+"_move")
        npc_play()
        # change the player that is playing
        self.to_move = 1 - self.to_move

    def get_easy_move(self):
        """The NPC of difficulty "easy" makes a move as the given player"""
        ### try to find a winning play
        ### else play randomly
        symbol = self.symbols[self.to_move]
        moves = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "":
                    if self.is_winning_move(symbol, x, y):
                        self.board[x][y] = symbol
                        self.still_playing = False
                        return
                    else:
                        moves.append([x,y])
        if moves:
            x, y = choice(moves)
            self.board[x][y] = symbol
        else:
            self.still_playing = False

    def get_normal_move(self):
        """The NPC of difficulty "normal" makes a move as the given player"""
        ### try to find a winning play
        ### try to stop the other player from winning in the next move
        ### else play randomly
        symbol = self.symbols[self.to_move]
        moves = []
        # try to find a winning move
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "":
                    if self.is_winning_move(symbol, x, y):
                        self.board[x][y] = symbol
                        self.still_playing = False
                        return
                    else:
                        moves.append([x,y])
        # try to prevent a win
        op_symbol = self.symbols[1-self.to_move]
        for m in moves:
            x,y = m
            if self.is_winning_move(op_symbol, x, y):
                self.board[x][y] = symbol
                return
        # play randomly
        if moves:
            x, y = choice(moves)
            self.board[x][y] = symbol
        else:
            self.still_playing = False

    def get_hard_move(self):
        """The NPC of difficulty "hard" makes a move as the given player"""
        ### find a winning play
        ### try to stop other player from winning
        ### try to occupy the centre square
        ### try to occupy an opposite corner
        ### else play randomly
        symbol = self.symbols[self.to_move]
        moves = []
        # try to find a winning move
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "":
                    if self.is_winning_move(symbol, x, y):
                        self.board[x][y] = symbol
                        self.still_playing = False
                        return
                    else:
                        moves.append([x,y])
        # try to prevent a win
        op_symbol = self.symbols[1-self.to_move]
        for m in moves:
            x,y = m
            if self.is_winning_move(op_symbol, x, y):
                self.board[x][y] = symbol
                return
        # try to occupy the centre square
        if [1,1] in moves:
            self.board[1][1] = symbol
            return
        # try to occupy an opposite corner
        b = self.board
        if b[0][0] == op_symbol and [2,2] in moves:
            self.board[2][2] = symbol
            return
        elif b[0][2] == op_symbol and [2,0] in moves:
            self.board[2][0] = symbol
            return
        elif b[2][0] == op_symbol and [0,2] in moves:
            self.board[0][2] = symbol
            return
        elif b[2][2] == op_symbol and [0,0] in moves:
            self.board[0][0] = symbol
            return
        # play randomly
        if moves:
            x, y = choice(moves)
            self.board[x][y] = symbol
        else:
            self.still_playing = False

    def is_winning_move(self, symbol, x, y):
        """Checks if this next move is a winning move"""
        if self.board[x][y] != "":
            return False
        else:
            self.board[x][y] = symbol
            r = self.check_win()
            self.board[x][y] = ""
            return r

    def check_win(self):
        """Check if we have a winner"""
        ## check the horizontal lines
        b = self.board
        if b[0][0] == b[1][0] == b[2][0] != "":
            return True
        elif b[0][1] == b[1][1] == b[2][1] != "":
            return True
        elif b[0][2] == b[1][2] == b[2][2] != "":
            return True
        ## check vertical lines
        elif b[0][0] == b[0][1] == b[0][2] != "":
            return True
        elif b[1][0] == b[1][1] == b[1][2] != "":
            return True
        elif b[2][0] == b[2][1] == b[2][2] != "":
            return True
        ## check diagonals
        elif b[0][0] == b[1][1] == b[2][2] != "":
            return True
        elif b[0][2] == b[1][1] == b[2][0] != "":
            return True
        else:
            return False

    def draw_win(self):
        """Look for a win and mark it"""
        ## check the horizontal lines
        b = self.board
        if b[0][0] == b[1][0] == b[2][0] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (0, SQUARESIZE//2),
                            (WIDTH, SQUARESIZE//2),
                            BARWIDTH//3)
            return True
        elif b[0][1] == b[1][1] == b[2][1] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (0, SQUARESIZE+BARWIDTH+SQUARESIZE//2),
                            (WIDTH, SQUARESIZE+BARWIDTH+SQUARESIZE//2),
                            BARWIDTH//3)
            return True
        elif b[0][2] == b[1][2] == b[2][2] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (0, 2*(SQUARESIZE+BARWIDTH)+SQUARESIZE//2),
                            (WIDTH, 2*(SQUARESIZE+BARWIDTH)+SQUARESIZE//2),
                            BARWIDTH//3)
            return True
        ## check vertical lines
        elif b[0][0] == b[0][1] == b[0][2] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (SQUARESIZE//2, 0),
                            (SQUARESIZE//2, HEIGHT),
                            BARWIDTH//3)
            return True
        elif b[1][0] == b[1][1] == b[1][2] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (SQUARESIZE+BARWIDTH+SQUARESIZE//2, 0),
                            (SQUARESIZE+BARWIDTH+SQUARESIZE//2, HEIGHT),
                            BARWIDTH//3)
            return True
        elif b[2][0] == b[2][1] == b[2][2] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (2*(SQUARESIZE+BARWIDTH)+SQUARESIZE//2, 0),
                            (2*(SQUARESIZE+BARWIDTH)+SQUARESIZE//2, HEIGHT),
                            BARWIDTH//3)
            return True
        ## check diagonals
        elif b[0][0] == b[1][1] == b[2][2] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (0,0),
                            (WIDTH, HEIGHT),
                            BARWIDTH//3)
            return True
        elif b[0][2] == b[1][1] == b[2][0] != "":
            pygame.draw.line(screen,
                            YELLOW,
                            (WIDTH, 0),
                            (0, HEIGHT),
                            BARWIDTH//3)
            return True
        else:
            return False

    def handle_click(self, ev):
        """Handles a click in the game area
        Returns:    0 if we restarted the game
                    -1 if we exited to the menu"""
        if self.menu_r.collidepoint(ev.pos):
            return -1
        elif self.restart_r.collidepoint(ev.pos):
            return 0
        elif self.still_playing:
            x, restx = divmod(ev.pos[0], SQUARESIZE+BARWIDTH)
            y, resty = divmod(ev.pos[1], SQUARESIZE+BARWIDTH)
            # check if we clicked out of bounds
            if restx > SQUARESIZE or resty > SQUARESIZE:
                return
            if x > 2 or y > 2:
                return

            if self.board[x][y] == "":
                self.board[x][y] = self.symbols[self.to_move]
                if self.check_win():
                    # the player just won
                    self.still_playing = False
                else:
                    self.to_move = 1 - self.to_move
                    # should the NPC play?
                    if self.players[self.to_move] == "NPC":
                        self.get_NPC_move()

    def draw_play(self, symbol, x, y):
        """Auxiliary function to draw O/X in the board"""
        scr = self.surface
        if symbol == "o":
            pygame.draw.circle(scr,
                WHITE,
                (x*(SQUARESIZE+BARWIDTH)+SQUARESIZE//2, y*(SQUARESIZE+BARWIDTH)+SQUARESIZE//2),
                SQUARESIZE//2 - 5,
                BARWIDTH//4)
        else:
            pygame.draw.line(scr,
                WHITE,
                (x*(SQUARESIZE+BARWIDTH)+5, y*(SQUARESIZE+BARWIDTH)+5),
                (x*(SQUARESIZE+BARWIDTH)+SQUARESIZE-5, y*(SQUARESIZE+BARWIDTH)+SQUARESIZE-5),
                BARWIDTH//3)
            pygame.draw.line(scr,
                WHITE,
                (x*(SQUARESIZE+BARWIDTH)+SQUARESIZE-5, y*(SQUARESIZE+BARWIDTH)+5),
                (x*(SQUARESIZE+BARWIDTH)+5, y*(SQUARESIZE+BARWIDTH)+SQUARESIZE-5),
                BARWIDTH//3)

    def draw(self):
        """Draws the board to the surface"""
        self.surface.fill(BG_COLOUR)

        self.surface.blit(self.restart_b, self.restart_r)
        self.surface.blit(self.menu_b, self.menu_r)

        pygame.draw.line(self.surface,
                    BAR_COLOUR,
                    (0, SQUARESIZE+BARWIDTH//2),
                    (WIDTH, SQUARESIZE+BARWIDTH//2),
                    BARWIDTH)
        pygame.draw.line(self.surface,
                    BAR_COLOUR,
                    (0, 2*SQUARESIZE + 3*BARWIDTH//2),
                    (WIDTH, 2*SQUARESIZE + 3*BARWIDTH//2),
                    BARWIDTH)
        pygame.draw.line(self.surface,
                    BAR_COLOUR,
                    (SQUARESIZE+BARWIDTH//2, 0),
                    (SQUARESIZE+BARWIDTH//2, _HEIGHT),
                    BARWIDTH)
        pygame.draw.line(self.surface,
                    BAR_COLOUR,
                    (2*SQUARESIZE+3*BARWIDTH//2, 0),
                    (2*SQUARESIZE+3*BARWIDTH//2, HEIGHT),
                    BARWIDTH)
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "x":
                    self.draw_play("x", x, y)
                elif self.board[x][y] == "o":
                    self.draw_play("o", x, y)
        self.draw_win()

menu = Menu(screen, [_WIDTH, _HEIGHT])
playing = False
in_menu = True
difficulty = None
game = None

while (playing or in_menu):
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == MOUSEBUTTONDOWN:
            # if we aren't playing, we are in one of the menus...
            if in_menu:
                menu.handle_click(ev)
                if (menu.players == 1 and menu.difficulty is not None) or (menu.players == 2):
                    # start the game
                    in_menu = False
                    playing = True
                    if menu.players == 1:
                        players = ["NPC", "human"]
                        shuffle(players)
                        difficulty = menu.difficulty
                    else:
                        players = ["human"]*2
                    game = Game(screen, players, difficulty)
            elif playing:
                r = game.handle_click(ev)
                if r == 0:
                    # restart the attributes that change during the game
                    game = Game(screen, players, difficulty)
                elif r == -1:
                    game = None
                    menu = Menu(screen, [_WIDTH, _HEIGHT])
                    in_menu = True
                    playing = False

    if in_menu:
        menu.draw()
    if playing:
        game.draw()

    pygame.display.update()