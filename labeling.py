import numpy as np
import csv
import matplotlib.pyplot as plt
import scipy.signal as sig

ntrials=80

csvfile = np.loadtxt("MateoEEG1.csv", delimiter=',', skiprows=1)
labels = np.loadtxt("MateoColor1.csv", delimiter=',')
labels = labels.astype(int)

# cum_signal = np.zeros((500, 8))
# for i in range(28500):
#     cum_signal[i % 500] += csvfile[i]
   
# cum_signal /= 57

# #plt.plot(range(0, 2000, 4), cum_signal[:,7])
# plt.plot(range(0, 2000, 4), cum_signal)

det_sig = np.zeros((500, 8))

red_cum_signal = np.zeros((500, 8))
yel_cum_signal = np.zeros((500, 8))
blu_cum_signal = np.zeros((500, 8))

j = 0
for i in range(0, 500*ntrials*3, 500):
    for chan in range(8):
        det_sig[:,chan] = sig.detrend(csvfile[i:i+500, chan])
    
    trial = labels[j]
    if (trial == 1):
        red_cum_signal += det_sig
    if (trial == 2):
        yel_cum_signal += det_sig
    if (trial == 3):
        blu_cum_signal += det_sig   
    j += 1    

red_cum_signal /= ntrials
yel_cum_signal /= ntrials
blu_cum_signal /= ntrials

bpfilt = sig.butter(4, (0.1, 12.5), 'bandpass', output='sos', fs=250)
for ch in range(8):        
    red_cum_signal[:,ch] = sig.sosfilt(bpfilt, red_cum_signal[:,ch]);
    yel_cum_signal[:,ch] = sig.sosfilt(bpfilt, yel_cum_signal[:,ch]);
    blu_cum_signal[:,ch] = sig.sosfilt(bpfilt, blu_cum_signal[:,ch]);

plt.subplot(331);
plt.plot(range(0, 2000, 4), red_cum_signal[:,0:3])
plt.subplot(332);
plt.plot(range(0, 2000, 4), red_cum_signal[:,3:6])
plt.subplot(333);
plt.plot(range(0, 2000, 4), red_cum_signal[:,6:])

plt.subplot(334);
plt.plot(range(0, 2000, 4), yel_cum_signal[:,0:3])
plt.subplot(335);
plt.plot(range(0, 2000, 4), yel_cum_signal[:,3:6])
plt.subplot(336);
plt.plot(range(0, 2000, 4), yel_cum_signal[:,6:])

plt.subplot(337);
plt.plot(range(0, 2000, 4), blu_cum_signal[:,0:3])
plt.subplot(338);
plt.plot(range(0, 2000, 4), blu_cum_signal[:,3:6])
plt.subplot(339);
plt.plot(range(0, 2000, 4), blu_cum_signal[:,6:])

plt.show()