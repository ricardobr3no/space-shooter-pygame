import pygame
import math

# config
from src.config.settings import TELA
from src.config.world import radial_glow, rect_glow

# vfx
# from src.vfx.particle import Particle


class Enemy_1(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.color: str | tuple = "hotpink2"
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)  # Cor vermelha
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 60
        self.target_player = player
        self.hp = 2
        self.apply_glow = True

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
        self.glow(self.apply_glow)

    def glow(self, apply: bool):
        if apply:
            radial_glow(
                win=TELA,
                sprite=self,
                offset=(0, 0),
                glow_color=self.color,
                intensity=100,
                glow_scale=1.3,
            )

    def death(self):
        self.kill()

    def __repr__(self) -> str:
        return "Enemy Type 1"


class Enemy_2(Enemy_1):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.color = "deeppink"
        self.size = 45
        self.speed = 40
        self.hp = 5
        self.update_image()

    def update_image(self):
        self.color = "deeppink"
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def __repr__(self) -> str:
        return "Enemy Type 2"
