import pygame
import playLayer

pygame.init()

canvas = pygame.display.set_mode((768, 500), pygame.RESIZABLE)
pygame.display.set_caption("Python Dash")
sprite_sheet = pygame.image.load("resources/menu.png")
color = (0, 102, 252, 255)
background = pygame.image.load("resources/bg-0.png")
exit = False
logo_rect = pygame.Rect((718), 0, 1895, 213)
play_button_rect = pygame.Rect((280), 0, 438, 438)


def getCentre(width):
    winx, winy = canvas.get_size()
    centrex = winx - width
    return centrex / 2

def getCentreY(width):
    winx, winy = canvas.get_size()
    centrey = winy - width
    return centrey / 2

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                print("Clicked! Loading...")
                playLayer.play_game(canvas, 0)
    winx, winy = canvas.get_size()
    width_x = winx - 50
    if width_x > 1000:
        width_x = 1000
    height_y = width_x / 8.9
    position = (getCentre(width_x), 0)
    logo_image = pygame.transform.scale(sprite_sheet.subsurface(logo_rect), (width_x, height_y))
    width_x = winx - 200
    width_x = width_x / 2.4
    if width_x > 340:
        width_x = 340
    height_y = width_x
    playPosition = (getCentre(width_x), getCentreY(height_y))
    play_button_image = pygame.transform.scale(sprite_sheet.subsurface(play_button_rect), (width_x, height_y))
    canvas.blit(background, (0, 0))
    canvas.blit(logo_image, dest=position)
    canvas.blit(play_button_image, dest=playPosition)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    pygame.display.update()