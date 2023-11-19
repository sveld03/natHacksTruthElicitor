## Checklist to run data collection:

##### 1. Connect OpenBCI USB Dongle and figure out which COM port it is connected to.
###### The COM port changes depending on which usb slot the Cyton is plugged into.
##### 2. Connect the Cyton & OpenBCI cap to the subject and test signal quality using OpenBCI GUI.
###### If signals are constantly railing, see if changing the gain from x24 (default) to x12 helps (first try to succeed w/ x24).
##### 3. Close OpenBCI GUI after clean signals are obtained to free up the Cyton's COM port.
##### 4. Plug in the FTDI via USB-B cable (If the GUI is ).
###### The GUI will connect to the first FTDI device it finds and will print the ID of the device.
###### If the device description is 'FT231X USB UART' instead of 'UM232R USB <-> Serial':
####### Then the GUI has connected to the Cyton (which is, annoyingly, also an FTDI device). Try switching the USB ports each device is plugged into.
###### If the GUI says DEVICE_NOT_FOUND:
####### Then the FTDI is not plugged in correctly, or you need to simply unplug everything and then plug back in to refresh the connection sockets.
##### 5. Connect the 4 wires that are disconnected after each use (*FUCKING THIS UP IS VERY BAD*).
###### Red wire --> Connects from DVDD of the Cyton to the positive rail on the breadboard where two 1M-ohm resistors are attached.
###### Blue wire --> Connects from GND (the GND *NEXT* to DVDD, not the GND next to VDD) to the negative rail on the breadboard with the orange and yellow wires in it.
###### Orange wire --> Connects from pin D12 on the Cyton to the unconnected end of the 1K-ohm resistor attached to the photocoupler with orange wires going into it.
###### Yellow wire --> Connects from pin D11 on the Cyton to the unconnected end of the 1K-ohm resistor attached to the photocoupler with yellow wires going into it.
###### If anything seems out of whack, carefully consult with the pictures in the folder: "circuit_pics"
##### 6. Open P3TE_Static_Variables.py
###### Ensure the com_port and gain_code match with the your setup.
##### 7. Before EACH trial ensure the static experiment variables match your experiment:
###### subject --> subject's name
###### n_trials --> the number of trials *per* image (i.e. total_flash_stimuli = n_trials * n_images)
###### down_time --> the time, in ms, the screen sits black in between each flash stimulus
###### flash_time --> the time, in ms, the screen presents each stimulus for
###### n_images --> the number of 1000x1000 pixel images in the "images" file following the format (images/image_#.png)
###### notes --> brief, and important, notes about the trial that will be included in the file name
##### 8. Run P3TE_Cyton_Data_Packager.py and ensure it connects to the Cyton and sends chunks every ~2 seconds.
###### This program will not close and *CAN* run indefinitely in the background as long as the Cyton is not disconnected from it.
####### Just make sure to periodically double check and make sure that it is still broadcasting chunks.
##### 9. Run P3TE_Data_Collector.py and ensure that it connects to the EEG stream and waits for the start signal from the FTDI.
###### It will also announce when it receives the start signal from the FTDI, which you will not be able to see while the GUI is running in full screen.
##### 10. Run P3TE_GUI.py, switch to the GUI window if it does not automatically do so, and move the mouse out of the user's way (to the right of the screen).
###### The 10 second countdown will allow the digital filters to settle and will give the user a moment to settle down physically.
##### 11. Periodically double check the signal quality with OpenBCI GUI
##### 12. Remember, you need to sanity check things frequently, there are *LOTS* of tests and sanity checks missing from the code at the moment.

