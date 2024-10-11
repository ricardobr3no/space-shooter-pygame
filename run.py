import pygame

from src.game import Game

from src.screens.game_over import teste
from src.screens.menu import Menu
from src.screens.main import Main

pygame.init()
pygame.font.init()

# telas
menu = Menu()
main = Main(menu)

if __name__ == "__main__":
    game = Game()
    # game.run(main)
    main.mainloop()
    # teste()
    ...
