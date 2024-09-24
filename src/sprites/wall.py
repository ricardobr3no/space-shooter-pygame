import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_sprite_colliding(self, sprite) -> bool:
        if self.rect.colliderect(sprite["rect"]):
            return True
        return False
