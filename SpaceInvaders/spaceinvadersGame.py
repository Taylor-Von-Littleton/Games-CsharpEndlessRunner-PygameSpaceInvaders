import pygame
import random
from pygame import mixer

pygame.init() # initializes pygame

window_height = 600 # height of the window
window_width = 800 # width of the window
rows = 3 
cols = 10
game_over = 0 # 0 when the game is not over and 1 when the game is over

clock = pygame.time.Clock() # creates a clock
timer = pygame.time.get_ticks() # gets the time in milliseconds

screen = pygame.display.set_mode((window_width, window_height)) # creates a window
pygame.display.set_caption("Space Invaders") # sets the title of the window

background = pygame.image.load("images/background.jpg") # loads the background image

mixer.init() # initializes the mixer
mixer.music.load('images/game.wav') # loads the music
mixer.music.play()  # plays the music -1 means loop forever

invaders_group = pygame.sprite.Group()  # creates a group of invaders 
player_group = pygame.sprite.Group() # creates the player
playerBullet_group = pygame.sprite.Group() # creates a group of player bullets
invaderBullet_group = pygame.sprite.Group() # creates a group of invader bullets

class player_bullet(pygame.sprite.Sprite): #blueprint for the player bullet
    def __init__(self, x, y): # initializes the player bullet
        pygame.sprite.Sprite.__init__(self) # initializes the sprite
        self.image = pygame.image.load("images/user_bullet.png") # loads the image 
        self.rect = self.image.get_rect()  # gets the rectangle of the image 
        self.rect.center = [x, y] # sets the center of the rectangle
    def update(self): # updates the player bullet
        self.rect.y -= 5 # moves the player bullet up 5 pixels
        if pygame.sprite.spritecollide(self, invaders_group, True): # if the player bullet collides with an invader end the bullet image.
            self.kill() # kills the player bullet


class invader_bullet(pygame.sprite.Sprite): #blueprint for the invader bullet
    def __init__(self, x, y): # initializes the invader bullet
        pygame.sprite.Sprite.__init__(self) # initializes the sprite
        self.image = pygame.image.load("images/invader_bullet.png") # loads the image
        self.rect = self.image.get_rect() # gets the rectangle of the image
        self.rect.center = [x, y]  # sets the center of the rectangle

    def update(self): # updates the invader bullet
        self.rect.y += 2 # moves the invader bullet down 2 pixels
        
        if pygame.sprite.spritecollide(self, player_group, False): # if the invader bullet collides with the player end the bullet image.
            self.kill() # kills the invader bullet image
            player.health_remaining -= 10 # decreases the player's health by 10 when the player is hit by an invader bullet


class Invader(pygame.sprite.Sprite): #blueprint for the invader
    def __init__(self, x, y): # initializes the invader 
        pygame.sprite.Sprite.__init__(self) # initializes the sprite
        self.image = pygame.image.load("images/spaceInvaders.png") # loads the image
        self.rect = self.image.get_rect() # gets the rectangle of the image
        self.rect.center = [x, y] # sets the center of the rectangle
        self.move_direction = 1 # sets the move direction to 1
        self.move_counter = 0 # sets the move counter to 0

    def update(self): # updates the invader
        self.rect.x += self.move_direction  # moves the invader to the right or left
        self.move_counter += 1 # increases the move counter by 1

        if self.move_counter > 75: # if the move counter is greater than 75
            self.move_direction *= -1 # change the move direction to -1
            self.move_counter *= -1 # change the move counter to -1

class Player(pygame.sprite.Sprite): #blueprint for the player
    def __init__(self, x, y): # initializes the player
        pygame.sprite.Sprite.__init__(self) # initializes the sprite
        self.image = pygame.image.load("images/user.png") # loads the image
        self.rect = self.image.get_rect() # gets the rectangle of the image
        self.rect.center = [x, y]  # sets the center of the rectangle
        self.last_shot = pygame.time.get_ticks() # sets the last shot to the current time
        self.health_start = 50 # sets the health to 50
        self.health_remaining = 50 # sets the health remaining to 50

    def update(self): # updates the player
        speed = 3 # sets the speed to 3 (the speed of the player)
        cooldown = 100 # sets the cooldown to 100 to delay the player's shot by 100 milliseconds to prevent spamming
        current_time = pygame.time.get_ticks() # gets the current time in milliseconds
        key = pygame.key.get_pressed() # gets the key pressed
        gameover = 0 # sets the gameover to 0 which means the game is not over

        pygame.draw.rect(screen, (0,0,0), (self.rect.x, self.rect.bottom, self.rect.width, 10)) # draws a black rectangle at the bottom of the player
        if self.health_remaining > 0: # if the player's health is greater than 0
            #CODE BELOW draws a green rectangle at the bottom of the player indicating the player's health 
            pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.bottom, int(self.rect.width * (self.health_remaining/self.health_start)), 10))
        elif self.health_remaining == 0: # if the player's health is 0
            self.kill() # kills the player
            gameover = 1  # sets the gameover to 1 which means the game is over

        if key[pygame.K_LEFT] and self.rect.left > 0:  # if the left arrow key is pressed and the player is not at the left side of the screen
            self.rect.x -= speed # move the player to the left

        if key[pygame.K_RIGHT] and self.rect.right < window_width: # if the right arrow key is pressed and the player is not at the right side of the screen
            self.rect.x += speed # move the player to the right

        if key[pygame.K_SPACE] and current_time-self.last_shot > cooldown: # if the space bar is pressed and the player has not shot in the last 100 milliseconds
            bullet = player_bullet(self.rect.centerx, self.rect.top) # creates a player bullet that will shoot from the center of the player
            playerBullet_group.add(bullet) # adds the player bullet to the playerBullet_group
            self.last_shot = pygame.time.get_ticks() # sets the last shot to the current time so the player cannot shoot again until 100 milliseconds have passed

        return gameover

def create_invader_bullet(): # function that creates an invader bullet
    attacking_invader = random.choice(invaders_group.sprites()) # chooses a random invader to shoot from
    invaderBullet = invader_bullet(attacking_invader.rect.centerx, attacking_invader.rect.centery) 
    #^^^CODE ABOVE creates an invader bullet that will shoot from the center of the invader
    invaderBullet_group.add(invaderBullet) # adds the invader bullet to the invaderBullet_group

def create_invaders(): # function that creates an invader
    for row in range(rows): # for each row
        for col in range(cols): # for each column
            invader = Invader(100 + col * 65, 80 + row * 50) # creates an invader at the specified coordinates
            invaders_group.add(invader) # adds the invader to the invaders_group

create_invaders() # calls the create_invaders function           

player = Player(int(window_width/2), window_height - 100) # creates the player at the center of the screen
player_group.add(player) # adds the player to the player_group

game = True # sets the game to true
while game: # while the game is true
    clock.tick(60) # sets the clock to 60 frames per second to prevent the game from running too fast
    screen.blit(background, (0,0)) # used to draw the background image
    if len(invaders_group) == 0: # if the invaders_group is empty
        game_over = 1 # sets the game_over to 1 which means the game is over

    seconds = (pygame.time.get_ticks() - timer) / 1000 # gets the number of seconds since the timer was set
    if(seconds > 5): # if the number of seconds since the timer was set is greater than 5
        create_invader_bullet() # calls the create_invader_bullet function to create an invader bullet
        timer = pygame.time.get_ticks() # sets the timer to the current time
  
    if game_over == 0: # if the game is not over
        invaders_group.update() # updates the invaders
        player_group.update() # updates the player
        invaderBullet_group.update() # updates the invader bullets
        playerBullet_group.update() # updates the player bullets

        invaders_group.draw(screen) # draws the invaders
        player_group.draw(screen) # draws the player
        invaderBullet_group.draw(screen) # draws the invader bullets
        playerBullet_group.draw(screen) # draws the player bullets
        game_over = player.update() # updates the player and sets the game_over to the return value of the player.update function

    elif game_over == 1: # if the game is over
        background = pygame.image.load("images/gameover_background.jpg") # loads the background image

    for event in pygame.event.get(): # gets all the events
        if event.type == pygame.QUIT: # if the event is a quit event
            game = False # sets the game to false which means the game is over
    
    pygame.display.update() # updates the display

pygame.quit() # quits the game