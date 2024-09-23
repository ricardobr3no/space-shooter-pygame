from typing_extensions import Tuple
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(
    name="comic sans",
    size=24,
)


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        positionX: int,
        positionY: int,
        text: str,
        color: tuple | list | str,
        bg: tuple | list | str,
        size: tuple,
        callback=None,
    ) -> None:
        super().__init__(),
        self.text = font.render(text, False, color, bg)
        self.image = pygame.Surface(size)
        self.image.fill("gray")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = positionX, positionY
        self.color = color
        self.bg = bg

        if callback == None:
            callback = lambda: print("no function")
        self.callback = callback

    def checkMouseClick(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True

        return False

    def update(self, dt=None):
        if self.checkMouseClick():
            self.color, self.bg = self.bg, self.color
            self.callback()
