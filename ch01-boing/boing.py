import pgzero, pgzrun, pygame
from enum import Enum
from random import randint

WIDTH=800
HEIGHT=480
BAT_PADDING=40
TITLE="Tim's Boing"

MIDDLE_X = WIDTH // 2
MIDDLE_Y = HEIGHT // 2

PLAYER_SPEED=6
MAX_AI_SPEED=6

space_held = False

class State(Enum):
    MENU = 1
    PLAY = 2
    GAMEOVER = 3

class Direction(Enum):
    UP = 1
    DOWN = 2
    NONE = 3

class Ball(Actor):
    def __init__(self, dx):
        super().__init__("ball", (0, 0))
        self.x = MIDDLE_X
        self.y = MIDDLE_Y
        self.dx = dx
        self.dy = 0

    def update(self):
        pass
    
class Bat(Actor):
    def __init__(self, player, speed=PLAYER_SPEED, move_function=None):
        super().__init__("bat00", (0, 0))
        if player == 1:
            self.x = BAT_PADDING
        elif player == 2:
            self.x = WIDTH - BAT_PADDING
        else:
            raise ValueError(f"Player should be 1 or 2, value passed in was {player}")
        self.y = MIDDLE_Y
        self.speed = speed
        self.score = 0
        if move_function is None:
            move_function = self.ai_move
        self.get_move = move_function
    
    def update(self):
        _dir = self.get_move()
        self.move(_dir)

    def move(self, dir_move):
        if dir_move == Direction.UP:
            self.y -= self.speed
        elif dir_move == Direction.DOWN:
            self.y += self.speed

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT
    
    def score_point(self):
        self.score += 1

    def ai_move(self):
        # ToDo: Implement actual AI, once ball movement is set. For now, just move randomly.
        dir = randint(-1, 1)
        if dir == 1:
            return Direction.UP
        elif dir == -1:
            return Direction.DOWN
        else:
            return Direction.NONE

class Game():
    def __init__(self):
        self.state = State.MENU
        self.num_players = 1
        self.actors = []
    
    def start_new_game(self):
        self.state = State.PLAY
        self.p1 = Bat(1, move_function=p1_move)
        if self.num_players == 1:
            self.p2 = Bat(2)
        else:
            self.p2 = Bat(2, move_function=p2_move)
        self.ball = Ball(-1)
        self.actors = [self.p1, self.p2, self.ball]

    def go_to_menu(self):
        self.state = State.MENU
        self.actors = []
    
    def end(self):
        self.state = State.GAMEOVER

    def update(self):
        for obj in self.actors:
            obj.update()

    def draw(self):
        screen.blit("table", (0, 0))

        for obj in self.actors:
            obj.draw()

        if self.state == State.GAMEOVER:
            screen.blit("over", (0, 0))
        elif self.state == State.MENU:
            menu_image = f"menu{self.num_players - 1}"
            screen.blit(menu_image, (0, 0))
        else:
            pass

def p1_move():
    if keyboard.up or keyboard.a or keyboard.s:
        return Direction.UP
    elif keyboard.down or keyboard.z or keyboard.x:
        return Direction.DOWN
    else:
        return Direction.NONE
    
def p2_move():
    if keyboard.k or keyboard.l or keyboard.semicolon or keyboard.quote:
        return Direction.UP
    elif keyboard.m or keyboard.comma or keyboard.period or keyboard.slash:
        return Direction.DOWN
    else:
        return Direction.NONE
    
def update():
    global space_held, game
    space_pressed = False
    if keyboard.space and not space_held:
        space_pressed = True
    space_held = keyboard.space
    if game.state == State.MENU:
        if keyboard.up:
            game.num_players = 1
        elif keyboard.down:
            game.num_players = 2
        elif space_pressed:
            game.start_new_game()
    elif game.state == State.GAMEOVER:
        if space_pressed:
            game.go_to_menu()
    elif game.state == State.PLAY:
        game.update()
        if keyboard.escape:
            game.end()

def draw(): 
    game.draw()

game = Game()

pgzrun.go()