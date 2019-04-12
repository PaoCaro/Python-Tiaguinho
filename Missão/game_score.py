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
        self.dead = False

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
        self.high_score = 0
        self.balls = []
        self.bg, self.bg_rect = load_png('bin/background.png')
        self.reset()

    def reset(self):
        """Resets the score, ball position and ball radius"""
        self.balls.clear()
        new_ball = Ball(WIDTH//2, BALL_SIZE, BALL_SIZE)
        # append adiciona um elemento ao fim da lista
        self.balls.append(new_ball)

        # Recomeçar pontos
        self.score = 0

    def draw(self, surface):
        """Draw the background and the ball on a surface"""
        # Desenhar o fundo
        surface.blit(self.bg, (0, 0))
        # Desenhar cada um dos elementos
        #  da Lista
        for ball in self.balls:
            ball.draw(surface)

    def draw_score(self, surface):
        """Draw the score on a surface"""
        # Criar o texto
        text = font.render(str(self.score), True, (155, 20, 20))
        # Desenhar o texto na surface
        surface.blit(text, (WIDTH - text.get_width() - 20, 20))

    def score_points(self, points):
        # Adicionar pontos ao jogo
        self.score += points
        # Atualizar o highscore
        if self.score > self.high_score:
            self.high_score = self.score

    def update(self, dt):
        """Updates ball position, checks if it is in bounds"""
        for ball in self.balls:
            ball.update(dt)
            if ball.posY > HEIGHT:
                ball.dead = True
            # Refletir a bola se bater nos lados
            if ball.posX > WIDTH or ball.posX < 0:
                ball.velX = -ball.velX
        self.balls[:] = [ball for ball in self.balls if not ball.dead]

    def split_ball (self, ball):
        new_ball = Ball(ball.posX, ball.posY, ball.radius)
        new_ball.velX = KICK_FORCE / 2
        new_ball.velY = -KICK_FORCE
        ball.velX = -KICK_FORCE / 2
        ball.velY = -KICK_FORCE
        self.balls.append(new_ball)
        self.score_points(1)


    def handle_click(self, ev):
        """Handle player mouse input event"""
        if ev.button == 1:
            for ball in self.balls:
                if ball.collide(ev.pos):
                    ball.kick(ev.pos)
                    ball.radius -= 1
                    self.score_points(1)
        elif ev.button == 3:
            for ball in self.balls[:]:
                if ball.collide(ev.pos):
                    self.split_ball(ball)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carregar fontes para textos
pygame.font.init()
df = pygame.font.get_default_font()
font = pygame.font.SysFont(df, 40)

# Inicializar o jogo
game = Game()
clock = pygame.time.Clock()

playing = True
while playing:
    # Eventos
    for ev in pygame.event.get():
        if ev.type == QUIT:
            playing = False
        elif ev.type == MOUSEBUTTONDOWN:
            game.handle_click(ev)
        elif ev.type == KEYDOWN:
            if ev.key == K_u:
                game.reset()

    if(len(game.balls) == 0):
        game.reset()

    dt = clock.tick(60) / 1000
    game.update(dt)
    game.draw(screen)
    game.draw_score(screen)
    
    # Atualizar ecrã
    pygame.display.update()

# Game over
screen.fill((0, 0, 0))
s = font.render("You lost with {} points!".format(game.high_score), True, (237, 205, 99))
screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 - s.get_height()//2))
pygame.display.update()

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.font.quit()
            pygame.quit()
            sys.exit()
