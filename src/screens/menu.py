import pygame
from pygame.time import Clock
from ui.button import Button


hud_group = pygame.sprite.Group()


# janela de menu
def menu(tela):
    clock = Clock()
    running = True
    background_color = (128, 0, 0)
    font = pygame.font.SysFont("comic sans", 34)

    texto_menu = font.render("MENU", False, "yellow")
    button1 = pygame.Rect(300, 200, 100, 50)
    button2 = Button(300, 400, "credits", "white", "black", (50, 20))
    hud_group.add(button2)

    def draw_button(button, text_content: str, callback=None):
        if callback == None:
            callback = lambda: print("sem funcao")

        surface = pygame.draw.rect(tela, "blue", button1)
        texto = font.render("start", False, "white")
        tela.blit(texto, (surface.x, surface.y))
        callback()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if button1.collidepoint(mouse_pos):
                    print("apertou")

        # logic
        hud_group.update()

        tela.fill(background_color)
        tela.blit(texto_menu, (300, 100))
        hud_group.draw(tela)
        draw_button(
            button=button1,
            text_content="start",
        )

        # tela.blit(button1, (300, 200))
        pygame.display.flip()

    pygame.quit()
