from operator import truediv
import pygame 
import os
import math
import random
pygame.init()


WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid")

## If you are going to make colors using RGB, make sure to assign them up here so that we do not have random numbers at the bottom
## This is good practice to have for future references.
white_color = (255,255,255)
black_color = (0,0,0)

#try playing around with different FPS to see how the image moves in different fps 
FPS = 60
# this is for the speed or velocity at which the plane will move; feel free to change this value to your liking
VEL = 5

#Initializing spaceship dimensions
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40
YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
# init Asteroid image
small_asteroid = pygame.image.load(os.path.join('assets', 'asteroid50.png'))
medium_asteroid = pygame.image.load(os.path.join('assets', 'asteroid100.png')) 
large_asteroid = pygame.image.load(os.path.join('assets', 'asteroid150.png'))
# init Alienship image
alien_img = pygame.image.load(os.path.join('assets', 'alienShip.png'))
alien_img = pygame.transform.scale(alien_img, (100, 100))
# init Asteroid image
ITEM_WIDTH, ITEM_HEIGHT = 50, 40
shield_img = pygame.image.load(os.path.join('assets','shield.png'))
shield_img = pygame.transform.scale(shield_img, (ITEM_WIDTH, ITEM_HEIGHT))
speed_up_img = pygame.image.load(os.path.join('assets','speed_up.png'))
speed_up_img = pygame.transform.scale(speed_up_img, (ITEM_WIDTH, ITEM_HEIGHT))
invincibility_img = pygame.image.load(os.path.join('assets','invincibility.png'))
invincibility_img = pygame.transform.scale(invincibility_img, (ITEM_WIDTH, ITEM_HEIGHT))
double_shot_img = pygame.image.load(os.path.join('assets','double_shot.png'))
double_shot_img = pygame.transform.scale(double_shot_img, (ITEM_WIDTH, ITEM_HEIGHT))
life_up_img = pygame.image.load(os.path.join('assets','life_up.png'))
life_up_img = pygame.transform.scale(life_up_img, (ITEM_WIDTH, ITEM_HEIGHT))

class Spaceship(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1: #This is player 1
            self.img = YELLOW_SPACESHIP
            self.x = WIDTH//2 + 100
        if self.rank == 2: #This is player 2
            self.img = RED_SPACESHIP
            self.x = WIDTH//2 - 100
        self.y = HEIGHT//2
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.angle = 0
        #update all of these variables below, when we apply changes to the variable above
        self.img_dir = pygame.transform.rotate(self.img, self.angle)
        self.rect_dir = self.img_dir.get_rect()
        self.rect_dir.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width//2, self.y - self.sine * self.height//2)

    def redraw_ship(self, WIN):
        #WIN.blit(self.img, (self.x, self.y, self.w, self.h))
        WIN.blit(self.img_dir, self.rect_dir)

    def turnLeft(self):
        self.angle += VEL
        self.img_dir = pygame.transform.rotate(self.img, self.angle)
        self.rect_dir = self.img_dir.get_rect()
        self.rect_dir.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width//2, self.y - self.sine* self.height//2)

    def turnRight(self):
        self.angle -= VEL
        self.img_dir = pygame.transform.rotate(self.img, self.angle)
        self.rect_dir = self.img_dir.get_rect()
        self.rect_dir.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width//2, self.y - self.sine* self.height//2)

    def moveForward(self):
        self.x += self.cosine*VEL #how to differentiate p1 and p2 speed
        self.y -= self.sine*VEL
        self.img_dir = pygame.transform.rotate(self.img, self.angle)
        self.rect_dir = self.img_dir.get_rect()
        self.rect_dir.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width//2, self.y - self.sine* self.height//2)

    def check_inbounds(self): #No problem with the bound check function.  Good job!
        if self.x <= 0 or self.x > WIDTH or self.y > HEIGHT or self.y <= 0:
            return False
        return True
    
    #One problem you ran into was when the plane went to the border, they would just stop moving
    #Hence, one way to fix that problem is to make a function bounce() that will relocate the plane
    #once it hit the border.  This way, when the plane is out of bounds, it does not just stay there.
    #**Check in the main function for more details**

    def bounce(self): 
        if self.x <= 0:
            self.x += 1
        if self.x > WIDTH:
            self.x -= 1
        if self.y > HEIGHT:
            self.y -= 1
        if self.y <= 0:
            self.y += 1

class Bullet(object):
    def __init__(self, player):
        self.coord = player.head
        self.x = self.coord[0]
        self.y = self.coord[1]
        self.width = 5
        self.height = 5
        self.cosine = player.cosine
        self.sine = player.sine
        self.xdelta = self.cosine*VEL
        self.ydelta = self.sine*VEL

    def move(self):
        self.x += self.xdelta
        self.y -= self.ydelta

    def draw_bullet(self, WIN):
        pygame.draw.rect(WIN, black_color, (self.x, self.y, self.width, self.height))

    def check_bounds(self):
        if self.x < - 10 or self.x > WIDTH or self.y > HEIGHT or self.y < - 10:
            return False

class Alienship(object):
    def __init__(self):
        self.img = alien_img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x, self.y = random.choice([(random.randrange(0, WIDTH-self.width), random.choice([-1*self.height - 5, HEIGHT + 5])), 
                                        (random.choice([-1*self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))])
        if self.x < WIDTH //2:
            self.xdirection =1
        else:
            self.xdirection = -1
        if self.y<HEIGHT//2:
            self.ydirection =1
        else: 
            self.ydirection =-1     
        self.xvel = self.xdirection * VEL
        self.yvel = self.ydirection * VEL
    def move(self):
        self.x +=  self.xvel
        self.y +=  self.yvel

    def draw_Alienship(self, WIN):
        WIN.blit(self.img, (self.x, self.y))

class AlienBullet(object):
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        if timer % 2 ==1:
            self.x = x
            self.y = y
            self.targetx = player1.x
            self.targety = player1.y
        else:
            self.x = x
            self.y = y
            self.targetx = player2.x
            self.targety = player2.y

        self.width = 5
        self.height = 5
        self.dx= self.targetx - self.x
        self.dy = self.targety -self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx = self.dx / self.dist
        self.dy= self.dy/ self.dist
        self.xvel = self.dx * VEL
        self.yvel = self.dy * VEL

    def move(self):
        self.x +=  self.xvel
        self.y +=  self.yvel

    def draw_alienbullet(self, WIN):
        pygame.draw.rect(WIN, black_color, (self.x, self.y, self.width, self.height))
class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1 :
            self.img = small_asteroid
        elif self.rank == 2:
            self.img = medium_asteroid
        else:
            self.img = large_asteroid
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x, self.y = random.choice([(random.randrange(0, WIDTH-self.width), random.choice([-1*self.height - 5, HEIGHT + 5])), 
                                        (random.choice([-1*self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))])
        
        if self.x < WIDTH//2:
            self.xdirection = 1
        else:
            self.xdirection =-1
        if self.y < HEIGHT//2:
            self.ydirection =1
        else:
            self.ydirection =1
        self.xvel = self.xdirection * random.randrange(1,3)
        self.yvel = self.ydirection * random.randrange(1, 3)
    def move(self):
        self.x +=  self.xvel
        self.y +=  self.yvel
    def draw_asteroid(self, WIN):
        WIN.blit(self.img, (self.x, self.y))

class Items(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank ==1:
            self.img = life_up_img
        if self.rank == 2:
            self.img = double_shot_img
        if self.rank == 3:
            self.img = invincibility_img
        if self.rank == 4:
            self.img = shield_img
        else:
            self.img = speed_up_img
        
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x, self.y = random.choice([(random.randrange(0, WIDTH-self.width), random.choice([-1*self.height - 5, HEIGHT + 5])), 
                                        (random.choice([-1*self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))])
        if self.x < WIDTH// 2:
            self.xdirection = 1
        else:
            self.xdirection = -1
        if self.y < HEIGHT//2:
            self.ydirection = 1
        else:
            self.ydirection = -1
        self.xvel = self.xdirection * VEL
        self.yvel = self.ydirection * VEL
        
    def move(self):
        self.x += self.xvel
        self.y += self.yvel
    
    def draw_items(self, WIN):
        WIN.blit(self.img, (self.x, self.y))
        
    
# additional life
# double- shot: shoots faster
# invincibility for few sec
# shield
# speed up

# we fly thru the item to activate it -> a collision check with items
# moves around similar to asteroids
# booleans


player1 = Spaceship(1)
p1_lives = 3
p1_scores = 0
player2 = Spaceship(2)
p2_lives = 3
p2_scores = 0
player1Bullet = [] #initialize bullet array for player 1
player2Bullet = [] #initialize bullet array for player 2
aliens = [ ] # init alienship 
alienBullet_list= []

items = []

p1_shields = False
p1_invincibility = False
p1_speed_up = False
p1_double_shot = False
p1_item_duration = -1

p2_shields = False
p2_invincibility = False
p2_speed_up = False
p2_double_shot = False
p2_item_duration = -1

#shield  = false in the beginning
#invincibility = false
#speed - up = false
#double shot = false
# life up is adding += to lives
asteroid = [] #init asteroid array
Spaceship = []
gameover = False

#redraw image of our window function
def redraw_window():

    font = pygame.font.SysFont('arial', 30)
    p1_livesText = font.render('Lives: ' + str(p1_lives), 1, black_color)
    p2_livesText = font.render('Lives: ' + str(p2_lives), 1, black_color)
    WIN.fill(white_color)
    player1.redraw_ship(WIN) 
    player2.redraw_ship(WIN)
    for b1 in player1Bullet: # if there is a bullet in the player1 call,
        b1.draw_bullet(WIN) # this draws our bullet
    for b2 in player2Bullet:
        b2.draw_bullet(WIN)
    for a in asteroid:
        a.draw_asteroid(WIN)
    for a in aliens:
        a.draw_Alienship(WIN)
    for a in alienBullet_list:
        a.draw_alienbullet(WIN)
    for i in items:
        i.draw_items(WIN)

    
    WIN.blit(p1_livesText, (WIDTH-75,25))
    WIN.blit(p2_livesText, (25,25))
    if gameover:
        pass
        

    pygame.display.update()

# Main class: Program 
# Two subclasses: Game and Menu
# gameover boolean call checks whether it is in game state or menu state
# run boolean call checks whether the program itself is running
# Hence, even if the gameover state changes, the program itself will not close
# The program only ends if we pressed red circle in the pop-up window, which tells the program that it is actually over

# initializing the starting point of yellow spaceship
## you can change the coordinate of the yellow spaceship once you create a red spaceship
## initialize for red spaceship

    # whether it is a game state or menu state




clock = pygame.time.Clock()
run = True #the program is running
timer = 0
while run:
    clock.tick(FPS)
    timer += 1 # ==1 second
    #Game state
    
    if not gameover:
        for b1 in player1Bullet: 
            b1.move() # the bullet is moving in constant time while the game is going on
            if not b1.check_bounds:
                player1Bullet.pop(player1Bullet.index(b1))
            if (b1.x >= player2.x and b1.x <= player2.x + player2.width) or (b1.x + b1.width >= player2.x and b1.x + b1.width <= player2.x + player2.width):
                if (b1.y >= player2.y and b1.y <= player2.y + player2.height) or (b1.y + b1.height >= player2.y and b1.y + b1.height <= player2.y + player2.height):
                    player2.x = WIDTH//2 - 100
                    player2.y = HEIGHT//2
                    if(p2_invincibility == False and p2_shields == False):# how to differentiate p1 & p2 invincibility
                        p2_lives -= 1 
                    player1Bullet.pop(player1Bullet.index(b1))
                    break
        for b2 in player2Bullet:
            b2.move()
            if not b2.check_bounds:
                player2Bullet.pop(player2Bullet.index(b2))
            if ((b2.x >= player1.x and b2.x <= player1.x + player1.width) or (b2.x + b2.width >= player1.x and b2.x + b2.width <= player1.x + player1.width)) and not p1_invincibility:
                if (b2.y >= player1.y and b2.y <= player1.y + player1.height) or (b2.y + b2.height >= player1.y and b2.y + b2.height <= player1.y + player1.height):
                    if (shields_p1 ==True): ## 
                        shields_p1= False ## 
                        break
                    player1.x = WIDTH//2 + 100
                    player1.y = HEIGHT//2
                    p1_lives -= 1 
                    player2Bullet.pop(player2Bullet.index(b2))
                    break
        for i in items:
            i.move()
            if (i.x >= player1.x - player1.width //2 and i.x <= player1.x + player1.width//2) or (i.x + a.width <= player1.x + player1.width//2 and i.x + i.width >= player1.x - player1.width//2):
                if (i.y >= player1.y - player1.width //2 and i.y <= player1.y + player1.width//2) or (i.y + i.width <= player1.y + player1.width//2 and i.y + i.width >= player1.y - player1.height//2):
                    p1_item_duration = timer
                    if i.rank == 1:
                        p1_lives +=1
                    elif i.rank ==2:
                        p1_double_shot = True
                    elif i.rank ==3:
                        p1_invincibility = True
                    elif i.rank ==4:
                        p1_shield = True
                    else:
                        p1_speed_up = True
                    items.pop(items.index(i))
        if p1_lives <= 0 or p2_lives <=0:
            gameover = True

        if p1_item_duration != -1:
            if timer - p1_item_duration >500:
                if p1_double_shot == True:
                    p1_double_shot = False
                elif p1_invincibility == True:
                    p1_invincibility = False
                elif p1_speed_up ==True:
                    p1_speed_up = False
        if timer % 100 ==0:
            choose = random.choice([1,2,3])
            asteroid.append(Asteroid(choose))

        if timer % 750 ==0:
            aliens.append(Alienship())

        if timer % 700 == 0:
            choose = random.choice([1,2,3,4,5])
            items.append(Items(choose))

        for i, a in enumerate(aliens): #i is index a is the alien
            a.move()
            if a.x > WIDTH + 100 or a.width + a.x < 100 or a.y> HEIGHT +100 or a.y + a.height <-100:
                aliens.pop(i)
            if timer % 75 == 0:
                alienBullet_list.append(AlienBullet( a.x + a.width//2, a.y + a.height//2, timer))
            #Alien collision check with player bullets
            # player 1:
            for b1 in player1Bullet:
                if(b1.x >= a.x and b1.y <= a.x+a.width) or (b1.x + b1.width >=  a.x and b1.x + b1.width <= a.x + a.width):
                    if(b1.y >= a.y and b1.y <= a.y+a.height) or (b1.y + b1.height >=  a.y and b1.y + b1.height <= a.y + a.height):
                        aliens.pop(i)
                        break

            for b2 in player2Bullet:
                if(b2.x >= a.x and b2.y <= a.x+a.width) or (b2.x + b2.width >=  a.x and b2.x + b2.width <= a.x + a.width):
                    if(b2.y >= a.y and b2.y <= a.y+a.height) or (b2.y + b2.height >=  a.y and b2.y + b2.height <= a.y + a.height):
                        aliens.pop(i)
                        break

        for i, b in enumerate(alienBullet_list):
            b.move()
            if (b.x >= player1.x - player1.width //2 and b.x <= player1.x + player1.width//2) or (b.x + b.width <= player1.x + player1.width//2 and b.x + b.width >= player1.x - player1.width//2):
                if (b.y >= player1.y - player1.width //2 and b.y <= player1.y + player1.width//2) or (b.y + b.width <= player1.y + player1.width//2 and b.y + b.width >= player1.y - player1.height//2) and not p1_invincibility:
                    if (shields_p1 ==True): ## 
                        shields_p1= False ## 
                        break
                    p1_lives -= 1
                    alienBullet_list.pop(i)
                    break
            
            if (b.x >= player2.x - player2.width //2 and b.x <= player2.x + player2.width//2) or (b.x + b.width <= player2.x + player2.width//2 and b.x + b.width >= player2.x - player2.width//2):
                if (b.y >= player2.y - player2.width //2 and b.y <= player2.y + player2.width//2) or (b.y + b.width <= player2.y + player2.width//2 and b.y + b.width >= player2.y - player2.height//2):
                    p2_lives -= 1
                    alienBullet_list.pop(i)
                    break

        for a in asteroid:
            a.move()
            if (a.x >= player1.x - player1.width //2 and a.x <= player1.x + player1.width//2) or (a.x + a.width <= player1.x + player1.width//2 and a.x + a.width >= player1.x - player1.width//2):
                if (a.y >= player1.y - player1.width //2 and a.y <= player1.y + player1.width//2) or (a.y + a.width <= player1.y + player1.width//2 and a.y + a.width >= player1.y - player1.height//2) and not p1_invincibility:
                    if (shields_p1 ==True): ## 
                        shields_p1= False ## 
                        break
                    player1.x = WIDTH //2 +100
                    player1.y = HEIGHT//2
                    p1_lives -= 1
                    asteroid.pop(asteroid.index(a))
                    break
            if (a.x >= player2.x - player2.width //2 and a.x <= player2.x + player2.width//2) or (a.x + a.width <= player2.x + player2.width//2 and a.x + a.width >= player2.x - player2.width//2):
                if (a.y >= player2.y - player2.width //2 and a.y <= player2.y + player2.width//2) or (a.y + a.width <= player2.y + player2.width//2 and a.y + a.width >= player2.y - player2.height//2):
                    player2.x = WIDTH //2 +100
                    player2.y = HEIGHT//2
                    p2_lives -= 1
                    asteroid.pop(asteroid.index(a))
                    break



            for b1 in player1Bullet:
                if(b1.x >= a.x and b1.y <= a.x+a.width) or (b1.x + b1.width >=  a.x and b1.x + b1.width <= a.x + a.width):
                    if(b1.y >= a.y and b1.y <= a.y+a.height) or (b1.y + b1.height >=  a.y and b1.y + b1.height <= a.y + a.height):
                        if a.rank ==2: 
                            new_a1 = Asteroid(1)
                            new_a2 = Asteroid(1)
                            new_a1.x = a.x
                            new_a1.y = a.y
                            new_a2.x = a.x
                            new_a2.y = a.y
                            asteroid.append(new_a1)
                            asteroid.append(new_a2)
                        if a.rank ==3: 
                            new_a1 = Asteroid(2)
                            new_a2 = Asteroid(2)
                            new_a1.x = a.x
                            new_a1.y = a.y
                            new_a2.x = a.x
                            new_a2.y = a.y
                            asteroid.append(new_a1)
                            asteroid.append(new_a2)

                        asteroid.pop(asteroid.index(a))
                        player1Bullet.pop(player1Bullet.index(b1))
                        break
            for b2 in player2Bullet:
                if(b2.x >= a.x and b2.y <= a.x+a.width) or (b2.x + b2.width >=  a.x and b2.x + b2.width <= a.x + a.width):
                    if(b2.y >= a.y and b2.y <= a.y+a.height) or (b2.y + b2.height >=  a.y and b2.y + b2.height <= a.y + a.height):
                        if a.rank ==2: 
                            new_a1 = Asteroid(1)
                            new_a2 = Asteroid(1)
                            new_a1.x = a.x
                            new_a1.y = a.y
                            new_a2.x = a.x
                            new_a2.y = a.y
                            asteroid.append(new_a1)
                            asteroid.append(new_a2)
                        if a.rank ==3: 
                            new_a1 = Asteroid(2)
                            new_a2 = Asteroid(2)
                            new_a1.x = a.x
                            new_a1.y = a.y
                            new_a2.x = a.x
                            new_a2.y = a.y
                            asteroid.append(new_a1)
                            asteroid.append(new_a2)
                            
                        asteroid.pop(asteroid.index(a))
                        player2Bullet.pop(player2Bullet.index(b2))
                        break
        
                        
        if p1_lives <= 0 or p2_lives<= 0:
            gameover = True

        keys_pressed = pygame.key.get_pressed() 
        if keys_pressed[pygame.K_LEFT]: 
            player1.turnLeft()
        if keys_pressed[pygame.K_RIGHT]:
            player1.turnRight()
        if keys_pressed[pygame.K_UP]:
            # Here, I applied some changes.  Two conditionals instead of one.
            # First if statement checks if the plane is in bounds, and if it 
            # is not in bounds, then it "bounces" the plane.  What this will be do
            # is move the player forward (or backwards depending on which bounds) 
            # so that when it checks for inbounds, it doesnt just stop moving once it 
            # hits the border
            if not player1.check_inbounds(): # if out of bounds, move it back by one pixel
                player1.bounce()  
            # Second, the else statement confirms that it is inbounds, and it can continue 
            # to move around without having to stop once it hits the outbounds.
            else:
                player1.moveForward()
        if keys_pressed[pygame.K_a]:
            player2.turnLeft()
        if keys_pressed[pygame.K_d]:
            player2.turnRight()
        if keys_pressed[pygame.K_w]:
            if not player2.check_inbounds():
                player2.bounce()
            else:
                player2.moveForward()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # this checks that the "shoot" button is pressed
                if not gameover:
                    player1Bullet.append(Bullet(player1)) # this adds a bullet to the array we called initially

            if event.key == pygame.K_TAB:
                if not gameover:
                    player2Bullet.append(Bullet(player2))
                else:
                    gameover = False
                    p1_lives = 3
                    p1_scores = 0
                    p2_lives = 3
                    p2_scores = 0
                    asteroid.clear()
                    player1Bullet.clear()
                    player2Bullet.clear()
                    aliens.clear()
                    alienBullet_list.clear()
    redraw_window() 
    
    # this line checks for which key is pressed on keyboard by the user
    # REMEMBER: X and Y coordinates are zero at top-left of the screen
    # The notation for key is K_"FOLLOWED BY THE KEY" 
pygame.quit() #this quits the entire program 



