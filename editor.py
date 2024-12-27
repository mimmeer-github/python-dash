import pygame

pygame.init()

canvas = pygame.display.set_mode((768, 500), pygame.RESIZABLE)
pygame.display.set_caption("Python Dash - INSERT LEVEL NAME")
player_image = pygame.image.load("resources/player.png")
background = pygame.image.load("resources/bg-0.png")
background = pygame.transform.scale(background, (1512, 1512))
floor_image = pygame.image.load("resources/g-0.png")
clock = pygame.time.Clock()
sprite_sheet = pygame.image.load("resources/assets.png")
camera_y = 0
camera_x = 0

sprite_width = 120
sprite_height = 120

spike_rect = pygame.Rect(0, 0, sprite_width, sprite_height)  # Assuming the spike is the first sprite
spike_image = sprite_sheet.subsurface(spike_rect)

block_rect = pygame.Rect(sprite_width, 0, sprite_width, sprite_height)  # Assuming the orb is the second sprite
block_image = sprite_sheet.subsurface(block_rect)

orb_rect = pygame.Rect((sprite_width * 2), 0, sprite_width, sprite_height)  # Assuming the orb is the second sprite
orb_image = sprite_sheet.subsurface(orb_rect)

pad_rect = pygame.Rect((sprite_width * 3), 0, sprite_width, sprite_height)  # Assuming the orb is the second sprite
pad_image = sprite_sheet.subsurface(pad_rect)

exit = False

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(spike_image, (60, 60)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xpos = x

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(block_image, (60, 60)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xpos = x

class Pad(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pad_image, (60, 12)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 48
        self.xpos = x

selected_object = None  # Keep track of the currently selected object type

exit = False
placed_objects = []  # List to store placed objects

while not exit:
    winx, winy = canvas.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if selected_object:
                # Create a new object instance and place it at mouse position
                new_object = selected_object(mouse_pos[0], mouse_pos[1])
                placed_objects.append(new_object)
    
    num_tiles_needed = (canvas.get_width() + camera_x) // floor_image.get_width() + 1
    num_tiles_needed_bg = (canvas.get_width() + camera_x) // background.get_width() + 1
    
    for i in range(num_tiles_needed_bg):
        canvas.blit(background, (i * background.get_width() - camera_x / 4, 0))
        
    for i in range(num_tiles_needed):
        canvas.blit(floor_image, (i * floor_image.get_width() - camera_x, 400))
        
    for obj in placed_objects:
        canvas.blit(obj.image, obj.rect)
    clock.tick(60)
    pygame.display.update()