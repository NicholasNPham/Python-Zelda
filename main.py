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

        # Sound
        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

    def run(self):
        # Event Loop
        #Key Handlers
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__': # Check if this is the main file.
    game = Game() # Creates a instance of Game Class.
    game.run() # Run Game instance.