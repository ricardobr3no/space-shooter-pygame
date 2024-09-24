import pygame

# entities
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.wall import Wall

# ui
from ui.buttons import Button
from config.settings import SCREEN_SIZE, GAME_TITLE

# math
from random import choice, randint


pygame.init()

tela = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
spawn_timer = 0  # spawn
font = pygame.font.SysFont(name="comic sans", size=32)
# font = pygame.font.Font(None, 34)


# groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

# entities
player = Player()
player_group.add(player)

# paredes invisiveis
wall_1 = Wall(0, 0, SCREEN_SIZE[0], 1)
wall_2 = Wall(0, SCREEN_SIZE[1], SCREEN_SIZE[0], 1)
wall_3 = Wall(0, 0, 1, SCREEN_SIZE[1])
wall_4 = Wall(SCREEN_SIZE[0], 0, 1, SCREEN_SIZE[1])
walls_group.add(wall_1, wall_2, wall_3, wall_4)


def spawn_enemys(spawn_rate: float, dt: float):
    global spawn_timer
    spawn_timer += dt
    if spawn_timer >= spawn_rate:
        spawn_range_x = choice((-30, SCREEN_SIZE[0] + 30))
        spawn_range_y = choice((-20, SCREEN_SIZE[1] + 30))

        new_enemy = Enemy(spawn_range_x, spawn_range_y, player)
        enemy_group.add(new_enemy)
        spawn_timer = 0


# janela do jogo
def main():
    global spawn_timer
    running = True
    score = 0
    score_label = font.render(f"{score}", True, "white")
    player_last_position = player.rect.x, player.rect.y

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

        wall_colission = pygame.sprite.groupcollide(
            # verifica se atigiu uma parede
            walls_group,
            player_group,
            dokilla=False,
            dokillb=False,
        )

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
            score += 1
            score_label = font.render(f"{score}", True, "white")
            # print(score)

        if game_over:
            bullets_group.empty()
            enemy_group.empty()
            player.restart()
            score = 0
            score_label = font.render(f"{score}", True, "white")
            spawn_timer = 0

        if wall_colission:
            player.rect.x, player.rect.y = player_last_position
        else:
            player_last_position = player.rect.x, player.rect.y

        # redraw
        tela.fill("midnightblue")

        player_group.draw(tela)
        bullets_group.draw(tela)
        enemy_group.draw(tela)

        tela.blit(score_label, (SCREEN_SIZE[0] // 2, 10))
        pygame.display.flip()
    pygame.quit()


# janela de menu
def menu():
    running = True
    background_color = (128, 0, 0)

    texto_menu = font.render("MENU", False, "yellow")
    screen_width = SCREEN_SIZE[0] / 2
    button_width, button_heigth = 200, 40
    button_x = screen_width // 2 + button_width // 4
    button_color = "blue"

    # buttons
    button1 = Button(
        button_x,
        150,
        button_width,
        button_heigth,
        button_color,
        "start",
        lambda: main(),
    )
    button2 = Button(
        button_x,
        250,
        button_width,
        button_heigth,
        button_color,
        "credits",
        lambda: print("credits"),
    )
    button3 = Button(
        button_x,
        350,
        button_width,
        button_heigth,
        button_color,
        "exit",
        lambda: pygame.quit(),
    )
    button_group.add(button1, button2, button3)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # verifica qual botao foi pressionado e em seguida aciona sua respectiva funcao
                mouse_pos = pygame.mouse.get_pos()
                for button in button_group.sprites():
                    if button.is_clicked(mouse_pos):
                        button.function()
                        print("saindo..")

        # logic
        button_group.update()

        # redraw
        tela.fill(background_color)
        tela.blit(texto_menu, (screen_width // 2 + texto_menu.get_size()[0], 50))
        button_group.draw(tela)

        # tela.blit(button1, (300, 200))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    menu()
