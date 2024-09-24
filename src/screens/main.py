import pygame

# entities
from src.sprites.player import Player
from src.sprites.enemys import Enemy
from src.sprites.walls import Wall

# ui
# from ui.buttons import Button
from src.config.settings import SCREEN_SIZE, GAME_TITLE

# math
from random import choice

# from .menu import Menu


class Main:

    def __init__(self, game_menu: object | None = None) -> None:
        self.load()
        self.menu = game_menu

    def load(self):
        # config
        self.tela = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0  # spawn
        self.font = pygame.font.SysFont(name="comic sans", size=32)
        # self.menu = Menu()

        # groups
        self.player_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()

        # entities
        self.player = Player()
        self.player_group.add(self.player)

        wall_margin = self.player.rect.size[1] // 2

        # paredes invisiveis
        wall_1 = Wall(0, -wall_margin, SCREEN_SIZE[0], 1)  # top
        wall_2 = Wall(0, wall_margin + SCREEN_SIZE[1], SCREEN_SIZE[0], 1)  # bottom
        wall_3 = Wall(-wall_margin, 0, 1, SCREEN_SIZE[1])  # left
        wall_4 = Wall(wall_margin + SCREEN_SIZE[0], 0, 1, SCREEN_SIZE[1])  # right
        self.walls_group.add(wall_1, wall_2, wall_3, wall_4)

        # score and ho status
        self.score = 0
        self.score_label = self.font.render(f"{self.score}", True, "white")
        self.hp_label = self.font.render(f"HP: {self.player.hp}", True, "yellow")
        self.player_last_position = self.player.rect.x, self.player.rect.y

    def spawn_enemys(self, spawn_rate: float, dt: float):
        self.spawn_timer += dt
        if self.spawn_timer >= spawn_rate:
            spawn_range_x = choice((-30, SCREEN_SIZE[0] + 30))
            spawn_range_y = choice((-20, SCREEN_SIZE[1] + 30))

            new_enemy = Enemy(spawn_range_x, spawn_range_y, self.player)
            self.enemy_group.add(new_enemy)
            self.spawn_timer = 0

    def mainloop(self):

        while self.running:
            dt = self.clock.tick(60) / 1_000

            self.spawn_enemys(1.3, dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.bullets_group.add(self.player.shoot_bullet())

            # update
            self.player_group.update(dt)
            self.bullets_group.update(dt)
            self.enemy_group.update(dt)

            wall_colission = pygame.sprite.groupcollide(
                # verifica se atigiu uma parede
                self.walls_group,
                self.player_group,
                dokilla=False,
                dokillb=False,
            )
            acertou = pygame.sprite.groupcollide(
                self.bullets_group,
                self.enemy_group,
                dokilla=True,
                dokillb=True,
            )
            game_over = pygame.sprite.groupcollide(
                self.player_group,
                self.enemy_group,
                dokilla=False,
                dokillb=False,
            )

            if acertou:
                self.score += 1
                self.score_label = self.font.render(f"{self.score}", True, "white")

            if game_over:
                self.player.hp -= 1
                self.hp_label = self.font.render(
                    f"HP: {self.player.hp}", False, "yellow"
                )
                self.bullets_group.empty()
                self.enemy_group.empty()
                self.player.restart_position()
                if self.player.hp <= 0:
                    # player.restart()
                    # score = 0
                    # score_label = font.render(f"{score}", True, "white")
                    # spawn_timer = 0
                    # self.menu.mainloop()
                    # if self.menu is object:
                    self.menu.mainloop()
                    ...

            if wall_colission:
                self.player.rect.x, self.player.rect.y = self.player_last_position
            else:
                self.player_last_position = self.player.rect.x, self.player.rect.y

            # redraw
            self.tela.fill("midnightblue")

            self.player_group.draw(self.tela)
            self.bullets_group.draw(self.tela)
            self.enemy_group.draw(self.tela)

            self.tela.blit(self.score_label, (SCREEN_SIZE[0] // 2, 10))
            self.tela.blit(self.hp_label, (40, 10))
            pygame.display.flip()

        # encerra loop da tela atual com break e inicia o proximo
        # self.menu.mainloop()
