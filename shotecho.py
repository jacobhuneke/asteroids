import pygame
from circleshape import *
from constants import *

#defines the shot echo, same as the Shot class but unable to cause asteroids to split
class Shotecho(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, SHOT_RADIUS, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

