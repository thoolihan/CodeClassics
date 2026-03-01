import pgzero, pgzrun, pygame
from enum import Enum
from random import randint
import math

WIDTH=800
HEIGHT=480
BAT_PADDING=40
TITLE="Tim's Boing"

MIDDLE_X = WIDTH // 2
MIDDLE_Y = HEIGHT // 2

HALF_BATX = 9
HALF_BATY = 64
HALF_BALL = 7
PLANE = MIDDLE_X - (BAT_PADDING + HALF_BATX + HALF_BALL)

PLAYER_SPEED=6
MAX_AI_SPEED=6

space_held = False

def clip(value, min_value = -1, max_value = 1):
    return max(min_value, min(value, max_value))

def normalize(x, y):
    length = math.hypot(x, y)
    return (x / length, y / length)

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
        self.speed = 5
        self.pause_counter = 0
        self.rebound_counter = 0

    def update(self):
        passing = False       
        if self.rebound_counter > 0:
            self.rebound_counter -= 1

        for i in range(self.speed):
            self.x += self.dx
            self.y += self.dy

            if self.y < 0:
                self.y = 0
                self.dy *= -1
            elif self.y > HEIGHT:
                self.y = HEIGHT
                self.dy *= -1
        
            if not passing and \
                self.rebound_counter==0 and \
                (self.x < (MIDDLE_X - PLANE) or self.x > (MIDDLE_X + PLANE)):
                passing = True
                if self.dx < 0:
                    # ball headed left
                    diff_y = self.y - game.p1.y
                    if abs(diff_y) < HALF_BATY:
                        self.rebound(diff_y)
                        game.p1.rebound()
                else:
                    # ball headed right
                    diff_y = self.y - game.p2.y
                    if abs(diff_y) < HALF_BATY:
                        self.rebound(diff_y)    
                        game.p2.rebound()     

            if self.out() and self.pause_counter == 0:
                self.pause_counter = 20
                if self.dx < 0:
                    game.p2.score_point()
                    game.p1.opp_scored_counter = 20
                else:
                    game.p1.score_point()
                    game.p2.opp_scored_counter = 20

            if self.pause_counter > 0:
                    self.pause_counter -= 1
                    game.ball = Ball(-self.dx)
                    game.actors[2] = game.ball
                    break     

    def rebound(self, diff_y):
        self.rebound_counter = 2
        self.dx *= -1
        self.dy += diff_y / (HALF_BATY * 2)
        self.dy = clip(self.dy)
        self.dx, self.dy = normalize(self.dx, self.dy)
        if self.speed < MIDDLE_X:
            self.speed+=1
        else:
            pass 
    
    def out(self):
        return self.x < 0 or self.x > WIDTH
    
class Bat(Actor):
    def __init__(self, player, speed=PLAYER_SPEED, move_function=None):
        super().__init__(f"bat{player-1}0", (0, 0))
        self.player = player
        if self.player == 1:
            self.x = BAT_PADDING
        elif self.player == 2:
            self.x = WIDTH - BAT_PADDING
        else:
            raise ValueError(f"Player should be 1 or 2, value passed in was {player}")
        self.y = MIDDLE_Y
        self.speed = speed
        self.score = 0
        if move_function is None:
            move_function = self.ai_move
        self.get_move = move_function
        self.score_counter = 0
        self.rebound_counter = 0
        self.opp_scored_counter = 0
    
    def update(self):
        _dir = self.get_move()
        self.move(_dir)
        self.image = self.bat_sprite()

    def move(self, dir_move):
        if dir_move == Direction.UP:
            self.y -= self.speed
        elif dir_move == Direction.DOWN:
            self.y += self.speed

        if self.y < HALF_BATY:
            self.y = HALF_BATY
        elif self.y > (HEIGHT - HALF_BATY):
            self.y = HEIGHT - HALF_BATY
    
    def score_point(self):
        self.score += 1
        self.score_counter = 30

    def rebound(self):
        self.rebound_counter = 15

    def bat_sprite(self):
        if self.rebound_counter > 0:
            self.rebound_counter -= 1
            return f"bat{self.player-1}1"
        elif self.opp_scored_counter > 0:
            self.opp_scored_counter -= 1
            return f"bat{self.player-1}2"
        else:
            return f"bat{self.player-1}0"
        

    def score_color(self):   
        if self.score_counter > 0:
            self.score_counter -= 1
            return 3 - self.player
        else:
            return 0        

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

        # draw ball, bats
        for obj in self.actors:
            obj.draw()

        # draw score
        if self.state != State.MENU:
            p1_d1_img = f"digit{self.p1.score_color()}{(self.p1.score // 10)}"
            p1_d2_img = f"digit{self.p1.score_color()}{(self.p1.score % 10)}"
            p2_d1_img = f"digit{self.p2.score_color()}{(self.p2.score // 10)}"
            p2_d2_img = f"digit{self.p2.score_color()}{(self.p2.score % 10)}"            
            screen.blit(p1_d1_img, (WIDTH // 4 - 20, 20))
            screen.blit(p1_d2_img, (WIDTH // 4 + 20, 20))
            screen.blit(p2_d1_img, (WIDTH * 3 // 4 - 20, 20))
            screen.blit(p2_d2_img, (WIDTH * 3 // 4 + 20, 20))
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
        if keyboard.escape or max(game.p1.score, game.p2.score) > 9:
            game.end()
        else: 
            game.update()

def draw(): 
    game.draw()

game = Game()

try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)

    music.play("theme")
    music.set_volume(0.3)
except Exception:
    # If an error occurs (e.g. no sound device), just ignore it
    pass

pgzrun.go()