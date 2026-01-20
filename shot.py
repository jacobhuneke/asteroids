from constants import *
import pygame
from circleshape import *
from shotecho import *

#Defines shot, as a small white circle with four shotecho variables
class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.se1 = None
        self.se2 = None
        self.se3 = None
        self.se4 = None

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, SHOT_RADIUS, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt