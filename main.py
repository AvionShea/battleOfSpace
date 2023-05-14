from matplotlib.pyplot import draw
import pygame
import os
pygame.font.init() #intialize pygame font library
pygame.mixer.init()

# Surface
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT) #defining play screen division

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun.mp3'))

HEALTH_FONT = pygame.font.SysFont('Arial', 35)
WINNER_FONT = pygame.font.SysFont('Arial', 95)

FPS = 60 #defining FPS
VEL = 3 #speed variable
BULLET_VEL = 5 #speed of bullets
MAX_BULLETS = 7 #number of bullets each player has
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

#Creating User Event
PURPLE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#importing spaceships
PURPLE_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "purple.png"))
PURPLE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(PURPLE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) #rotate and resizing image

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) #rotate and resizing image

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)) #scaling image used as background

def draw_window(purple, red, purple_bullets, red_bullets, purple_health, red_health):        
        WIN.blit(SPACE, (0, 0)) #Fill Surface with image
        pygame.draw.rect(WIN, WHITE, BORDER) #rectangle dividing play screen

        purple_health_text = HEALTH_FONT.render("Lives: " + str(purple_health), 1, WHITE)
        red_health_text = HEALTH_FONT.render("Lives: " + str(red_health), 1, WHITE)
        WIN.blit(purple_health_text,(10, 10))
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

        WIN.blit(PURPLE_SPACESHIP, (purple.x, purple.y)) #placing purple ship on x and y axis -draw a surface onto the screen - use whenever you're adding images or text
        WIN.blit(RED_SPACESHIP, (red.x, red.y)) #placing red ship on x and y axis



        for bullet in purple_bullets:
            pygame.draw.rect(WIN, PURPLE, bullet)

        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        pygame.display.update() #updates the window/surface

#Purple Spaceship Move Keys using W,A,S,D
def purple_movement(keys_pressed, purple): 
        if keys_pressed[pygame.K_a] and purple.x - VEL > 0: #LEFT #AND statements keeps playing from moving off screen
            purple.x -= VEL #subtracting from x-axis
        if keys_pressed[pygame.K_d] and purple.x + VEL + purple.width < BORDER.x: #RIGHT #Keeps ship from crossing divider
            purple.x += VEL #adding to x-axis
        if keys_pressed[pygame.K_w] and purple.y - VEL > 0: #UP
            purple.y -= VEL #subtracting from y-axis
        if keys_pressed[pygame.K_s] and purple.y + VEL + purple.width < HEIGHT: #DOWN
            purple.y += VEL #adding to y-axis

#Red Spaceship Move Keys using arrows
def red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
            red.x -= VEL #subtracting from x-axis
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
            red.x += VEL #adding to x-axis
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
            red.y -= VEL #subtracting from y-axis
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT: #DOWN
            red.y += VEL #adding to y-axis

#function moves, handles collison, and removing of bullets #checks for colliding with rectangle. Only works if both objects are rectangular
def handle_bullets(purple_bullets, red_bullets, purple, red): 
    for bullet in purple_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #checking if purple bullets hits red ship
            pygame.event.post(pygame.event.Event(RED_HIT))
            purple_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            purple_bullets.remove(bullet) #remove bullets if they go off the screen

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #moving closer to 0,0
        if purple.colliderect(bullet): #checking if red bullets hits purple ship
            pygame.event.post(pygame.event.Event(PURPLE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0: 
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, TEAL)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(6000)

#Main Game Loop
def main():
    purple = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #Starting position for purple spaceship
    red = pygame.Rect(750, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #Starting position for red spaceship

    purple_bullets = [] #bullet storage
    red_bullets = [] #bullet storage

    purple_health = 10 #health
    red_health = 10 #health

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #control speed of While Loop - never goes over the speed given
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #firing bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(purple_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(purple.x + purple.width, purple.y + purple.height//2 - 2, 10, 5) # two // for interger division
                    purple_bullets.append(bullet) #removes bullet whenever bullet is fired
                    BULLET_FIRE_SOUND.play() #sound plays whenever bullet is fired

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) # two // for interger division
                    red_bullets.append(bullet) #removed bullet whenever bullet is fired
                    BULLET_FIRE_SOUND.play() #sound plays whenever bullet is fired
        
            if event.type == PURPLE_HIT:
                purple_health -= 1 #whenever the ship is hit, it removes the health
                BULLET_HIT_SOUND.play() #sound plays whenever ship is hit
            
            if event.type == RED_HIT:
                red_health -=1 #whenever the ship is hit, this removes the health
                BULLET_HIT_SOUND.play()#sound plays whenever ship is hit


        winner_text = ""
        if purple_health <= 0:
            winner_text = "Red Wins!"

        if red_health <= 0:
            winner_text = "Purple Wins!"

        if winner_text != "":
            draw_winner(winner_text) # SOMEONE WON
            break

        keys_pressed = pygame.key.get_pressed()
        purple_movement(keys_pressed, purple)
        red_movement(keys_pressed, red)

        handle_bullets(purple_bullets, red_bullets, purple, red) #events that happen if bullets collide with ships

        draw_window(purple, red, purple_bullets, red_bullets, purple_health, red_health)

    main()

#Only run this main function if the file is directly ran, not imported.
if __name__ == "__main__":
    main()