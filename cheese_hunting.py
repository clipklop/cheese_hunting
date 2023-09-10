#

import os 

import pygame

from game_object import GameObject

# os.environ['SDL_AUDIODRIVER'] = 'dsp'


class Wall(GameObject):
    sprite_filename = 'wall'


class Player(GameObject):
    sprite_filename = 'player'
    player_speed = 3


def draw_whole_screen(screen, context):
    # fill the screen with a color
    screen.fill('salmon')
    
    # draw a character
    context['player'].draw(screen)

    # draw walls
    context['wall'].draw(screen)


def compose_context(screen):
    return {
        'player': Player(screen.get_width() // 2, screen.get_height() // 2),
        'wall': Wall(100, 100)
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            context['player'].rect = context['player'].rect.move(0, -1 * player.player_speed)
        if keys[pygame.K_s]:
            context['player'].rect = context['player'].rect.move(0, player.player_speed)
        if keys[pygame.K_a]:
            context['player'].rect = context['player'].rect.move(-1 * player.player_speed, 0)
        if keys[pygame.K_d]:
            context['player'].rect = context['player'].rect.move(player.player_speed, 0)

        # limits FPS
        dt = clock.tick(60) / 1000


    pygame.quit()


if __name__ == '__main__':
    main()
