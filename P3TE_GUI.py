from P3TE_Static_Variables import n_trials, n_images, label, down_time, flash_time, label_file_name;

import pygame, time
import numpy as np
import winsound
import csv

# Attempt to grab the FTDI device
import ftd2xx as ftd; # Communicating the the UM232R FTDI chip for triggering
d = ftd.open(1);
print(d.getDeviceInfo());
OP = 0x03;           # Bit mask for output D0 & D1
d.setBitMode(OP, 1);  # Set pin as output, and async bitbang mode
state = 0x00;
d.write(str(state));
print("FTDI initialized.");
        
# Load flash images
images = [None] * n_images;

# images[0] = pygame.image.load("Faces/thispersondoesnotexist-11.com.jpeg")
for image_id in range(n_images):
    """ first 10 images """
    images[image_id] = pygame.image.load('images/image_'+str(image_id)+'.png')

    """ next 10 images"""
    # images[image_id] = pygame.image.load('images/thispersondoesnotexist-' + str(image_id + 1) + '.com.jpeg')

    """ third batch """
    # images[image_id] = pygame.image.load('images/thispersondoesnotexist-' + str(image_id + 11) + '.com.jpeg')

    """ basic P300 generation using a shit ton of images """
    # images[image_id + 1] = pygame.image.load('Faces/thispersondoesnotexist-' + str(image_id + 21) + '.com.jpeg')

frequency = 2500  # Set Starting Frequency To 2500 Hertz
beep_duration = 150; # ms

# Define color shorthands
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Init pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
screen.fill(BLACK)

# Track number of flashes
n_flashed = 0

# Create pseudo-randomized vector of image choices
image_labels = np.repeat(np.arange(n_images), n_trials)
np.random.shuffle(image_labels);
# for image in range(n_images * n_trials):
#     is_probe = np.random.randint(10)
#     if(is_probe == 1):
#         image_labels[image] = label

# Font for writing text to screen
pygame.font.init();
my_font = pygame.font.SysFont('Comic Sans MS', 200);

# Send start signal to data collector
state = 0x01;
d.write(str(state));

# Print 5sec countdown to screen
# !! Don't change this. !! The digital filter needs time to settle down. !!
for countdown in range(10):
    screen.fill(BLACK);
    text_surface = my_font.render(str(10-countdown), False, (255, 255, 255));
    screen.blit(text_surface, (300,100));
    pygame.display.update();
    winsound.Beep(700, 150);
    time.sleep(.85);

# Reset ftdi trigger
state = 0x00;
d.write(str(state));

# Re-init black screen
screen.fill(BLACK);
pygame.display.update();
winsound.Beep(1300, 100);

# Start timer
init_time = time.time()

# Random position variables
randx = 0;
randy = 0;
randomizer = False; """ SHOULD BE FALSE FOR EVERYTHING BUT GENERAL P300 """
expecting_reaction = False;
reaction_timer = 0;

# Loop through all trials
while n_flashed < n_trials*n_images:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_RETURN:
                expecting_reaction = False;

    # Check if it is time for next flash
    if (time.time() - init_time) >= down_time/1000.0:

        # Check reaction timer
        if(expecting_reaction and time.time()-reaction_timer>0.35):
            
            winsound.PlaySound('error_beep.wav', winsound.SND_ASYNC)
            time.sleep(.1)
            winsound.PlaySound('error_beep.wav', winsound.SND_ASYNC)

            expecting_reaction = False;

        # Get image id for this trial
        image_id = image_labels[n_flashed];

        # Randomize a new position if one is needed (also update ftdi pins)
        if not randomizer:
            randx = np.random.randint(0, 750)
            randy = np.random.randint(0, 350)
            state = 0x01
            d.write(str(state));
            
        screen.blit(images[image_id], (460,40))

        # Note that a new position has already been randomized for this flash
        if not randomizer:
            #frequency = np.random.randint(440, 5000)
            #winsound.Beep(frequency, beep_duration)
            randomizer = True
            if(image_id == label):
                expecting_reaction = True;
                reaction_timer = time.time();

        pygame.display.update()
        if (time.time() - init_time) >= (down_time+flash_time)/1000.0:
            screen.fill(BLACK)
            pygame.display.update()
            init_time = time.time()
            n_flashed += 1
            state = 0x00;
            d.write(str(state));
            randomizer = False
            
# Pause for a few seconds, then send shutdown signal to data collector
time.sleep(3.5);
state = 0x02
d.write(str(state));
                            
with open(label_file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerows([image_labels])