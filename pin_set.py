import ftd2xx as ftd;
d = ftd.open(1);
print(d.getDeviceInfo());
OP = 0x03;
d.setBitMode(OP, 1); 
state = 0x00;
d.write(str(state));

print("Pins are reset to initial states.")