import pygame
from circleshape import *
from constants import *
from shot import *
from shotecho import *

#Player Class with CircleShape parent
#constructor from parent with additional rotation attribute
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.score = 0
    
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    #overrides CircleShape draw()
    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)
        

    #updates player's rotation variable by the speed * delta time
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    #updates the player rotation given input by the wasd and space keys
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt
        
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)   
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    #updates the player location data
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    #if the player has not shot within the duration of the cooldown, fires one shot followed by four shot echo circle shape objects
    #creating a cometlike trail
    def shoot(self):
        if self.shot_cooldown <= 0:  
            shot = Shot(self.position.x, self.position.y)
            shot.se1 = Shotecho(self.position.x, self.position.y)
            shot.se2 = Shotecho(self.position.x, self.position.y)
            shot.se3 = Shotecho(self.position.x, self.position.y)
            shot.se4 = Shotecho(self.position.x, self.position.y)

            vel = pygame.Vector2(0, 1)
            rotated_vec = vel.rotate(self.rotation)
            scaled = rotated_vec * PLAYER_SHOOT_SPEED
            shot.velocity = scaled
            shot.se1.velocity = scaled * 0.98
            shot.se2.velocity = scaled * 0.96
            shot.se3.velocity = scaled * 0.94
            shot.se4.velocity = scaled * 0.92
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS