# 

import os

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from pygame.sprite import Group
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


class Wall(GameObject):
    sprite_filename = 'wall'
    # sprite_filename = 'wooden'

    def calculate_walls_coordinates(self, screen_width: int, screen_height: int) -> list[list[int]]:
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


class Maze(GameObject):
    sprite_filename = 'wooden'

    def calculate_maze(self, screen_width: int, screen_height: int) -> list[list[int]]:
        center = screen_width // 2, screen_height // 2
        maze_coordinates = []

        for x in range(self.width, center[0]-self.width, self.width*2):
            maze_coordinates.extend([
                [center[0]-x, center[1]+self.width],
                [center[0]+x, center[1]+self.width],
                [center[0]-x, center[1]-self.width],
                [center[0]+x, center[1]-self.width],
            ])

        for x in range(self.width, center[1]-self.width, self.width*2):
            maze_coordinates.extend([
                [center[0]-self.width, center[1]-x],
                [center[0]-self.width, center[1]+x],
                [center[0]+self.width, center[1]-x],
                [center[0]+self.width, center[1]+x],
            ])

        return maze_coordinates


class Background(GameObject):
    sprite_filename = 'carpet'

    def __init__(self, topleft_x: int, topleft_y: int) -> None:
        super().__init__(topleft_x, topleft_y)
        sprite_image_full_path = os.path.join(
            'resources',
            f'{self.sprite_filename}.{self.sprite_extension}'
            )
        self.image = load(sprite_image_full_path)


class Player(GameObject):
    sprite_filename = 'player'
    player_speed = 5


class Cheese(GameObject):
    sprite_filename = 'cheese'


class Monster(GameObject):
    sprite_filename = 'monster'
    monster_speed = 5

