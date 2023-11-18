import numpy as np
import sklearn
import csv
import matplotlib.pyplot as plt
import scipy.signal as sig
from scipy.stats import zscore
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pandas as pd


ntrials=100

# load the data and cut off the trash data from the end
data = pd.read_csv("Steven_0_data_general_P300_right_side_screen(2_trials)(139_images)(1300_downTime)(700_flashTime)_labelExpementalData.csv")
data = data.to_numpy()[:139000, :8]

# chunk the data into each 2000 ms ephoch with 1300 ms black sceen followed by 700 ms image
data = np.reshape(data, (278, 500, 8))

# average across channels
data = np.mean(data, axis=2)

# bandpass filter
bpfilt = sig.butter(4, (1, 20), 'bandpass', output='sos', fs=250)

# normalize each epoch
for i in range(data.shape[0]):
    data[i] = zscore(data[i])

# get last 700 ms of each epoch (image)
only_im = np.empty((278, 125))
for i in range(data.shape[0]):
    only_im[i] = data[i][375:]

# apply filter
only_im_filtered = np.empty((278, 125))
for i in range(data.shape[0]):
    only_im_filtered[i] = sig.sosfilt(bpfilt, only_im[i])

# get last 1300 ms of each epoch (image)
only_control = np.empty((278, 375))
for i in range(data.shape[0]):
    only_control[i] = data[i][:375]

# apply filter
only_control_filtered = np.empty((278, 375))
for i in range(data.shape[0]):
    only_control_filtered[i] = sig.sosfilt(bpfilt, only_control[i])

# trim the epoch so it's sized equally to image period
only_control_buffered = np.empty((278, 125))
for i in range(data.shape[0]):
    only_control_buffered[i] = only_control_filtered[i][125:-125]

plt.title('P300 Signal')
plt.ylim(-0.1, 0.1)
plt.plot(np.mean(only_im_filtered, axis=0), color='red')
plt.show()

plt.title('Rest Signal')
plt.ylim(-0.1, 0.1)
plt.plot(np.mean(only_control_buffered, axis=0), color='blue')
plt.show()

# X and y are the concatenations of this data
X = np.vstack((only_im_filtered, only_control_buffered))
y = np.concatenate((np.zeros(278), np.ones(278)))

# get train and test indices
shuffled_indices = np.arange(556)
np.random.shuffle(shuffled_indices)
train_indices = shuffled_indices[:400]
test_indices = shuffled_indices[400:]

# make X train/test, y train/test
X_train, y_train = X[train_indices], y[train_indices]
X_test, y_test = X[test_indices], y[test_indices]

# classifier
clf = SVC()
clf.fit(X_train, y_train)

acc_message  = f'Accuracy: {np.round(np.mean(clf.predict(X_test) == y_test), 2)}'

cm = confusion_matrix(y_test, clf.predict(X_test), labels=[0, 1])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot()
disp.ax_.set_title(acc_message)
plt.show()