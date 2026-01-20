import pygame
import sys
from player import *
from asteroid import *
from constants import *
from asteroidfield import *
from shot import *
from logger import log_state, log_event

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    #starts game, creates clock, delta time variable, screen, and player
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    font = pygame.font.SysFont(None, 32)
    
    #def groups for containers
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #def containers for classes
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    #init screen, player, field
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    input_box = pygame.Rect(screen.get_width() - 200, 20, 180, 40)

    asteroid_field = AsteroidField()
    
    #gameloop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        #adds score counter to top right
        pygame.draw.rect(screen, "black", input_box, 2)
        text_surface = font.render(f"SCORE: {player.score}", True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                print(f"Your scored {player.score} points! Good Job!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split(player)
            
        for image in drawable:
            image.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        

if __name__ == "__main__":
    main()
