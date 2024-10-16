import pygame


class Game:

    def __init__(self, main_screen=None) -> None:
        pygame.init()
        pygame.font.init()
        self.main_screen = main_screen
        pygame.mouse.set_visible(False)

    def run(self, screen=None):
        """
        se não foi passado uma tela especifica no metodo 'run' e nem foi definida uma tela padrao. Entao deve exibir mensagem de alerta
        """
        if screen is None:
            self.main_screen.mainloop()
            return
        screen.mainloop()
