# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

time_counter = 0
wait_counter = 0
waiting = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if not waiting:
        current_picture = int(time_counter/60)+1
        im = pygame.transform.scale(pygame.image.load(f"Faces/thispersondoesnotexist-{current_picture}.com.jpeg"), (500, 500))
        pygame.Surface.blit(screen, im, (390, 110))
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

    if not waiting:
        time_counter += 1

    if time_counter%60 == 0:
        waiting = True

    if waiting and wait_counter < 30:
        wait_counter += 1
    elif waiting and wait_counter == 30:
        waiting = False
        wait_counter = 0

    print(time_counter)

pygame.quit()