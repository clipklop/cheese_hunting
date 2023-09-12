# 

import os

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import spritecollide 
from pygame.transform import scale



class GameObject(Sprite):
    sprite_filename: str | None = None
    sprite_extension: str = 'png'
    width: int = 40
    height: int = 40
    color_key: tuple[int, int, int] = (245, 245, 245)

    def __init__(self, topleft_x: int, topleft_y: int) -> None:
        super().__init__()
        sprite_image_full_path = os.path.join(
            'resources',
            f'{self.sprite_filename}.{self.sprite_extension}'
            )
        self.image = scale(load(sprite_image_full_path), (self.width, self.height))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_x, topleft_y
    
    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_collided_with(self, another_object: "GameObject") -> bool:
        return self.rect.colliderect(another_object.rect)


class Maze(GameObject):
    sprite_filename = 'wooden'

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


class Background(GameObject):
    # bg_full_path = os.path.join('resources', 'carpet.png')
    
    # def __init__(self, topleft_x: int, topleft_y: int) -> None:
    #     super().__init__(topleft_x, topleft_y)
    #     self.image = load(self.sprite_image_full_path)
    # #     self.rect = self.image.get_rect()
    # #     self.rect.left, self.rect.top = location
    # def draw(self, surface: Surface) -> None:
    #     surface.blit(self.image, (self.rect.x, self.rect.y))

    sprite_filename = 'carpet'
    sprite_extension: str = 'png'

    def __init__(self, topleft_x: int, topleft_y: int) -> None:
        super().__init__(topleft_x, topleft_y)
        sprite_image_full_path = os.path.join(
            'resources',
            f'{self.sprite_filename}.{self.sprite_extension}'
            )
        self.image = load(sprite_image_full_path)
    
    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
