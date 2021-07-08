import pygame
from settings import *

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.chomp = pygame.mixer.Sound('sound/chomp.ogg')
        self.death_sound = pygame.mixer.Sound('sound/death.ogg')
        self.sprite_sheet = pygame.image.load('sprites/spritesheet.png').convert()
        self.sprite_list = []
        self.image = None
        self.current_sprite = 0
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        pygame.mixer.Sound.stop(self.chomp)
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction

            self.sprite_list = []
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        if self.on_coin():
            pygame.mixer.Sound.play(self.chomp)
            self.eat_coin()

        if self.current_sprite >= len(self.sprite_list):
            self.current_sprite = 0
        else:
            self.current_sprite += 0.2

    def draw(self):

        if self.direction == vec(0, 0):  # not moving:
            self.sprite_list.append(self.get_sprite(209, 105, 50, 50))

        if self.direction == vec(-1, 0):  # left
            self.sprite_list.append(self.get_sprite(53, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(105, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(53, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(209, 105, 50, 50))

        if self.direction == vec(1, 0):  # right
            self.sprite_list.append(self.get_sprite(157, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(209, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(157, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(209, 105, 50, 50))

        if self.direction == vec(0, 1):  # down
            self.sprite_list.append(self.get_sprite(261, 105, 50, 50))
            self.sprite_list.append(self.get_sprite(1, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(261, 105, 50, 50))
            self.sprite_list.append(self.get_sprite(209, 105, 50, 50))

        if self.direction == vec(0, -1):  # up
            self.sprite_list.append(self.get_sprite(261, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(1, 205, 50, 50))
            self.sprite_list.append(self.get_sprite(261, 157, 50, 50))
            self.sprite_list.append(self.get_sprite(209, 105, 50, 50))

        self.image = self.sprite_list[int(self.current_sprite)]

        self.app.screen.blit(self.image, ((int(self.pix_pos.x) - 15),
                                          (int(self.pix_pos.y) - 15)))

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, (255, 255, 0), (30 + 20 * x, HEIGHT - 15), 7)

        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, pygame.Rect(-x, -y, w, h))
        sprite = pygame.transform.scale(sprite, (30, 30))
        return sprite

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        pos = (self.pix_pos.x, self.pix_pos.y)
        if pos <= LEFT_BOUNDARY:  # teleports to the right
            self.pix_pos.x = RIGHT_BOUNDARY[0]
            self.pix_pos.y = RIGHT_BOUNDARY[1]
        if pos >= RIGHT_BOUNDARY:  # teleports to the left
            self.pix_pos.x = LEFT_BOUNDARY[0]
            self.pix_pos.y = LEFT_BOUNDARY[1]

        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
