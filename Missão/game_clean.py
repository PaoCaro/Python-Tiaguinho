import sys
import pygame

from pygame.locals import *


from lib import load_png, get_random_colour, dist

WIDTH = 600
HEIGHT = 350

GRAVITY = 500
KICK_FORCE = 300
HORIZONTAL_MULT = 10
BALL_SIZE = 40


class Ball(object):
    color = (100, 10, 10)

    def __init__(self, start_x, start_y, radius):
        """Creates a ball"""
        self.posX = start_x
        self.posY = start_y
        self.velX = 0
        self.velY = 0
        self.radius = radius
        self.img, self.img_rect = load_png("bin/ball.png")

    def collide(self, point):
        """Returns whether the point is inside the ball"""
        # Criar um ponto
        pos = (self.posX, self.posY)
        # Verificar distancia
        d = dist(pos, point)
        # Existe colisão se a distancia for menor que o raio da bola
        return d <= self.radius

    def kick(self, mouse_pos):
        """Kicks the ball upwards according to the mouse position"""
        dx = mouse_pos[0] - self.posX
        self.velY = -KICK_FORCE
        self.velX = -HORIZONTAL_MULT * dx

    def draw(self, surface):
        """Draw the ball on a surface"""
        pos = (int(self.posX), int(self.posY))
        pygame.draw.circle(surface, Ball.color, pos, int(self.radius))

    def update(self, dt):
        """Updates the ball position"""
        # Movimento horizontal
        self.posX += self.velX * dt
        # Movimento vertical
        self.velY += GRAVITY * dt
        self.posY += self.velY * dt


class Game(object):
    def __init__(self):
        """Create a new game"""
        self.score = 0
        self.ball = Ball(WIDTH//2, BALL_SIZE, BALL_SIZE)
        self.bg, self.bg_rect = load_png('bin/background.png')
        self.reset()

    def reset(self):
        """Resets the score, ball position and ball radius"""
        # Posição
        self.ball.posX = WIDTH / 2
        self.ball.posY = BALL_SIZE
        # Velocidade
        self.ball.velX = 0
        self.ball.velY = 0
        # Tamanho
        self.ball.radius = BALL_SIZE
        # Recomeçar pontos
        self.score = 0

    def draw(self, surface):
        """Draw the background and the ball on a surface"""
        # Desenhar o fundo
        surface.blit(self.bg, (0, 0))
        # Desenhar a bola
        self.ball.draw(surface)

    def update(self, dt):
        """Updates ball position, checks if it is in bounds"""
        self.ball.update(dt)
        # Recomeçar o jogo se a bola cair
        if self.ball.posY > HEIGHT:
            self.reset()
        # Refletir a bola se bater nos lados
        if self.ball.posX > WIDTH or self.ball.posX < 0:
            self.ball.velX = -self.ball.velX

    def handle_click(self, ev):
        """Handle player mouse input event"""
        if ev.button == 1:
            if self.ball.collide(ev.pos):
                self.ball.kick(ev.pos)
                self.ball.radius -= 1
                self.score += 1
            else:
                self.score -= 1
        elif ev.button == 3:
            pass


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.font.init()
df = pygame.font.get_default_font()
font = pygame.font.SysFont(df, 40)

game = Game()
clock = pygame.time.Clock()

playing = True
while playing:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            playing = False
        elif ev.type == MOUSEBUTTONDOWN:
            game.handle_click(ev)
        elif ev.type == KEYDOWN:
            if ev.key == K_u:
                game.reset()

    dt = clock.tick(60) / 1000
    game.update(dt)
    game.draw(screen)
    pygame.display.update()

# Game over
screen.fill((0, 0, 0))
s = font.render("You lost with {} points!".format(game.score), True, (237, 205, 99))
screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 - s.get_height()//2))
pygame.display.update()

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.font.quit()
            pygame.quit()
            sys.exit()
