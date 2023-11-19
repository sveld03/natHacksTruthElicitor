# Hardware parameters

    # This must match the COM port you have the OpenBCI usb dongle plugged into
com_port = 'COM5';

    # Cyton board gain (all channels currently set to same gain bc I'm lazy)
    #TODO: consider not being lazy here :)
    # 0 = Gain x1
    # 1 = Gain x2
    # 2 = Gain x4
    # 3 = Gain x6
    # 4 = Gain x8
    # 5 = Gain x12
    # 6 = Gain x24
gain_code = 5;


# Experiment Parameters
subject = "Steven";
n_trials = 2;
n_images = 60;
n_suspect_images = 10;
n_irrelevant_images = 50;
down_time = 500;
flash_time = 200;
notes = "PTI_suspectx5_irrelevant_Jack";
label = 1;
target = 0;






# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv No touchy! vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

sampling_frequency = 250;

# Calculate EEG scale factor (uV/count)
SCALE_FACTOR_EEG = 0;
if(gain_code == 0):
    SCALE_FACTOR_EEG = (4500000)/1/(2**23-1);
elif(gain_code == 1):
    SCALE_FACTOR_EEG = (4500000)/2/(2**23-1);
elif(gain_code == 2):
    SCALE_FACTOR_EEG = (4500000)/4/(2**23-1);
elif(gain_code == 3):
    SCALE_FACTOR_EEG = (4500000)/6/(2**23-1);
elif(gain_code == 4):
    SCALE_FACTOR_EEG = (4500000)/8/(2**23-1);
elif(gain_code == 5):
    SCALE_FACTOR_EEG = (4500000)/12/(2**23-1);
elif(gain_code == 6):
    SCALE_FACTOR_EEG = (4500000)/24/(2**23-1);
else:
    raise Exception();

# Get File Name
label_file_name = "";
data_file_name = "";
import os.path;
for experiment_number in range(100):
    file_suffix = notes + "_(" + str(n_trials) + "_trials)(" + str(n_images) + "_images)(" + str(down_time) + "_downTime)(" + str(flash_time) + "_flashTime)_" + "label" + str(label) + ".csv";
    label_file_name = "trial_data/" + subject + "_" + str(experiment_number) + "_" + "labels_" + file_suffix;
    data_file_name = "trial_data/" + subject + "_" + str(experiment_number) + "_" + "data_" + file_suffix;
    if(not os.path.isfile(label_file_name) or not(os.path.isfile(data_file_name))):
        if(os.path.isfile(label_file_name) != os.path.isfile(data_file_name)):
            raise Exception("File count mismatch.");
        break;