import pygame

# ui
from src.ui.buttons import Button
from src.config.settings import SCREEN_SIZE, GAME_TITLE
from .main import Main


class Menu:
    def __init__(self) -> None:
        self.load()
        self.game = Main()

    def load(self):
        # config
        self.tela = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        font = pygame.font.SysFont(name="comic sans", size=32)
        # groups
        self.button_group = pygame.sprite.Group()

        self.running = True
        self.background_color = (128, 0, 0)
        self.screen_width = SCREEN_SIZE[0] / 2

        self.texto_menu = font.render("MENU", False, "yellow")
        self.texto_creditos = font.render("by kBreno", False, "yellow")

        button_width, button_heigth = 200, 40
        button_x = self.screen_width // 2 + button_width // 4
        button_color = "blue"

        # buttons
        button1 = Button(
            button_x,
            150,
            button_width,
            button_heigth,
            button_color,
            "start",
            lambda: self.game.mainloop(),
        )
        button2 = Button(
            button_x,
            250,
            button_width,
            button_heigth,
            button_color,
            "exit",
            lambda: exit(),  # sai do jogo: pygame.quit(), sys.exit()
        )
        self.button_group.add(button1, button2)

    def mainloop(self):

        while self.running:
            self.clock.tick(60)
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # verifica qual botao foi pressionado e em seguida aciona sua respectiva funcao
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.button_group.sprites():
                        if button.is_clicked(mouse_pos):
                            button.function()
                            print("saindo..")

            # logic
            self.button_group.update()

            # redraw
            self.tela.fill(self.background_color)
            self.tela.blit(
                self.texto_menu,
                (self.screen_width // 2 + self.texto_menu.get_size()[0], 50),
            )
            self.tela.blit(self.texto_creditos, (self.screen_width // 2, 300))
            self.button_group.draw(self.tela)

            pygame.display.flip()
