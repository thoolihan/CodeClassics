import pgzero, pgzrun
from enum import Enum

WIDTH=800
HEIGHT=480
BAT_PADDING=40
TITLE="Tim's Boing"

MIDDLE_X = WIDTH // 2
MIDDLE_Y = HEIGHT // 2

PLAYER_SPEED=6
MAX_AI_SPEED=6

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
    def __init__(self, player, speed=PLAYER_SPEED):
        super().__init__("bat00", (0, 0))
        if player == 1:
            self.x = BAT_PADDING
        elif player == 2:
            self.x = WIDTH - BAT_PADDING
        else:
            raise ValueError(f"Player should be 1 or 2, value passed in was {player}")
        self.y = MIDDLE_Y
        self.speed = speed
    
    def update(self):
        pass

    def move(self, direction):
        if direction == Direction.UP:
            self.y -= self.speed
        elif direction == Direction.DOWN:
            self.y += self.speed

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT



class Game():
    def __init__(self):
        self.state = State.MENU
        self.p1 = Bat(1)
        self.p2 = Bat(2)
        self.ball = Ball(-1)

        self.num_players = 1

        self.actors = [self.p1, self.p2, self.ball]
    
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

def update():
    game.update()

def draw(): 
    game.draw()

game = Game()

pgzrun.go()