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
    high_score = 0

    
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
    Shotecho.containers = (updatable, drawable)

    #init screen, player, field
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    input_box = pygame.Rect(screen.get_width() - 200, 20, 180, 40)

    asteroid_field = AsteroidField()
    
    def update_leaderboard():
        # Write to a .md file manually
        with open('leaderboard.md', 'w') as f:
            f.write('-------ASTEROIDS LEADERBOARD-------\n')
            f.write('---RANK------PLAYER-----SCORE------\n')
            f.write(f'----1-------{leader}----{player.score}------\n')
            f.write(f'----2-------SECOND-----score------\n')
            f.write(f'----3----------THIRD-----score------\n')

    #gameloop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #sets screen to purple
        screen.fill((51, 0, 51))

        #adds score counter to top right
        pygame.draw.rect(screen, (51, 0, 51), input_box, 2)
        text_surface = font.render(f"SCORE: {player.score}", True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                #ends game if player ran into any asteroids
                log_event("player_hit")
                pygame.display.quit()
                print("Game over!")
                print(f"Your scored {player.score} points! Good Job!")
                if player.score > high_score:
                    leader = input("You set the high score! Enter your name: ")
                    update_leaderboard()
                    high_score = player.score
                with open('leaderboard.md', 'r', encoding='utf-8') as file:
                    print(file.read())   
                    ##NEED NEW FUNCTION TO OVERWRITE LEADERBOARD.MD
                sys.exit()
            #checks to see if player shot any asteroids, deletes shot and splits asteroid
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()    
                    shot.se1.kill()
                    shot.se2.kill()
                    shot.se3.kill()
                    shot.se4.kill()                
                    asteroid.split(player)
            
        #draws images on the screen in their new positions after updated by dt
        for image in drawable:
            image.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        

if __name__ == "__main__":
    main()
