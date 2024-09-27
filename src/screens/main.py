import random
import pygame
import time

# entities
from src.sprites.player import Player
from src.sprites.enemys import Enemy_1, Enemy_2
from src.sprites.power_up import PowerUp
from src.sprites.walls import Wall

# ui
from src.ui.buttons import Button
from src.config.settings import SCREEN_SIZE, GAME_TITLE, FPS, TELA
from src.config.world import BACKGROUND_COLOR

from .game_over import show_game_over_screen

# math
from random import choice, randint

from src.vfx.particle import Particle

font = pygame.font.SysFont(
    name="comic sans",
    size=24,
)


class Main:

    def __init__(self, game_menu: object | None = None) -> None:
        self.load()
        self.menu = game_menu
        self.best_score = 0

    def load(self):
        # config
        pygame.display.set_caption(GAME_TITLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0  # spawn
        self.font = pygame.font.SysFont(name="comic sans", size=32)
        # self.menu = Menu()

        # groups
        self.player_group = pygame.sprite.GroupSingle()
        self.bullets_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.powerups_group = pygame.sprite.Group()
        self.button_group = pygame.sprite.GroupSingle()

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
        self.game_over_label = self.font.render("GAME OVER", True, "white")
        self.hp_label = self.font.render(f"HP: {self.player.hp}", True, "yellow")
        self.player_last_position = self.player.rect.x, self.player.rect.y
        # powerups
        self.power_ups_count = 0
        self.power_ups_timer = 0

        self.particles = []
        self.tela_game_over = self.show_game_over_screen()
        self.replaying = False
        self.is_game_over = False

    def show_game_over_screen(self):

        surface = pygame.Surface((400, 300))
        center = (surface.get_width() // 2, surface.get_height() // 2)

        # draw
        surface.fill("darkgray")
        surface.set_alpha(90)
        width_button = 100
        self.replay_button = Button(
            x=SCREEN_SIZE[0] // 2 - width_button // 2,
            y=SCREEN_SIZE[1] // 2 + 100,
            width=width_button,
            height=40,
            color="orange",
            text="replay",
            function=lambda: self.load(),
        )
        self.button_group.add(self.replay_button)
        self.button_group.update()
        # adicionando ao canva
        surface.blit(
            self.game_over_label,
            (center[0] - self.game_over_label.get_width() // 2, center[1]),
        )
        self.button_group.draw(surface)

        return surface

    def spawn_power_up(self, x, y):
        powerup = PowerUp(x, y)
        self.powerups_group.add(powerup)

    def spawan_bullets_extra(self, shooted_bullet, amount):
        self.power_ups_timer += amount
        extra_bullets = []

        for _ in range(self.power_ups_count):
            extra_bullets.append(shooted_bullet)

        if self.power_ups_timer >= 0.4:
            self.bullets_group.add(extra_bullets[0])

    def spawn_enemys(self, spawn_rate: float, dt: float):
        self.spawn_timer += dt
        if self.spawn_timer >= spawn_rate:
            # choicing spawn location
            spawn_margin = 30
            spawn_location = choice(
                [
                    # borders
                    (-spawn_margin, -30),
                    (-spawn_margin, SCREEN_SIZE[1] + 30),
                    (SCREEN_SIZE[0] + spawn_margin, -30),
                    (SCREEN_SIZE[0] + spawn_margin, SCREEN_SIZE[1] + 30),
                    # centers
                    (SCREEN_SIZE[0] // 2, -spawn_margin),
                    (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] + spawn_margin),
                    (-spawn_margin, SCREEN_SIZE[1] // 2),
                    (SCREEN_SIZE[0] + spawn_margin, SCREEN_SIZE[1] // 2),
                ]
            )

            # choicing enemy type
            choiced_enemy = choice([Enemy_1, Enemy_1, Enemy_1, Enemy_2])
            new_enemy = choiced_enemy(spawn_location[0], spawn_location[1], self.player)
            self.enemy_group.add(new_enemy)
            self.spawn_timer = 0

    def mainloop(self):

        # codigo temporario
        self.spawn_power_up(500, 400)
        showing_game_over = False

        while self.running:
            dt = self.clock.tick(FPS) / 1_000
            spawn_rate = 1.3
            self.spawn_enemys(spawn_rate, dt)

            # loop de evento
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    shooted_bullet = self.player.shoot_bullet()
                    self.bullets_group.add(shooted_bullet)

                    if showing_game_over:
                        print("mostrei")
                        self.replaying = self.replay_button.is_clicked(
                            pygame.mouse.get_pos()
                        )
                        if self.replaying:
                            self.button_group.sprite.function()
                            showing_game_over = False

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
                dokillb=False,
            )
            atingido = pygame.sprite.groupcollide(
                self.player_group,
                self.enemy_group,
                dokilla=False,
                dokillb=False,
            )
            coletou_power_up = pygame.sprite.groupcollide(
                self.player_group, self.powerups_group, dokilla=False, dokillb=True
            )

            if acertou:
                """
                A função pygame.sprite.groupcollide() retorna um dicionário que mapeia os sprites do primeiro grupo com os sprites do segundo grupo que colidiram com eles.
                """
                for sprites_collision in acertou.values():
                    for enemy in sprites_collision:
                        enemy.hp -= self.player.damage

                        if enemy.hp <= 0:
                            particle_lifetime = randint(100, 150)

                            for _ in range(randint(2, 4)):
                                # particula blood
                                new_particle = Particle(enemy.rect.x, enemy.rect.y)
                                # config particle
                                new_particle.load(
                                    size=enemy.size // 2,
                                    color="purple",
                                    speed=random.uniform(0.8, 1.1),
                                    lifetime=particle_lifetime,
                                )
                                self.particles.append(new_particle)
                                enemy.death()

                            # particula body
                            new_particle = Particle(enemy.rect.x, enemy.rect.y)
                            # config particle
                            new_particle.load(
                                size=enemy.size,
                                color=enemy.color,
                                lifetime=particle_lifetime,
                                speed=0.2,
                            )

                            self.particles.append(new_particle)
                            enemy.death()

                            self.score += 1
                            self.score_label = self.font.render(
                                f"{self.score}", True, "white"
                            )

            if atingido:
                self.player.hp -= 1
                self.hp_label = self.font.render(
                    f"HP: {self.player.hp}", False, "yellow"
                )
                self.bullets_group.empty()
                self.enemy_group.empty()
                self.player.restart_position()
                #
                if self.player.hp <= 0:
                    if self.score > self.best_score:  # atualiza best_score
                        self.best_score = self.best_score

                    self.score = 0
                    self.score_label = self.font.render(f"{self.score}", True, "white")
                    self.spawn_timer = 0

                    showing_game_over = True

                    ...

            if wall_colission:
                self.player.rect.x, self.player.rect.y = self.player_last_position
            else:
                self.player_last_position = self.player.rect.x, self.player.rect.y

            if coletou_power_up:
                print("coletou mesmo")
                self.power_ups_count += 1

            # redraw
            if not showing_game_over:
                TELA.fill(BACKGROUND_COLOR)
                # update
                self.player_group.update(dt)
                self.bullets_group.update(dt)
                self.enemy_group.update(dt)

                # draw
                self.powerups_group.draw(TELA)
                self.player_group.draw(TELA)
                self.bullets_group.draw(TELA)
                self.enemy_group.draw(TELA)

                for particle in self.particles:
                    particle.draw(TELA)
                    ...

                TELA.blit(self.score_label, (SCREEN_SIZE[0] // 2, 10))
                TELA.blit(self.hp_label, (40, 10))

            else:
                self.button_group.update()
                self.tela_game_over = self.show_game_over_screen()
                self.replaying = self.replay_button.is_clicked(pygame.mouse.get_pos())
                print(self.replaying)

                TELA.blit(
                    self.tela_game_over,
                    (
                        SCREEN_SIZE[0] // 2 - self.tela_game_over.get_width() // 2,
                        SCREEN_SIZE[1] // 2 - self.tela_game_over.get_height() // 2,
                    ),
                )
                self.button_group.draw(TELA)

            pygame.display.flip()

        # encerra loop da tela atual com break e inicia o proximo
        # self.menu.mainloop()
