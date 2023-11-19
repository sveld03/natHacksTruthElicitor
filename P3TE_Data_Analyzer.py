from P3TE_Static_Variables import sampling_frequency;
import numpy as np;
import matplotlib.pyplot as plt;
import scipy.signal as sig;

# Get the target image id
#target_image_id = int(input("What was the target image id?\n"));
#TODO: switch this back
target_image_id = 6;
probe_image_id = 3

# Length of P300 response to evaluate (2s)
response_length = sampling_frequency * 1;

# Pull label data
label_file = "trial_data/Steven_0_labels_faces_2nd_batch_target_6_(30_trials)(10_images)(1300_downTime)(700_flashTime)_label3.csv";
labels = (np.loadtxt(label_file, delimiter=',')).astype(int);

# Extract trial parameters
n_images = int(max(labels)+1);
n_flashes = int(len(labels));
n_trials = int(n_flashes/n_images);

# Pull sample data
data_file = "trial_data/Steven_0_data_faces_2nd_batch_target_6_(30_trials)(10_images)(1300_downTime)(700_flashTime)_label3.csv";
samples = np.loadtxt(data_file, delimiter=',', skiprows=1);

# Init filter
bpfilt = sig.butter(4, (1, 12.5), 'bandpass', output='sos', fs=250)
# Apply filter to each electrode
for channel in range(8): 
    # Detrend channel
    samples[:,channel] = sig.detrend(samples[:,channel]);   
    # Filter channel
    samples[:,channel] = sig.sosfilt(bpfilt, samples[:,channel]); 
    
# Find end-of-countdown index and trim off countdown samples
eoc_index = np.where(samples[:,8] == 0)[0][0];
print("Countdown samples appeared to take up " + str(eoc_index/sampling_frequency) + " seconds.");
samples = samples[eoc_index:,:];

# Check if a shutdown signal was found
if(np.sum(samples[:,9]) == 0):
    print("Warning! No shutdown signal was detected.");

# Init response signals
target_signals = np.zeros((n_trials,response_length,8));
target_flash_index = 0;

probe_signals = np.zeros((n_trials,response_length,8))
probe_flash_index = 0;

non_target_signals = np.zeros((n_trials*(n_images-2),response_length,8));
non_target_flash_index = 0;

# Loop through the data and find the data for each flash
last_flash_index = 0;
for flash in range(n_flashes):
    
    if(flash == n_flashes-1):
        continue;
        
    # Find start index of this flash
    start_index = np.where(samples[last_flash_index:,8] == 1)[0][0]+last_flash_index;
    
    # Check if this was a target flash or not & append accordingly
    if(labels[flash] == target_image_id):
        target_signals[target_flash_index,:,:] = samples[start_index:start_index+response_length,:8]
        target_flash_index += 1;
    elif(labels[flash] == probe_image_id):
        probe_signals[probe_flash_index,:,:] = samples[start_index:start_index+response_length,:8]
        probe_flash_index += 1;
    else:
        non_target_signals[non_target_flash_index,:,:] = samples[start_index:start_index+response_length,:8]
        non_target_flash_index += 1;
            
    # Reset for next flash seek
    last_flash_index = np.where(samples[start_index:,8] == 0)[0][0]+start_index;

# Calc avg responses
avg_target_response = np.mean(target_signals, axis=0);
avg_probe_response = np.mean(probe_signals ,axis=0)
avg_non_target_response = np.mean(non_target_signals[:,:,:], axis=0);

# Visualize responses
plt.figure(1);
plt.subplot(331);
plt.plot(avg_target_response[:,0:3]);
plt.subplot(332);
plt.plot(avg_target_response[:,3:6]);
plt.subplot(333);
plt.plot(avg_target_response[:,6:8]);
plt.subplot(334);
plt.plot(avg_non_target_response[:,0:3]);
plt.subplot(335);
plt.plot(avg_non_target_response[:,3:6]);
plt.subplot(336);
plt.plot(avg_non_target_response[:,6:8]);
plt.subplot(337);
plt.plot(avg_probe_response[:,0:3]);
plt.subplot(338);
plt.plot(avg_probe_response[:,3:6]);
plt.subplot(339);
plt.plot(avg_probe_response[:,6:8]);

plt.figure(1);
plt.subplot(131);
plt.plot(np.mean(avg_target_response[:,0:3], axis=1), c='b');
plt.plot(np.mean(avg_non_target_response[:,0:3], axis=1), c='r');
plt.plot(np.mean(avg_probe_response[:,0:3], axis=1), c='g');
plt.subplot(132);
plt.plot(np.mean(avg_target_response[:,3:6], axis=1), c='b');
plt.plot(np.mean(avg_non_target_response[:,3:6], axis=1), c='r');
plt.plot(np.mean(avg_probe_response[:,3:6], axis=1), c='g');
plt.subplot(133);
plt.plot(np.mean(avg_target_response[:,6:8], axis=1), c='b');
plt.plot(np.mean(avg_non_target_response[:,6:8], axis=1), c='r');
plt.plot(np.mean(avg_probe_response[:,6:8], axis=1), c='g');

plt.show()