import pygame

from src.game import Game

from src.screens.menu import Menu
from src.screens.main import Main

pygame.init()
pygame.font.init()

menu = Menu()
main = Main(menu)
# telas

if __name__ == "__main__":
    game = Game(menu)
    game.run(menu)
    ...
