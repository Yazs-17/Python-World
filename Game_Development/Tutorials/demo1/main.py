import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
text_surface = test_font.render('My game',False,'Black')

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_x_pos = 600
snail_rect = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        " 1h14min' "
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         print('jump')

    screen.blit(ground_surface,(0,300))
    screen.blit(sky_surface,(0,0))
    screen.blit(text_surface,(300,50))

    screen.blit(snail_surface, snail_rect)
    snail_rect.x -= 4 # snail_rect.left -= 4
    if snail_rect.left <= -100:
        snail_rect.left = 800
    # player_rect.left += 1
    screen.blit(player_surface,player_rect)

    # if player_rect.colliderect(snail_rect):
    #     print('collision')

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        # print('collision')
        print(pygame.mouse.get_pressed())
    pygame.display.update()
    clock.tick(60)