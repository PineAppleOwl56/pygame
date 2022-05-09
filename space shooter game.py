import pygame

pygame.init()

window = pygame.display.set_mode((500,500))

pygame.display.set_caption("Space Shooter")


background = pygame.image.load('background.jpg')
standing = pygame.image.load('L6.png')
enamy = pygame.image.load('123.png')
clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.velocity = 5
        self.hitbox = (self.x, self.y, 46, 46)
        
    def draw(self, window):
        window.blit(standing, (self.x, self.y))
        self.hitbox = (self.x  , self.y, 46, 46)

    def hit(self):
        self.x = 60 
        self.y = 410
        font1 = pygame.font.SysFont('comicsans', 40)
        text = font1.render('You have crashed', 1, (153, 255, 255))
        window.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

        
class projectile():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = 6
        
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        
class enemy():
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.end = end
        self.path = [x, end]
        self.velocity = 6
        self.hitbox = (self.x, self.y, 90, 60)
        self.health = 100
        self.visible = True
        self.enamy = enamy
        
    def draw(self, window):
        self.move()
        if self.visible:
            window.blit(self.enamy, (self.x,self.y))

            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1]-20, 90, 10))
            pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0], self.hitbox[1]-20, 90 - (9* (10 - self.health/10)), 10))
            self.hitbox = (self.x, self.y, 90, 60)
    
    def move(self):
        if self.velocity > 0:
            if self.x < self.path[1] + self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity

        else:
            if self.x > self.path[0] - self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
                
    def hit(self):
        if self.health > 0:
            self.health -= 0.5
        else:
            self.visible = False
            
    def restart(self):

        font3 = pygame.font.SysFont('comicsans', 50)
        text = font3.render('You Have Won', 1, (153, 255, 255))
        window.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 1000:
            pygame.time.delay(1000)
            i += 0.1
            pygame.quit()


def outputting():
    window.blit(background, (0, 0))
    text = font.render("score: " + str(score), 1, (250, 0, 0))
    window.blit(text, (390,10))
    ship.draw(window)
    enamyship.draw(window)
    for bullet in bullets:
       bullet.draw(window)
    pygame.display.update()

font = pygame.font.SysFont("comicsans", 15, True, True)
ship = player(220, 440, 46, 46)
enamyship = enemy(0, 50, 90, 60, 410)
bullets = []

run = True 
while run:
    clock.tick(60)
    
    if ship.hitbox[1] < enamyship.hitbox[1] + enamyship.hitbox[3] and ship.hitbox[1] + ship.hitbox[3] > enamyship.hitbox[1]:
        if ship.hitbox[0] + ship.hitbox[2] > enamyship.hitbox[0] and ship.hitbox[0] < enamyship.hitbox[0] + enamyship.hitbox[2]:
            ship.hit()
            score -= 5
    
    if enamyship.visible == False:
        enamyship.restart()
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    for bullet in bullets:
        if bullet.y - bullet.radius < enamyship.hitbox[1] + enamyship.hitbox[3] and bullet.y + bullet.radius > enamyship.hitbox[1]:
            if bullet.x + bullet.radius > enamyship.hitbox[0] and bullet.x - bullet.radius < enamyship.hitbox[0] + enamyship.hitbox[2]:
                enamyship.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.y < 500 and bullet.y > 0:
            bullet.y -= bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if len(bullets) < 100:
            bullets.append(projectile(round(ship.x + ship.width // 2), round(ship.y), 2, (153, 255, 255)))
    
    if keys[pygame.K_LEFT] and ship.x > ship.velocity:
        ship.x -= ship.velocity

        
    elif keys[pygame.K_RIGHT] and ship.x < 500 - ship.width - ship.velocity:
        ship.x += ship.velocity

    if keys[pygame.K_UP] and ship.y > ship.velocity:
        ship.y -= ship.velocity

    elif keys[pygame.K_DOWN] and ship.y < 500 - ship.height - ship.velocity:
        ship.y += ship.velocity

    outputting()