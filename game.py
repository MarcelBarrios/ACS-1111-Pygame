#!/usr/bin/python
# -*- coding: utf-8 -*-
# Example 2

# Import and initialize pygame

import pygame
import time
import math
from random import randint, choice
pygame.init()

# Get the clock

clock = pygame.time.Clock()

# Configure the screen

screen = pygame.display.set_mode([500, 500])

# Make a group

all_sprites = pygame.sprite.Group()


# Game Object
# Game Object

class GameObject(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        image,
        ):
        super(GameObject, self).__init__()
        self.surf = pygame.image.load(image)
        self.surf = self.surf.convert_alpha()  
        self.mask = pygame.mask.from_surface(self.surf)
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect()  # add

    def render(self, screen):
        self.rect.x = self.x  # add
        self.rect.y = self.y  # add
        screen.blit(self.surf, (self.x, self.y))


class Apple(GameObject):

    def __init__(self):
        super(Apple, self).__init__(0, 0, 'apple.png')
        self.dx = 0
        self.dy = randint(0, 200) / 100 + 1
        self.reset()  # call reset here!

    def move(self):
        self.x += self.dx
        self.y += self.dy

   # Check the y position of the apple

        if self.y > 500:
            self.reset()

 # add a new method

    def reset(self):
        self.x = choice([93, 218, 343])
        self.y = -64


class Strawberry(GameObject):

    def __init__(self):
        super(Strawberry, self).__init__(0, 0, 'strawberry.png')
        self.dx = randint(0, 200) / 100 + 1
        self.dy = 0
        self.reset()  # call reset here!

    def move(self):
        self.x += self.dx
        self.y += self.dy

   # Check the y position of the apple

        if self.x > 500:
            self.reset()

 # add a new method

    def reset(self):
        self.x = -64
        self.y = choice([93, 218, 343])


class Player(GameObject):

    def __init__(self):
        super(Player, self).__init__(0, 0, 'player.png')
        self.lanes_x = [93, 218, 343]
        self.lanes_y = [93, 218, 343]
        self.lane_index_x = 1
        self.lane_index_y = 1
        self.reset()
        self.hit_cooldown = False
        self.last_hit_time = 0

    def left(self):
        if self.lane_index_x > 0:
            self.lane_index_x -= 1
            self.dx = self.lanes_x[self.lane_index_x]

    def right(self):
        if self.lane_index_x < len(self.lanes_x) - 1:
            self.lane_index_x += 1
            self.dx = self.lanes_x[self.lane_index_x]

    def up(self):
        if self.lane_index_y > 0:
            self.lane_index_y -= 1
            self.dy = self.lanes_y[self.lane_index_y]

    def down(self):
        if self.lane_index_y < len(self.lanes_y) - 1:
            self.lane_index_y += 1
            self.dy = self.lanes_y[self.lane_index_y]

    def move(self):
        self.x -= (self.x - self.dx) * 0.25
        self.y -= (self.y - self.dy) * 0.25

    def reset(self):
        self.dx = self.lanes_x[self.lane_index_x]
        self.dy = self.lanes_y[self.lane_index_y]
        self.x = 250 - 32
        self.y = 250 - 32

    def hit(self):
        if not self.hit_cooldown:
            print('Player hit by bomb, or there was a normal collision!')
            self.hit_cooldown = True
            self.last_hit_time = time.time()


class Bomb(GameObject):

    def __init__(self):
        super(Bomb, self).__init__(0, 0, 'bomb.png')
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.reset()

    def move(self):

        # Move in a specific direction

        if self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed

        # Reset bomb if it goes off screen

        if self.x < -64 or self.x > 500 or self.y < -64 or self.y > 500:
            self.reset()

    def reset(self):

        # Randomly choose an edge to start from

        edge = choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            self.x = choice([93, 218, 343])
            self.y = -64  # Start above the screen
            self.direction = 'down'
        elif edge == 'bottom':
            self.x = choice([93, 218, 343])
            self.y = 500  # Start below the screen
            self.direction = 'up'
        elif edge == 'left':
            self.x = -64  # Start left of the screen
            self.y = choice([93, 218, 343])
            self.direction = 'right'
        elif edge == 'right':
            self.x = 500  # Start right of the screen
            self.y = choice([93, 218, 343])
            self.direction = 'left'

        # Set a lower speed for movement

        self.speed = randint(0, 50) / 100 + 0.5  # Adjusted speed range


# Make an instance of GameObject
# apple = GameObject(0, 250, 'apple.png')

apple = Apple()
strawberry = Strawberry()

# make an instance of Player

player = Player()

bomb = Bomb()

# Add sprites to group

all_sprites.add(player)
all_sprites.add(apple)
all_sprites.add(strawberry)
all_sprites.add(bomb)

# make a fruits Group

fruit_sprites = pygame.sprite.Group()

fruit_sprites.add(apple)
fruit_sprites.add(strawberry)

# Creat the game loop

running = True
while running:

  # Looks at events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()

  # Clear screen

    screen.fill((255, 255, 255))

  # Move and render Sprites

    for entity in all_sprites:
        entity.move()
        entity.render(screen)

  # Check Colisions

    fruit = pygame.sprite.spritecollideany(player, fruit_sprites)
    if fruit:
        fruit.reset()

# Check collision player and bomb

    if pygame.sprite.collide_rect(player, bomb) and player.rect.collidepoint(bomb.x, bomb.y):
        player.hit()
        running = False

    if player.hit_cooldown and time.time() - player.last_hit_time > 2:
        player.hit_cooldown = False

  # Update the window

    pygame.display.flip()

  # tick the clock!

    clock.tick(60)
