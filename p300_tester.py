experimentnumber = "7-Yellow.csv"
subjectname = "StevenColor"
filename = subjectname + experimentnumber
ntrials = 100

if __name__ == "__main__":


    import pygame, random, time
    import numpy as np
    import winsound
    import csv
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 150  # Set Duration To 1000 ms == 1 second


    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    screen.fill(BLACK)

    init_time = time.time()

    count = 0

    c_tracker = np.zeros(ntrials*3)

    color_choices = np.repeat(['RED', 'YELLOW', 'BLUE'], ntrials)

    randx = 0
    randy = 0

    np.random.shuffle(color_choices)
    np.random.shuffle(color_choices)
    randomizer = False

    pygame.font.init() # you have to call this at the start, 
                    # if you want to use this module.
    my_font = pygame.font.SysFont('Comic Sans MS', 200)


    for countdown in range(10):
        screen.fill(BLACK)
        text_surface = my_font.render(str(10-countdown), False, (255, 255, 255))
        screen.blit(text_surface, (300,100))
        pygame.display.update()
        winsound.Beep(700, 150)
        time.sleep(.85)

    screen.fill(BLACK)
    text_surface = my_font.render("prog", False, (255, 255, 255))
    screen.blit(text_surface, (300,100))
    pygame.display.update()
    winsound.Beep(1300, 150)

    while count < ntrials*3:
        
        #screen.fill(BLACK)
        if (time.time() - init_time) >= 1.5:
            if not randomizer:
                randx = np.random.randint(0, 750)
                randy = np.random.randint(0, 350)
                
            random_color = color_choices[count]

            if random_color == 'RED':
                pygame.draw.polygon(screen, RED, ((50+randx,450+randy),
                                                (250+randx, 50+randy),
                                                (450+randx,450+randy)))
                c_tracker[count] = 1
            if random_color == 'YELLOW':
                pygame.draw.circle(screen, YELLOW, (250+randx,250+randy), 200)
                c_tracker[count] = 2
            if random_color == 'BLUE':
                pygame.draw.rect(screen, BLUE, (50+randx,50+randy, 400, 400))
                c_tracker[count] = 3
                
            if not randomizer:
                frequency = np.random.randint(440, 5000)
                winsound.Beep(frequency, duration)
                randomizer = True

            pygame.display.update()
            if (time.time() - init_time) >= 2:
                screen.fill(BLACK)
                pygame.display.update()
                init_time = time.time()
                count += 1
                randomizer = False
                
    print(c_tracker)
                
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerows([c_tracker])