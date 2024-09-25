import pygame
from src.config.settings import SCREEN_SIZE, TELA
from src.config.world import radial_glow
from .bullets import Bullet

width, height = SCREEN_SIZE


class Player(pygame.sprite.Sprite):
    size = 50

    def __init__(self):
        super().__init__()
        self.restart()

    def restart(self):
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 0, 0))  # Cor vermelha
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - self.size // 2
        self.rect.y = height // 2 - self.size // 2
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.speed = 300
        self.hp = 3
        self.damage = 1
        self.apply_glow = True

    def restart_position(self):
        self.rect.x = width // 2 - self.size // 2
        self.rect.y = height // 2 - self.size // 2

    def update(self, dt):
        # Aqui você adicionaria a lógica de movimento do player
        # Por exemplo:
        keys = pygame.key.get_pressed()
        dir = pygame.Vector2()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dir.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dir.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dir.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dir.y += 1

        if dir != (0, 0):
            dir = dir.normalize()

        self.rect.x += dir.x * self.speed * dt
        self.rect.y += dir.y * self.speed * dt

        # glow
        self.glow(self.apply_glow)

    def shoot_bullet(self):
        mouse_pos = pygame.mouse.get_pos()
        target_x, target_y = mouse_pos
        start_x, start_y = (
            self.rect.x + self.size / 2,
            self.rect.y + self.size / 2,
        )
        bullet = Bullet(start_x, start_y, target_x, target_y)
        return bullet

    def glow(self, apply: bool):
        if apply:
            radial_glow(
                win=TELA,
                sprite=self,
                glow_color="red",
                intensity=80,
                glow_scale=1.4,
            )
