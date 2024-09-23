from typing_extensions import Tuple
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(
    name="comic sans",
    size=24,
)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text, function):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        font = pygame.font.SysFont("comic sans", 36)
        self.text_surface = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(width // 2, height // 2))
        self.image.blit(self.text_surface, self.text_rect)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.function = function

    def update(self):
        pass

    def is_clicked(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)
