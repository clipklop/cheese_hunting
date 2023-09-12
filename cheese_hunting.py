#

import os
import random 

import pygame
from pygame.sprite import Group
from pygame.sprite import spritecollide 

from text import Text
from game_objects import GameObject, Maze, Background

# os.environ['SDL_AUDIODRIVER'] = 'dsp'


class Wall(GameObject):
    sprite_filename = 'wall'
    # sprite_filename = 'wooden'

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
    
    def calculate_maze(self, screen_width, screen_height):
        center = screen_width // 2, screen_height // 2
        maze_coordinates = []

        for x in range(self.width, center[0]-self.width, self.width*2):
            maze_coordinates.append([center[0]-x, center[1]+self.width])
            maze_coordinates.append([center[0]+x, center[1]+self.width])

        for x in range(self.width, center[0], self.width*2):
            maze_coordinates.append([center[0]-x, center[1]+self.width])
            maze_coordinates.append([center[0]+x, center[1]+self.width])

        for x in range(self.width, center[1]-self.width, self.width*2):
            maze_coordinates.append([center[0]-self.width, center[1]-x])
            maze_coordinates.append([center[0]-self.width, center[1]+x])

        for x in range(self.width, center[1], self.width*2):
            maze_coordinates.append([center[0]+self.width, center[1]-x])
            maze_coordinates.append([center[0]+self.width, center[1]+x])

        return maze_coordinates


class Player(GameObject):
    sprite_filename = 'player'
    player_speed = 5


class Cheese(GameObject):
    sprite_filename = 'cheese'


def draw_whole_screen(screen, context):
    # fill the screen with a background
    # screen.fill('salmon')
    # bg = Background((0, 0))
    # screen.blit(bg.image, bg.rect)
    # bg = Background(0, 0)
    # screen.blit(bg.image, bg.rect)
    context['background'].draw(screen)
    
    # draw a character
    context['player'].draw(screen)

    # draw a cheese
    context['cheese'].draw(screen)

    # draw walls
    context['wall'].draw(screen)

    # draw maze
    context['maze'].draw(screen)
    # [w.draw(screen) for w in context['wall']]

    # draw score
    Text(str(context['score']), (screen.get_width() - 60, 10)).draw(screen)


def compose_context(screen):
    walls = Wall(0, 0)
    walls_coordinates = walls.calculate_walls_coordinates(screen.get_width(), screen.get_height())
    walls_maze = walls.calculate_maze(screen.get_width(), screen.get_height())
    return {
        'background': Background(0, 0),
        'player': Player(screen.get_width() // 2, screen.get_height() // 2),
        'cheese': Cheese(100,100),
        'wall': Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        'maze': Group(*[Wall(x, y) for (x, y) in walls_maze]),
        'score': 0
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
        
        if spritecollide(context['player'], context['maze'], dokill=False):
            context['player'].rect.topleft = old_player_topleft

        if context['player'].is_collided_with(context['cheese']):
            context['score'] += 1
            context['cheese'].rect.topleft = (
                random.randint(Wall.width, screen.get_width() - Wall.width * 2),
                random.randint(Wall.height, screen.get_height() - Wall.height * 2),
            )

        # limits FPS
        clock.tick(60) / 1000


    pygame.quit()


if __name__ == '__main__':
    main()
