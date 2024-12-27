import pygame

def play_game(canvas, level_data):
    """
    Runs the main game loop.

    Args:
        canvas: The pygame display surface.
        level_data: A dictionary containing level data (e.g., objects, positions).
    """

    player_image = pygame.image.load("resources/player.png")
    background = pygame.image.load("resources/bg-0.png")
    background = pygame.transform.scale(background, (1512, 1512))
    floor_image = pygame.image.load("resources/g-0.png")
    player_y = 0
    speed_y = 0
    jump_height = 18
    camera_y = 0
    camera_x = 0
    clock = pygame.time.Clock()
    sprite_sheet = pygame.image.load("resources/assets.png")
    scroll_speed = 10
    player_direction = 0

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
    isTouchingG = False
    prev_touch = False
    
    spikes = pygame.sprite.Group()
    spikes.add(Spike(getBlockX(4), getBlockY(0)))
    blocks = pygame.sprite.Group()
    blocks.add(Spike(getBlockX(4), getBlockY(0)))
    blocks.add(Block(getBlockX(5), getBlockY(0)))
    blocks.add(Block(getBlockX(6), getBlockY(0)))
    blocks.add(Block(getBlockX(7), getBlockY(0)))
    pads = pygame.sprite.Group()
    pads.add(Pad(getBlockX(3), getBlockY(0)))
    running = True
    toJump = False
    while running:
        toJump = False
        winx, winy = canvas.get_size()
        player_surface = pygame.Surface(player_image.get_size(), pygame.SRCALPHA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                toJump = True
        player_rect = player_surface.get_rect()
        player_rect.x = 100
        player_rect.y = 340 - player_y
        
        player_y = player_y + speed_y
        speed_y = speed_y - 1.2
        # Clamp player_y to prevent falling through the floor
        if player_y < 0:
            player_y = 0
            speed_y = 0
            isTouchingG = True
            if toJump:
                speed_y = jump_height
                isTouchingG = False

        # Update camera position
        camera_y = player_y - 200

        # Clamp camera_y to prevent scrolling too far
        camera_y = max(0, camera_y)
        camera_x = camera_x + scroll_speed

        # Draw background
        canvas.blit(background, (0-(camera_x / 2), camera_y))
        
        num_tiles_horizontal = winx // 512 + 1  # Add 1 for potential overlap
        num_tiles_vertical = 1  # Assuming 1 row of tiles for now
        num_tiles_needed = (canvas.get_width() + camera_x) // floor_image.get_width() + 1
        num_tiles_needed_bg = (canvas.get_width() + camera_x) // background.get_width() + 1
        
        for i in range(num_tiles_needed_bg):
            canvas.blit(background, (i * background.get_width() - camera_x / 4, 0))
        for i in range(num_tiles_needed):
            canvas.blit(floor_image, (i * floor_image.get_width() - camera_x, 400))
        for spike in spikes:
            spike.rect.x = spike.xpos - camera_x
            if player_rect.colliderect(spike.rect):
                player_y = 0
                speed_y = 0
                camera_x = 0
                camera_y = 0
                isTouchingG = False
        
        for block in blocks:
            block.rect.x = block.xpos - camera_x
            if player_rect.colliderect(block.rect):
                prev_touch = True
                isTouchingG = True
                if toJump:
                    speed_y = jump_height
                    isTouchingG = False
                player_y = fixYPos(player_y, block)
            elif prev_touch:
                prev_touch = False
                isTouchingG = False
        
        for pad in pads:
            pad.rect.x = pad.xpos - camera_x
            if player_rect.colliderect(pad.rect):
                prev_touch = False
                isTouchingG = False
                speed_y = jump_height + jump_height / 3
        
        if isTouchingG:
            player_direction = round(player_direction / 90) * 90
        else:
            player_direction = player_direction - 5
    
        spikes.draw(canvas)
        blocks.draw(canvas)
        pads.draw(canvas)
        rotated_player_surface = pygame.transform.rotate(player_image, player_direction)
        player_rect = rotated_player_surface.get_rect(center=player_rect.center) 
        canvas.blit(rotated_player_surface, player_rect)
        clock.tick(60)
        pygame.display.update()

def fixYPos(y, block):
    origin_y = y
    while player_rect.colliderect(block.rect):
        origin_y += 1
        player_rect.y = 340 - origin_y
    return origin_y

def getBlockX(x):
    mul_x = x * 60
    new_x = mul_x + 520
    return new_x

def getBlockY(y):
    new_y = y + 340
    return new_y