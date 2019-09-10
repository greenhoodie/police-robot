# Wiimote Test #1
# (c) Jessie Newman 2019
# Gr. 12 Digital Electronics

# To-do Next Time:
    # From tutorial, have console just show char
        # instead of all that junk.
    # Add nunchuck as well, and try to get
        #both working simutaniously
    # Not really in this file, but look through
        # the old robot code and salvage what you can


#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices


# DEVICE NAMES FOR FUTURE REFERENCE
label_wiimote_motion = "Nintendo Wii Remote Motion Plus"
label_wiimote_nunchuck = "Nintendo Wii Remote Nunchuk"
label_wiimote_buttons = "Nintendo Wii Remote"
label_wiimote_IR = "Nintendo Wii Remote IR"
label_wiimote_accel = "Nintendo Wii Remote Accelerometer"


# Wiimote butotns codes
up = 103
down = 108
left = 105
right = 106
aBtn = 304
bBtn = 305
plus = 407
minus = 412
home = 316
btn1 = 257
btn2 = 258



# find the wiimote, no matter the event number
# will obv need error handling l8r
buttons_location = "Not Found"
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    if(device.name == label_wiimote_buttons):
        buttons_location = device.path
if buttons_location == "Not Found":
    print "Error finding wiimote. "

# creates object to store data
wiimote_buttons = InputDevice(buttons_location)

# event.value is 1 on press and 0 on release
# no built in status of holding a button, so
# would need to implement myself.
for event in wiimote_buttons.read_loop():
    print(categorize(event))
    print(event.value)