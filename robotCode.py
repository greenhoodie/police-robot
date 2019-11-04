

# Improvement Goals:
# * Better comments & organization
# * More functional loop
# * Arrays?
# * Able to turn off pin output easier for debugging


# Imports
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
from gpiozero import Motor, LED
import time

# Device ID's
label_wiimote_buttons = "Nintendo Wii Remote"
label_wiimote_accel = "Nintendo Wii Remote Accelerometer"


# Button ID's
buttonId = [103, 108, 105, 106, 304, 305, 407, 412, 316, 257, 258]
# Button Held States
buttonHeld = [False, False, False, False, False, False, False, False, False, False, False]

# Indexes for both arrays:
#  0   1   2     3    4   5   6     7     8   9   10
# UP DOWN LEFT RIGHT (A) (B) PLUS MINUS HOME (1) (2)


# Motors
leftWheels = Motor(16, 13)
rightWheels = Motor(6, 5)
lowerArm = Motor(10, 25)
upperArm = Motor(26, 21)
clawExtend = Motor(3, 4)
clawClose = Motor(17, 22)

# Inhibits
leftWheelsInh = LED(19) # note: I know this isn't an LED: the LED module simply works really easily
rightWheelsInh = LED(12)
lowerArmInh = LED(11)
upperArmInh = LED(20)
clawExtendInh = LED(2)
clawCloseInh = LED(27)

# Nerf gun
nerfMotors = LED(18)
nerfCoilBackward = LED(23)
nerfCoilForward = LED(24)

# Other State-tracking Variables
x = 0
y = 0
direction = "none"
delay = 0.5
already_shooting = False
debugMode = False # to disable pin output


# Find the Wiimote devices by name
wiimote_loc = "Not Found"
accel_loc = "Not Found"
devices = [InputDevice(path) for path in list_devices()]

while(wiimote_loc == "Not Found" or accel_loc == "Not Found"):
    print("Attempting to find remote...")
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if(device.name == label_wiimote_buttons):
            wiimote_loc = device.path
        if(device.name == label_wiimote_accel):
            accel_loc = device.path
    time.sleep(2) # try again in 2 seconds
print("Remote connected!")

# Make Input Device instances from the paths we found
wiimote_accel = InputDevice(accel_loc)
wiimote_buttons = InputDevice(wiimote_loc)

""" Main Loop """
while True:
    # Steering Values
    event = wiimote_accel.read_one()
    if event != None:
        # Getting tilt
        if(event.code == 3): # forward-backward tilt
            y = event.value
        if(event.code == 4): # left-right turn
            x = event.value
    
    
    # Button Status
    event = wiimote_buttons.read_one()
    if event != None:
        for id in range(len(buttonId)):
            if event.code == buttonId[id]:
                buttonHeld[id] = event.value
                
    
    ### Clear Buffer ###
    while wiimote_accel.read_one() != None:
        pass
    while wiimote_buttons.read_one() != None:
        pass
    
    
    ### Wheel Control ###
    if buttonHeld[4] and y>-90 and x<20 and x>-40 and direction != "forward":
        print("Going forward")
        direction = "forward"
        if not debugMode:
            leftWheelsInh.off()
            rightWheelsInh.off()
            time.sleep(delay)
            
            leftWheels.forward()
            rightWheels.backward()
            leftWheelsInh.on()
            rightWheelsInh.on()
        else:
            time.sleep(delay)
    elif buttonHeld[4] and y>-90 and x>=35 and direction != "left":
        print("Going left")
        direction = "left"
        if not debugMode:
            leftWheelsInh.off()
            rightWheelsInh.off()
            time.sleep(delay)
            
            leftWheels.backward()
            rightWheels.forward()
            leftWheelsInh.on()
            rightWheelsInh.on()
        else:
            time.sleep(delay)
    elif buttonHeld[4] and y>-90 and x<=-50 and direction != "right":
        print("Going right")
        direction = "right"
        if not debugMode:
            leftWheelsInh.off()
            rightWheelsInh.off()
            time.sleep(delay)
            leftWheels.forward()
            rightWheels.backward()
            leftWheelsInh.on()
            rightWheelsInh.on()
    elif buttonHeld[4] and y<-100 and direction != "backward":
        print("Going backward")
        direction = "backward"
        if not debugMode:
            leftWheelsInh.off()
            rightWheelsInh.off()
            time.sleep(delay)
            leftWheels.backward()
            rightWheels.backward()
            leftWheelsInh.on()
            rightWheelsInh.on()
    elif not buttonHeld[4] and direction != "none":
        print("Stop Moving.")
        direction = "none"
        if not debugMode:
            leftWheelsInh.off()
            rightWheelsInh.off()
            time.sleep(delay)
    
    ### Other Buttons ###
    # Lower Arm
    if buttonHeld[10]: # (2): Move Up
        print("Lower Arm up")
        if not debugMode:
            lowerArm.forward()
            lowerArmInh.on()
    elif buttonHeld[9]: # (1): Move Down
        print("Lower Arm down")
        if not debugMode:
            lowerArm.backward()
            lowerArmInh.on()
    else:
        lowerArmInh.off()
    
    # Upper Arm
    if buttonHeld[3]: # Right: Move Up
        print("Upper Arm up")
        if not debugMode:
            upperArm.forward()
            upperArmInh.on()
    elif buttonHeld[2]: # Left: Move Down
        print("Upper Arm down")
        if not debugMode:
            upperArm.backward()
            upperArmInh.on()
    else:
        upperArmInh.off()
    
    # Extend/Retract Claw
    if buttonHeld[0]: # Up: Extend
        print("Claw extend")
        if not debugMode:
            clawExtend.forward()
            clawExtendInh.on()
    elif buttonHeld[1]: # Down: Retract
        print("Claw retract")
        if not debugMode:
            clawExtend.backward()
            clawExtendInh.on()
    else:
        clawExtendInh.off()
    
    # Open/Close Claw
    if buttonHeld[7]: # (-): Close
        print("Close claw")
        if not debugMode:
            clawClose.forward()
            clawCloseInh.on()
    elif buttonHeld[6]: # (+): Open
        print("Open claw")
        if not debugMode:
            clawClose.backward()
            clawCloseInh.on()
    else:
        clawCloseInh.off()
    
    # Nerf Shooter
    if(buttonHeld[5]): # (B): Shoot
        if(not already_shooting): # haven't started shooting yet
            print("Start shooting!")
            if not debugMode:
                nerfMotors.on()
            time.sleep(0.5) # wait for motors to get up to speed
            already_shooting = True
        # whether we were already shooting or not
        #forward coil half a second
        if not debugMode:
            nerfCoilForward.on()
        print("Pew!")
        time.sleep(0.5)
        if not debugMode:
            #turn off
            nerfCoilForward.off()
            #back coil on
            nerfCoilBackward.on()
        time.sleep(0.5)
        if not debugMode:
            nerfCoilBackward.off()
    else: #done shooting
        if(already_shooting):
            print("Done shooting")
            already_shooting = False
            if not debugMode:
                nerfMotors.off()
    
    
