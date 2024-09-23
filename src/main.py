import pygame

# entities
from sprites.player import Player
from sprites.enemy import Enemy

# ui
from ui.buttons import Button

from settings import SCREEN_SIZE, GAME_TITLE
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
hud_group = pygame.sprite.Group()

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
def main():
    global spawn_timer
    running = True
    score = 0
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

        # redraw
        tela.fill("black")

        player_group.draw(tela)
        bullets_group.draw(tela)
        enemy_group.draw(tela)

        tela.blit(score_label, (300, 10))
        pygame.display.flip()
    pygame.quit()


# janela de menu
def menu():
    running = True
    background_color = (128, 0, 0)

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


if __name__ == "__main__":
    menu()
