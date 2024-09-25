from random import randrange
import pygame

BACKGROUND_COLOR = "midnightblue"
from .settings import TELA


def rect_glow(
    win: pygame.Surface,
    sprite,
    offset: tuple = (0, 0),
    glow_color: tuple | str = "white",
    intensity: int = 1,
    glow_scale: float = 1,
):
    """
    o efeito de glow consiste em adicionar à uma superficie, varias camadas com diferentes tonalidades e opacidade
    """
    size_surface = sprite_size = sprite.rect.size[0]

    position = (
        sprite.rect.x + offset[0],
        sprite.rect.y + offset[1],
    )

    for n_layer in range(1, 6):
        glow_surface = pygame.Surface((size_surface, size_surface))
        glow_surface.set_alpha(intensity)
        glow_surface.fill(glow_color)

        size_surface = glow_surface.get_size()[0]

        win.blit(
            glow_surface,
            (
                position[0] - size_surface // 2 + sprite_size // 2,
                position[1] - size_surface // 2 + sprite_size // 2,
            ),
        )
        intensity //= n_layer
        size_surface *= glow_scale


def radial_glow(
    win: pygame.Surface,
    sprite,
    offset: tuple = (0, 0),
    glow_color: tuple | str = "white",
    intensity: int = 1,
    glow_scale: float = 1,
):
    """
    o efeito de glow consiste em adicionar à uma superficie, varias camadas com diferentes tonalidades e opacidade
    """
    size_surface = sprite_size = sprite.rect.size[0]
    # radius = glow_scale * sprite_size

    position = (
        sprite.rect.x + offset[0],
        sprite.rect.y + offset[1],
    )

    for n_layer in range(1, 6):
        glow_surface = pygame.Surface((size_surface, size_surface))
        glow_surface.fill(BACKGROUND_COLOR)

        size_surface = glow_surface.get_size()[0]
        glow_surface.set_alpha(intensity)

        pygame.draw.circle(
            surface=glow_surface,
            color=glow_color,
            center=(
                size_surface // 2,
                size_surface // 2,
            ),
            radius=size_surface // 2,
        )

        win.blit(
            glow_surface,
            (
                position[0] - size_surface // 2 + sprite_size // 2,
                position[1] - size_surface // 2 + sprite_size // 2,
            ),
        )
        intensity //= n_layer
        size_surface *= glow_scale
