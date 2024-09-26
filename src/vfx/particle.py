import pygame
import random, math
from random import randint


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.1, 0.5)
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.lifetime = 60
        self.load()

    def load(self, size=None, color=None, speed=None, lifetime=None):
        if size is not None:
            self.size = size
        if color is not None:
            self.color = color
        if speed is not None:
            self.speed = speed
        if lifetime is not None:
            self.lifetime = lifetime
        self.angle = self.get_angle()
        self.alpha = 255

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill(self.color)

    def get_angle(self):
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - self.y, mx - self.x) + randint(-3, 6) / 10
        # angulo mais desvio aleatorio
        # print(angle)
        return angle

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        self.alpha -= 2  # Diminui a opacidade gradualmente

    def draw(self, screen):
        self.update()
        self.image.set_alpha(self.alpha)
        screen.blit(self.image, (int(self.x), int(self.y)))

    def is_alive(self):
        return self.lifetime > 0


def teste():
    # Inicialização do Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Lista de partículas
    particles = []

    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Cria novas partículas (por exemplo, ao clicar)
        if pygame.mouse.get_pressed()[0]:
            for _ in range(10):
                particles.append(Particle(300, 150))
        # particles.append(Particle(*pygame.mouse.get_pos()))

        # Atualiza e desenha as partículas
        for particle in particles:
            particle.update()
            particle.draw(screen)

        # Remove partículas mortas
        particles = [particle for particle in particles if particle.is_alive()]

        # Atualiza a tela
        pygame.display.flip()
        # Limpa a tela
        screen.fill((0, 0, 0))

        # Limita a taxa de quadros
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    teste()
