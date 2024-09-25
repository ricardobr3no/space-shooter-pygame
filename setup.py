import pygame

from src.game import Game

from src.screens.menu import Menu
from src.screens.main import Main

pygame.init()
pygame.font.init()

# telas
menu = Menu()
main = Main(menu)

if __name__ == "__main__":
    game = Game(menu)
    game.run(main)
    ...
