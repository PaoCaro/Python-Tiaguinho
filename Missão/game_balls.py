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
        # Apagar todas as bolas
        self.balls.clear()
        # Criar a primeira bola
        new_ball = Ball(WIDTH//2, BALL_SIZE, BALL_SIZE)
        # Adicionar a bola nova à lista
        self.balls.append(new_ball)
        # Recomeçar pontos
        self.score = 0

    def split_ball(self, ball):
        # Criar a bola nova no mesmo sitio e com o mesmo tamanho
        new_ball = Ball(ball.posX, ball.posY, ball.radius)
        # A bola nova vai prá direita (positivo)
        new_ball.velX = KICK_FORCE / 2
        # A bola velha vai para a esquerda (negativo)
        ball.velX = -KICK_FORCE / 2
        # Ambas as bolas vão para cima (negativo)
        new_ball.velY = -KICK_FORCE
        ball.velY = -KICK_FORCE
        # Adicionar a bola nova à lista
        self.balls.append(new_ball)

    def draw(self, surface):
        """Draw the background and the ball on a surface"""
        # Desenhar o fundo
        surface.blit(self.bg, (0, 0))
        # Desenhar cada uma das bola na lista
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
        # Processar todas as bolas da lista
        for ball in self.balls:
            # Atualizar a bola
            ball.update(dt)
            # Remover a bola da lista se ela cair
            if ball.posY > HEIGHT:
                ball.dead = True
            # Refletir a bola se bater nos lados
            if ball.posX > WIDTH or ball.posX < 0:
                ball.velX = -ball.velX
        # Filtrar as bolas mortas
        self.balls[:] = [b for b in self.balls if not b.dead]

    def handle_click(self, ev):
        """Handle player mouse input event"""
        # Botão esquerdo
        if ev.button == 1:
            # Verificar se tocamos em alguma das bola
            for ball in self.balls:
                if ball.collide(ev.pos):
                    # Acertamos
                    ball.kick(ev.pos)
                    ball.radius -= 1
                    self.score += 1
        # Botão direito
        elif ev.button == 3:
            # Verificar se tocamos em alguma das bola
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

    # Recomeçar o jogo se o jogador não tiver mais bolas
    if (len(game.balls) == 0):
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

# Esperar para sair
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.font.quit()
            pygame.quit()
            sys.exit()
