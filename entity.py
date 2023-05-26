import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2() # Initalize (x,y)

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