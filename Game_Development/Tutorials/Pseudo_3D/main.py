import pygame
import math

# Define constants
screenWidth = 800
screenHeight = 600
w = 800
h = 600

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Raycaster")

# Define colors (assuming RGB_* are tuples representing colors)
RGB_Red = (255, 0, 0)
RGB_Green = (0, 255, 0)
RGB_Blue = (0, 0, 255)
RGB_White = (255, 255, 255)
RGB_Yellow = (255, 255, 0)
# Initialize variables
posX, posY = 22, 12
dirX, dirY = -1, 0        #  initial direction vector
planeX, planeY = 0, 0.66  #   the 2d raycaster version of camera plane
worldMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
def done():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False
def verLine(x, drawStart, drawEnd, color):
    pygame.draw.line(screen, color, (x, drawStart), (x, drawEnd))
    # pygame.draw.line(screen, color, (x, drawStart), (x, drawEnd))
def print_fps(fps):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
# Main loop
oldTime = 0
time = 0
while not done():
    time = pygame.time.get_ticks()
    # w: width of screen: 800
    for x in range(w):
        cameraX = 2 * x / w - 1 # x-coordinate in camera space
        rayDirX = dirX + planeX * cameraX # direction of ray
        rayDirY = dirY + planeY * cameraX

        mapX, mapY = int(posX), int(posY)

        if rayDirX == 0:
            deltaDistX = 1e30
        else:
            deltaDistX = abs(1 / rayDirX)

        if rayDirY == 0:
            deltaDistY = 1e30
        else:
            deltaDistY = abs(1 / rayDirY)

        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX

        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        hit = False
        side = 0
        while not hit:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            if worldMap[mapX][mapY] > 0:
                hit = True

        if side == 0:
            perpWallDist = (sideDistX - deltaDistX)
        else:
            perpWallDist = (sideDistY - deltaDistY)

        lineHeight = int(h / perpWallDist)

        drawStart = -lineHeight // 2 + h // 2
        if drawStart < 0:
            drawStart = 0
        drawEnd = lineHeight // 2 + h // 2
        if drawEnd >= h:
            drawEnd = h - 1

        # Determine color based on wall type
        wall_type = worldMap[mapX][mapY]
        if wall_type == 1:
            color = RGB_Red
        elif wall_type == 2:
            color = RGB_Green
        elif wall_type == 3:
            color = RGB_Blue
        elif wall_type == 4:
            color = RGB_White
        else:
            color = RGB_Yellow

        # Darken color for side walls
        if side == 1:
            color = tuple(c // 2 for c in color)

        # Draw vertical line
        verLine(x, drawStart, drawEnd, color)

    pygame.display.flip()

    # Handle movement and rotation
    oldTime = time
    time = pygame.time.get_ticks()
    frameTime = (time - oldTime) / 1000.0

    moveSpeed = frameTime * 5.0
    rotSpeed = frameTime * 3.0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if worldMap[int(posX + dirX * moveSpeed)][int(posY)] == 0:
            posX += dirX * moveSpeed
        if worldMap[int(posX)][int(posY + dirY * moveSpeed)] == 0:
            posY += dirY * moveSpeed

    if keys[pygame.K_DOWN]:
        if worldMap[int(posX - dirX * moveSpeed)][int(posY)] == 0:
            posX -= dirX * moveSpeed
        if worldMap[int(posX)][int(posY - dirY * moveSpeed)] == 0:
            posY -= dirY * moveSpeed

    if keys[pygame.K_RIGHT]:
        oldDirX = dirX
        dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
        dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
        planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)

    if keys[pygame.K_LEFT]:
        oldDirX = dirX
        dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
        dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
        planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)

    print_fps(1.0 / frameTime)
    screen.fill((0, 0, 0))

pygame.quit()
