import pygame, sys
from settings import * # Imports setting using "*" as everything in the file.
from level import Level

class Game:
    def __init__(self):

        # general setup
        pygame.init() # Initalize pygame module.
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH)) # Surface for pygame module with WIDTH & HEIGHT.
        pygame.display.set_caption("Python Zelda")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        # Event Loop
        #Key Handlers
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__': # Check if this is the main file.
    game = Game() # Creates a instance of Game Class.
    game.run() # Run Game instance.