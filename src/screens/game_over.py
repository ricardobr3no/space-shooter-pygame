import pygame

from src.ui.buttons import Button
from src.config.settings import TELA

font = pygame.font.SysFont(
    name="comic sans",
    size=24,
)

replay_button = Button(
    200, 250, 100, 20, "orange", "replay", lambda: print("replaying")
)
button_group = pygame.sprite.GroupSingle()
button_group.add(replay_button)


def show_game_over_screen():
    surface = pygame.Surface((400, 300))
    center = (surface.get_width() // 2, surface.get_height() // 2)
    game_over_label = font.render("GAME OVER", True, "white")

    # draw
    surface.fill("darkgray")
    surface.set_alpha(90)
    button_group.update()
    button_clicked = button_group.sprite.is_clicked(pygame.mouse.get_pos())
    # adicionando ao canva
    surface.blit(game_over_label, (center[0], center[1]))
    button_group.draw(surface)

    return surface, button_clicked


def teste():
    tela_teste = TELA
    running = True
    while running:
        tela_game_over, replaying = show_game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tela_game_over, replaying = show_game_over_screen()
                if replaying:
                    button_group.sprite.function()

        tela_teste.blit(tela_game_over, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    teste()
