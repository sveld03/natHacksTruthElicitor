# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

experimentnumber = "7-Yellow.csv"
subjectname = "StevenEEG"
filename = subjectname + experimentnumber

from p300_tester import ntrials

import csv
import numpy as np
from matplotlib import pyplot as plt
from pylsl import StreamInlet, resolve_stream, resolve_byprop

print("looking for an EEG stream")
stream = resolve_byprop('source_id', 'Cyton_Data_Packager')
print("Got stream!")

# create new inlet to read from stream
inlet = StreamInlet(stream[0])

aux_received = False
saved_eeg_data = np.zeros((250*2*3*ntrials+30*250, 8))

header = ["channel1", "channel2", "channel3", "channel4", "channel5", "channel6", "channel7", "channel8"]

try:
    sample_ind = 0
    reg_ind = 0
    
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        if not aux_received:
            
            sample, _ = inlet.pull_sample()
                   
            if sample[8] == 1:
                aux_received = True
                print("Prog pressed")
            
        if aux_received:
                        
            chunk, _ = inlet.pull_chunk()
            
            if len(chunk) > 0:
                print(np.shape(chunk))  
                print(np.shape(saved_eeg_data))         
                print(reg_ind)     

                saved_eeg_data[reg_ind:reg_ind+np.shape(chunk)[0]] = np.array(chunk)[:,0:8]
                reg_ind += np.shape(chunk)[0]
        
except KeyboardInterrupt:
                    
    chunk, _ = inlet.pull_chunk()
            
    if len(chunk) > 0:
        #print(chunk)                
        saved_eeg_data[reg_ind:reg_ind+np.shape(chunk)[0]] = np.array(chunk)[:,0:8]
                
    with open(str(filename), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerow(header)
        writer.writerows(saved_eeg_data[:250*2*3*ntrials])
    print('Data collected and exported!')
    
    