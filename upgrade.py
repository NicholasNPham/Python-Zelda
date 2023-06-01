import pygame
from settings import *

class Upgrade:
    def __init__(self, player):

        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Item Creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # Selection System
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []
        for item, index in enumerate(range(self.attribute_nr)):
            # Horizontal Position.
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            # Vertical Postion.
            top = self.display_surface.get_size()[1] * 0.1

            # Create the Object.
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        self.input()
        self.selection_cooldown()

        for item in self.item_list:
            item.display(self.display_surface, 0, 'test', 1, 2, 3)


class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

    def display(self, surface, selection_num, name, value, max_value, cost):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)