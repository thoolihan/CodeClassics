import pgzero, pgzrun

WIDTH=800
HEIGHT=480
BAT_PADDING=40
TITLE="Tim's Boing"

MIDDLE_X = WIDTH // 2
MIDDLE_Y = HEIGHT // 2

PLAYER_SPEED=6
MAX_AI_SPEED=6

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
    def __init__(self, player):
        super().__init__("bat00", (0, 0))
        if player == 1:
            self.x = BAT_PADDING
        elif player == 2:
            self.x = WIDTH - BAT_PADDING
        else:
            raise ValueError(f"Player should be 1 or 2, value passed in was {player}")
        self.y = MIDDLE_Y
    
    def update(self):
        pass
        

def update():
    for obj in game:
        obj.update()

def draw(): 
    screen.blit("table", (0, 0))
    for obj in game:
        obj.draw()

num_players = 1
b = Ball(-1)
p1 = Bat(1)
p2 = Bat(2)
game = [b, p1, p2]

pgzrun.go()