#

import os
import random 

import pygame
from pygame import Surface
from pygame.sprite import Group
from pygame.sprite import spritecollide 

from text import Text
from game_objects import Wall, Maze, Background, Player, Cheese, Monster


def draw_whole_screen(screen: Surface, context: dict[str]) -> None:
    # fill the screen with a background
    context['background'].draw(screen)
    
    # draw a character
    context['player'].draw(screen)

    # draw a monster
    context['monster'].draw(screen)    

    # draw a cheese
    context['cheese'].draw(screen)

    # draw walls
    context['wall'].draw(screen)

    # draw maze
    context['maze'].draw(screen)

    # draw score
    Text(str(context['score']), (screen.get_width() - 60, 10)).draw(screen)


def compose_context(screen: Surface) -> dict[str]:
    walls = Wall(0, 0)
    walls_coordinates = walls.calculate_walls_coordinates(screen.get_width(), screen.get_height())
    
    maze = Maze(0, 0)
    maze_coordinates = maze.calculate_maze(screen.get_width(), screen.get_height())
    
    return {
        'score': 0,
        'background': Background(0, 0),
        'player': Player(screen.get_width() // 2, screen.get_height() // 2),
        'monster': Monster(80, 80),
        'cheese': Cheese(40,40),
        'wall': Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        'maze': Group(*[Maze(x, y) for (x, y) in maze_coordinates]),
    }


def player_move(player: Player) -> None:
    # add support of WASD and arrows keys for character moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.rect = player.rect.move(0, -1 * player.player_speed)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.rect = player.rect.move(0, player.player_speed)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.rect = player.rect.move(-1 * player.player_speed, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.rect = player.rect.move(player.player_speed, 0)


def monster_move(player: Player, monster: Monster) -> None:
    # Move the enemy randomly on the screen
    direction = random.choice(['left', 'right', 'up', 'down', 'to_player'])

    if direction == 'left':
        monster.rect = monster.rect.move(-1 * monster.monster_speed, 0)
    elif direction == 'right':
        monster.rect = monster.rect.move(monster.monster_speed, 0)
    elif direction == 'up':
        monster.rect = monster.rect.move(0, -1 * monster.monster_speed)
    elif direction == 'down':
        monster.rect = monster.rect.move(0, monster.monster_speed)
    if direction == 'to_player':
        # Calculate the distance between the enemy and the player
        distance_x = player.rect.x - monster.rect.x
        distance_y = player.rect.y - monster.rect.y

        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        
        if distance != 0:
            monster.rect.x += monster.monster_speed * distance_x / distance
            monster.rect.y += monster.monster_speed * distance_y / distance    


def main():
    # game setup
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    screen_center = (screen.get_width() // 2, screen.get_height() // 2)
    clock = pygame.time.Clock()
    running = True
    
    context = compose_context(screen)

    player = context['player']
    monster = context['monster']
    cheese = context['cheese']
    walls = context['wall']
    maze = context['maze']

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)

        # flip or display everything on the screen
        pygame.display.flip()

        old_player_topleft = player.rect.topleft
        old_cheese_topleft = cheese.rect.topleft
        old_monster_topleft= monster.rect.topleft

        player_move(player=player)

        monster_move(player=player, monster=monster)    

        if spritecollide(player, context['wall'], dokill=False):
            context['player'].rect.topleft = old_player_topleft
        
        if spritecollide(context['player'], context['maze'], dokill=False):
            context['player'].rect.topleft = old_player_topleft

        if player.is_collided_with(cheese):
            context['score'] += 1
            cheese.rect.topleft = (
                random.randint(Wall.width, screen.get_width() - Wall.width * 2),
                random.randint(Wall.height, screen.get_height() - Wall.height * 2),
            )

        if monster.is_collided_with(cheese):
            monster.rect.topleft = old_monster_topleft

        if spritecollide(cheese, maze, dokill=False):
            cheese.rect.topleft = old_cheese_topleft
        
        # if spritecollide(monster, maze, dokill=False):
        #     monster.rect.topleft = old_monster_topleft

        if spritecollide(monster, walls, dokill=False):
            monster.rect.topleft = old_monster_topleft        



        # limits FPS
        clock.tick(60) / 1000


    pygame.quit()


if __name__ == '__main__':
    main()
