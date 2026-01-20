import pygame
from circleshape import *
from constants import *
from logger import log_event
import random
from player import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt

#defines how asteroids split when shot
    def split(self, player):
        self.kill()
        #if the smallest type of asteroid, player earns 3 pts and the asteroid is gone
        if self.radius <= ASTEROID_MIN_RADIUS:
            player.score += 3
            return
        
        log_event("asteroid_split")

        #sets angles for two newly created asteroids
        angle = random.uniform(20, 50)
        first_new = self.velocity.rotate(angle)
        second_new = self.velocity.rotate(angle * -1)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        #creates two new asteroids
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_new * 1.2
        second_asteroid.velocity = second_new * 1.2

        if new_radius == ASTEROID_MIN_RADIUS:
            player.score += 2
        else:
            player.score += 1

