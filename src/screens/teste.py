import pygame

pygame.init()

# Criando a tela
screen = pygame.display.set_mode((800, 600))

# Criando uma superfície para o círculo
circle_surface = pygame.Surface((300, 300))
circle_surface.fill((255, 255, 255))  # Preenchendo com branco

# Desenhando o círculo na superfície
pygame.draw.circle(
    circle_surface, (0, 0, 255), (150, 150), 100
)  # Círculo azul com raio 100 no centro

# Posicionando a superfície na tela
screen.blit(circle_surface, (250, 150))

# Atualizando a tela
pygame.display.flip()

# Loop principal do jogo (simplificado)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
