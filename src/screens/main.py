import pygame
from pygame.time import Clock
from random import randint, choice

# entities
from sprites.player import Player
from sprites.enemy import Enemy

# groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# entities
player = Player()
player_group.add(player)


def spawn_enemys(spawn_rate: float, dt: float):
    global spawn_timer
    spawn_timer += dt
    if spawn_timer >= spawn_rate:
        spawn_range_x = choice([randint(-20, -10), randint(610, 620)])
        spawn_range_y = randint(-20, 620)

        new_enemy = Enemy(spawn_range_x, spawn_range_y, player)
        enemy_group.add(new_enemy)
        spawn_timer = 0


# janela do jogo
def main(tela):
    global spawn_timer
    running = True
    score = 0
    clock = Clock()
    font = pygame.font.SysFont(name="comic sans", size=32)

    score_label = font.render(f"{score}", True, "white")

    while running:
        dt = clock.tick(60) / 1_000

        spawn_enemys(1.3, dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullets_group.add(player.shoot_bullet())

        # update
        player_group.update(dt)
        bullets_group.update(dt)
        enemy_group.update(dt)

        acertou = pygame.sprite.groupcollide(
            bullets_group,
            enemy_group,
            dokilla=True,
            dokillb=True,
        )
        game_over = pygame.sprite.groupcollide(
            player_group,
            enemy_group,
            dokilla=False,
            dokillb=False,
        )

        if acertou:
            # verfica se projetil colidiu com inimigo
            score += 1
            score_label = font.render(f"{score}", True, "white")

        if game_over:
            # verficar game_over. Se inimigo colidir com player
            bullets_group.empty()
            enemy_group.empty()
            player.restart()
            score = 0
            score_label = font.render(f"{score}", True, "white")
            spawn_timer = 0

        # redraw
        tela.fill("black")

        player_group.draw(tela)
        bullets_group.draw(tela)
        enemy_group.draw(tela)

        tela.blit(score_label, (300, 10))
        pygame.display.flip()
    pygame.quit()
