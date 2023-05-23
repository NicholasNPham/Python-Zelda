import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Graphics Setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement
        self.direction = pygame.math.Vector2() # Initalize (x,y)
        self.speed = 5 # Determines how fast the player is moving.
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
                           'right_idle':[], 'left_idle':[], 'up_idle':[], 'down_idle':[],
                           'right_attack':[], 'left_attack':[], 'up_attack':[], 'down_attack':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            """
            Key Handlers.
            The most topleft corner of "World Map" coordinate (0,0), whilst the Player is in Coordinates (2 * 64, 2 * 64).
            The player is set a positive x and a positive y. (Y Coords are reversed). -1 means going up. 
            """
            # Movement Input.
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Attack input.
            if keys[pygame.K_SPACE]: # Check if key is press and is not attacking.
                self.attacking = True # Initial variable is set to false. If key is pressed, attacking is now true.
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            #Magic Input.
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        # Idle Status.
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        #Attacking Status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if self.direction.x == 0 and self.direction.y == 0:
                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        # Override idle.
                        self.status = self.status.replace('_idle', '_attack')
                    else:
                        self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self, speed):
        if self.direction.magnitude() != 0: # Check if vector has any length.
            self.direction = self.direction.normalize() # If magnitude does have length, set to 1 constantly.

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal': # Check Direction.
            for sprite in self.obstacle_sprites: # all sprites in obstacle_sprites.
                if sprite.hitbox.colliderect(self.hitbox): # For all sprites, check the rectangle of sprite with the player.
                    if self.direction.x > 0: # Moving Right.
                        self.hitbox.right = sprite.hitbox.left # Player moving right colliding with the left side of sprite.
                    if self.direction.x < 0: # Moving Left.
                        self.hitbox.left = sprite.hitbox.right # Player moving left colliding with the right side of sprite.

        if direction == "vertical":
            for sprite in self.obstacle_sprites: # all sprites in obstacle_sprites.
                if sprite.hitbox.colliderect(self.hitbox): # For all sprites, check the rectangle of sprite with the player.
                    if self.direction.y > 0: # Moving Down
                        self.hitbox.bottom = sprite.hitbox.top # Player moving down colliding with the top side of sprite.
                    if self.direction.y < 0: # Moving Up
                        self.hitbox.top = sprite.hitbox.bottom # Player moving up colliding with the bottom side of sprite.

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time > self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        # Loop over the frame index.
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image.
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
