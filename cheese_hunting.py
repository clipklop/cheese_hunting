#

import os 

import pygame
from pygame.sprite import Group
from pygame.sprite import spritecollide

from game_object import GameObject

# os.environ['SDL_AUDIODRIVER'] = 'dsp'


class Wall(GameObject):
    # sprite_filename = 'wall'
    sprite_filename = 'wooden'

    def calculate_walls_coordinates(self, screen_width, screen_height):
        horizontal_wall_blocks_amount = screen_width // self.width
        vertical_wall_blocks_amount = screen_height // self.height

        walls_coordinates = []
        for block_num in range(horizontal_wall_blocks_amount):
            walls_coordinates.extend([
                (block_num * self.width, 0),
                (block_num * self.width, screen_height - self.height)
            ])
        for block_num in range(vertical_wall_blocks_amount):
            walls_coordinates.extend([
                (0, block_num * self.height),
                (screen_width - self.width, block_num * self.height),
            ])        

        return walls_coordinates


class Background(pygame.sprite.Sprite):
    bg_full_path = os.path.join('resources', 'carpet.png')

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.bg_full_path)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(GameObject):
    sprite_filename = 'player'
    player_speed = 2.5


def draw_whole_screen(screen, context):
    # fill the screen with a background
    # screen.fill('salmon')
    bg = Background((0, 0))
    # screen.fill([255, 255, 255])
    screen.blit(bg.image, bg.rect)
    
    # draw a character
    context['player'].draw(screen)

    # draw walls
    context['wall'].draw(screen)
    # [w.draw(screen) for w in context['wall']]


def compose_context(screen):
    walls = Wall(0, 0)
    walls_coordinates = walls.calculate_walls_coordinates(screen.get_width(), screen.get_height())

    return {
        'player': Player(screen.get_width() // 2, screen.get_height() // 2),
        'wall': Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
    }


def main():
    # game setup
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    screen_center = (screen.get_width() // 2, screen.get_height() // 2)
    clock = pygame.time.Clock()
    running = True
    
    context = compose_context(screen)

    player = Player(*screen_center)

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        draw_whole_screen(screen, context)

        # flip or display everything on the screen
        pygame.display.flip()

        old_player_topleft = context['player'].rect.topleft

        # add support of WASD and arrows keys for character moving
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            context['player'].rect = context['player'].rect.move(0, -1 * player.player_speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            context['player'].rect = context['player'].rect.move(0, player.player_speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            context['player'].rect = context['player'].rect.move(-1 * player.player_speed, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            context['player'].rect = context['player'].rect.move(player.player_speed, 0)

        if spritecollide(context['player'], context['wall'], dokill=False):
            context['player'].rect.topleft = old_player_topleft

        # limits FPS
        clock.tick(60) / 1000


    pygame.quit()


if __name__ == '__main__':
    main()
