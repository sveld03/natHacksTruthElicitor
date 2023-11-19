from P3TE_Static_Variables import data_file_name, label_file_name, label, n_trials, n_images, sampling_frequency, down_time, flash_time;

import csv;
import numpy as np;
from pylsl import StreamInlet, resolve_byprop;
import pygame

# Grab the data stream being streamed by P3TE_Cyton_Data_Packager.py
print("looking for an EEG stream");
stream = resolve_byprop('source_id', 'Cyton_Data_Packager');
inlet = StreamInlet(stream[0]);
print("Got stream!");

# Init stuff
start_signal_received = False
saved_eeg_data = np.zeros((int(np.ceil(sampling_frequency*n_images*((down_time+flash_time)/1000)*n_trials+300*sampling_frequency)), 10))
header = ["channel1", "channel2", "channel3", "channel4", "channel5", "channel6", "channel7", "channel8","Trigger","Shutdown"]

try:
    # Init data sample index
    sample_index = 0
    
    print("Waiting for start signal...");
    while True:
        
        # Get a new sample until a start signal is detected
        if not start_signal_received:
            
            sample, _ = inlet.pull_sample()
                   
            if(sample[8] == 1):
                start_signal_received = True;
                print("Start signal received.");
            
        # Pull in a new chunk
        if start_signal_received:
                        
            chunk, _ = inlet.pull_chunk()
            
            if len(chunk) > 0:

                saved_eeg_data[sample_index:sample_index+np.shape(chunk)[0]] = np.array(chunk)
                sample_index += np.shape(chunk)[0]
                
                # Check if a shutdown signal has been detected
                if(saved_eeg_data[sample_index-1, 9] == 1):
                    print("Shutdown signal received");
                    break;
        
except KeyboardInterrupt:
            
    # Pull in one extra chunk if there was a keyboard interrupt        
    chunk, _ = inlet.pull_chunk()
            
    if len(chunk) > 0:
        saved_eeg_data[sample_index:sample_index+np.shape(chunk)[0]] = np.array(chunk)
        sample_index += np.shape(chunk)[0]

                
# Print the data to a csv file
with open(str(data_file_name), 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header);
    writer.writerows(saved_eeg_data[:sample_index]);
    print('Data collected and exported!')
    
from P3TE_correlation_analysis import spit_out_answers as ans;

d = str(data_file_name);
l = str(label_file_name);
guess = ans(d, l, 0);

image = pygame.image.load("images/thispersondoesnotexist-" + str(guess+60) + ".com.jpeg")

# Init pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080))

req = False;
while(not req):

    screen.fill((0, 0, 0))
    screen.blit(image, (460,40))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_RETURN:
                req = True;