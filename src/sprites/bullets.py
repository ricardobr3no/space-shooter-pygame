import pygame
import math

from src.config.settings import SCREEN_SIZE, TELA
from src.config.world import radial_glow


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self, start_x, start_y, target_x, target_y, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))  # size
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 500
        self.dx, self.dy = self.target_direction(start_x, start_y, target_x, target_y)
        self.apply_glow = True

    def target_direction(self, fromX, fromY, toX, toY):
        angle = math.atan2(toY - fromY, toX - fromX)
        dx = math.cos(angle)
        dy = math.sin(angle)
        return dx, dy

    def update(self, dt) -> None:
        self.rect.x += self.dx * self.speed * dt
        self.rect.y += self.dy * self.speed * dt

        # remover se tiver fora do canva
        if (self.rect.x < -10 or self.rect.x > SCREEN_SIZE[0] + 10) or (
            self.rect.y < -10 or self.rect.y > SCREEN_SIZE[1] > 10
        ):
            self.kill()
            print("removido")

        self.glow(self.apply_glow)

    def glow(self, apply: bool):
        if apply:
            radial_glow(
                win=TELA,
                sprite=self,
                offset=(0, 0),
                glow_color="red",
                intensity=180,
                glow_scale=1.6,
            )
