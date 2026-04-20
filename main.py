import pygame
from random import randint
pygame.init()
window_widths = 800
window_height = 600
square_size = 32
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
class Obstacles:
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,square_size,square_size)
    def draw(self,screen):
        pygame.draw.rect(screen,red,self.rect)

        
        
class Player:
    def __init__(self,x,y):
        self.health = 2
        self.rect=pygame.Rect(x,y,square_size,square_size)
        self.speed = 5
        self.bullets=[]
        self.direction = (0,-1)       
    def move(self,obstacles):
        keys = pygame.key.get_pressed()
        dx,dy = 0,0
        if keys[pygame.K_w]==True and self.rect.y>0:
            dy = -1
        if keys[pygame.K_s] == True and self.rect.y<window_height - square_size:
            dy = 1
        if keys[pygame.K_a] == True and self.rect.x>0:
            dx = -1
        if keys[pygame.K_d] == True and self.rect.x<window_widths - square_size:
            dx = 1
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed
        temp_rect = pygame.Rect(new_x, new_y, square_size, square_size)
        # Перевірка зіткнень
        for obstacle in obstacles:
            if temp_rect.colliderect(obstacle.rect):
                return  # Якщо є зіткнення, не рухаємо гравця
        self.rect.x = new_x
        self.rect.y = new_y
        if dx != 0 or dy != 0:       
            self.direction = (dx,dy) 
    def shoot(self):
        bulet = Bulet(self.rect.centerx,self.rect.centery,self.direction[0],self.direction[1])
        self.bullets.append(bulet)
    def draw(self,window):
        pygame.draw.rect(window,white,self.rect)
        for bulet in self.bullets:
            bulet.move()
            bulet.draw(window)

class Bulet:
    def __init__(self,x,y,dx,dy):
        self.rect = pygame.Rect(x,y,3,3)
        self.dx = dx * 10
        self.dy = dy * 10
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
    def draw(self,window):
        pygame.draw.rect(window,(255,255,0),self.rect)    

class Vertical_enemy:
    def __init__(self,x,y):
        self.speed = 4
        self.direction = ('up')
        self.bullets = []
        self.rect = pygame.Rect(x,y,square_size,square_size)
        self.cooldown = 2000
        self.lastshot = 0
    def shoot(self):
        currenttime = pygame.time.get_ticks()
        if currenttime - self.lastshot >= self.cooldown:
            if self.direction == "up":
                dx,dy = 0,-1
            else:
                dx,dy = 0,1
            bullet = Bulet (self.rect.centerx,self.rect.centery,dx,dy)
            self.bullets.append(bullet)
            self.lastshot = currenttime 

    def draw(self,window):
        pygame.draw.rect(window,blue,self.rect)
        for bulet in self.bullets:
            bulet.move()
            bulet.draw(window)
    def move(self,obstacles):
        if self.direction == "up":
            dy = -self.speed
        else:
            dy = self.speed
        new_y = self.rect.y + dy
        if new_y < 0 or new_y > window_height:
            if self.direction == "up":
                self.direction = "down"
                return
            else:
                self.direction = "up"
                return
        temprect = pygame.Rect(self.rect.x,new_y,square_size,square_size)
        for obstacle in obstacles:
            if temprect.colliderect(obstacle.rect):
                if self.direction == "up":
                    self.direction = "down"
                    return
                else:
                    self.direction = "up"
                    return
        self.rect.y = new_y

class Horizontal_enemy:
    def __init__(self,x,y):
        self.cooldown = 2000
        self.lastshot = 0
        self.speed = 4
        self.direction = ('right')
        self.bullets = []
        self.rect = pygame.Rect(x,y,square_size,square_size)
    def draw(self,window):
        pygame.draw.rect(window,blue,self.rect)
        for bulet in self.bullets:
            bulet.move()
            bulet.draw(window)
    def move(self,obstacles):
        if self.direction == "left":
            dx = -self.speed
        else:
            dx = self.speed
        new_x = self.rect.x + dx
        if new_x < 0 or new_x > window_widths:
            if self.direction == "right":
                self.direction = "left"
                return
            else:
                self.direction = "right"
                return
        temprect = pygame.Rect(new_x,self.rect.y,square_size,square_size)
        for obstacle in obstacles:
            if temprect.colliderect(obstacle.rect):
                if self.direction == "right":
                    self.direction = "left"
                    return
                else:
                    self.direction = "right"
                    return
        self.rect.x = new_x
    def shoot(self):
        currenttime = pygame.time.get_ticks()
        if currenttime - self.lastshot >= self.cooldown:
            if self.direction == "left":
                dx,dy = -1,0
            else:
                dx,dy = 1,0
            bullet = Bulet (self.rect.centerx,self.rect.centery,dx,dy)
            self.bullets.append(bullet)
            self.lastshot = currenttime 

class Game:
    def __init__(self):
        self.lastspawn = pygame.time.get_ticks()
        self.window = pygame.display.set_mode((window_widths,window_height))
        self.clock = pygame.time.Clock()
        self.state = ("menu")
        self.obstacles=[Obstacles(100,100),Obstacles(132,200),Obstacles(164,300),Obstacles(200,400),Obstacles(400,500),Obstacles(400,200),Obstacles(400,400),Obstacles(500,400),Obstacles(364,100)]
        self.player = Player(x=400,y=100)
        self.enemies = [Vertical_enemy(50,50),Vertical_enemy(500,100), Horizontal_enemy(50,50),Horizontal_enemy(0,200)]
    def run(self):
        while True:
            if self.state==("menu"):
                self.menu()
            elif self.state == ("game"):
                self.game()
            elif self.state == "results":
                self.results()
    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "game"
        self.window.fill(black)
        font = pygame.font.Font(None,75)
        text = font.render("battle.city",True,white)
        self.window.blit(text,(window_widths//2-text.get_width()//2,200))
        text = font.render("press space to start",True,white)
        self.window.blit(text,(window_widths//2-text.get_width()//2,350))
        pygame.display.update()
        self.clock.tick(60)
    def is_position_emty(self,x,y,obstacles):
        temp_rect = pygame.Rect(x,y,square_size,square_size)
        for obstacle in obstacles:
            if temp_rect.colliderect(obstacle.rect):
                return False
        return True
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastspawn >= 5 and len(self.enemies) < 5:
            x =  randint(0,window_widths - square_size)
            y = randint(0,window_height - square_size)
            if self.is_position_emty(x,y,self.obstacles):
                n = randint(0,1)
                if n == 0:
                    new_enemy = Vertical_enemy(x,y)
                else:
                    new_enemy = Horizontal_enemy(x,y)
                self.enemies.append(new_enemy)
                self.lastspawn = current_time
    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
        self.window.fill(black)
        for obstacle in self.obstacles:
            obstacle.draw(screen=self.window)
            for bullet in self.player.bullets[:]:
                if bullet.rect.colliderect(obstacle.rect):
                    self.player.bullets.remove (bullet)
        self.spawn_enemy()
        for enemy in self.enemies:
            enemy.move(self.obstacles)
            enemy.draw(self.window)
            enemy.shoot()
            for bulet in enemy.bullets[:]:
                if bulet.rect.colliderect(self.player.rect):
                    self.player.health -= 1
                    enemy.bullets.remove (bulet)
            for bullet in self.player.bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.player.bullets.remove (bullet)
                    self.enemies.remove (enemy)
        self.player.move(self.obstacles)
        self.player.draw(self.window)
        health_text = pygame.font.Font(None,35).render(F'HEALTH {self.player.health}',True,(0,255,0))
        self.window.blit(health_text,(window_widths/2-80,window_height-30))
        if self.player.health == 0:
            self.state = "results"
        self.clock.tick(60)
        pygame.display.update()

    def results(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.player.health = 2
                    self.state = "menu"
        self.window.fill(black)
        game_over_text = pygame.font.Font(None,100).render(F'GAME OVER ',True,(255,0,0))
        self.window.blit(game_over_text,(window_widths/2-200,window_height/2-50))
        pygame.display.update()
        self.clock.tick(60)

game = Game()
game.run()