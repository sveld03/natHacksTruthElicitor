# natHacks EEG P300 Truth Elicitor

### General Setup

1. The subject will begin alone in a room and will have access to 3 **safes**. Each safe will contain a distinct object and corresponds to a distinct **buttons**.

2. The subject will **steal** an item from one of the safes and hide it on their person or put it in a nearby bag of their own.
  
3. The 3 safes will be set aside (todo: test in sight setting vs out of sight setting).

4. The subject will then engage with the Truth Elicitor by looking at the **GUI** while pressing the correseponding **buttons**.

##### Blue Safe
- contains a blue, rectangular credit card
- associated with the blue, square button
##### Red Safe
- contains a red, trapezoidal box cutter
- associated with the red, triangular button
##### Yellow Safe
- contains a yellow, cylindrical tube of chapstick
- associated with the yellow, circular button

##### GUI
- once initiated, the GUI will display a black screen for 3 seconds
- the GUI will then randomly display one of the following images for 0.5 seconds:
    - an image of a blue square
    - an image of a red triangle
    - an image of a yellow circle
- the user will then react as rapidly as possible to press the physical button corresponding to the image displayed on screen
- the process then repeats for the desired number of iterations

##### Data Collection
- the user will wear an EEG headset while engaging with the truth elicitor
- when a particular image is shown to the user, the EEG response to that image will be recorded and associated with that image
- the average EEG response to each image will be accumulated and averaged over time for analysis

##### EEG Configuration
- CH1-C3, CH2-Cz, CH3-C4, CH4-P3, CH5-Pz, CH6-P4, CH7-O1, CH8-O2
- 4th order butterworth bandpass filter between 0.1 Hz and 12.5 Hz
