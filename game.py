# Example 2

# Import and initialize pygame
import pygame
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
	def __init__(self, x, y, image):
		super(GameObject, self).__init__()
		self.surf = pygame.image.load(image)
		self.x = x
		self.y = y
		self.rect = self.surf.get_rect() # add 

	def render(self, screen):
		self.rect.x = self.x # add
		self.rect.y = self.y # add
		screen.blit(self.surf, (self.x, self.y))

class Apple(GameObject):
 def __init__(self):
   super(Apple, self).__init__(0, 0, 'apple.png')
   self.dx = 0
   self.dy = (randint(0, 200) / 100) + 1
   self.reset() # call reset here! 

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
   self.dx = (randint(0, 200) / 100) + 1
   self.dy = 0
   self.reset() # call reset here! 

 def move(self):
   self.x += self.dx
   self.y += self.dy
   # Check the y position of the apple
   if self.x > 500: 
     self.reset()

 # add a new method
 def reset(self):
   self.x =  -64
   self.y = choice([93, 218, 343])

class Player(GameObject):
  def __init__(self):
    super(Player, self).__init__(0, 0, 'player.png')
    self.lanes_x = [93, 218, 343]  
    self.lanes_y = [93, 218, 343]  
    self.lane_index_x = 1          
    self.lane_index_y = 1
    self.reset()

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

# Make an instance of GameObject
# apple = GameObject(0, 250, 'apple.png')

apple = Apple()
strawberry = Strawberry()
# make an instance of Player
player = Player()

# Add sprites to group
all_sprites.add(player)
all_sprites.add(apple)
all_sprites.add(strawberry)

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

  # Update the window
  pygame.display.flip()
  # tick the clock!
  clock.tick(60)


