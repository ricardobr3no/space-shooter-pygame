import pygame

# config
from src.config.settings import TELA
from src.config.world import radial_glow


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        self.color = "dodgerblue"
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.apply_glow = True

    def update(self) -> None:
        self.glow(self.apply_glow)

    def death(self) -> None:
        print("coletado")
        self.kill()

    def glow(self, apply: bool):
        if apply:
            radial_glow(
                win=TELA,
                sprite=self,
                glow_color="red",
                intensity=80,
                glow_scale=1.3,
            )
