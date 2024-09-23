import pygame
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.size = 35
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill("pink")  # Cor vermelha
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 50
        self.target_player = player
        # self.dir = self.get_player_direction(x, y, player)

    def get_player_direction(self, fromX: int, fromY: int, player):
        angle = math.atan2(player.rect.y - fromY, player.rect.x - fromX)
        dx = math.cos(angle)
        dy = math.sin(angle)
        return dx, dy

    def update(self, dt):
        # Aqui você adicionaria a lógica de movimento do enemy
        # Por exemplo:
        dx, dy = self.get_player_direction(self.rect.x, self.rect.y, self.target_player)

        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt
