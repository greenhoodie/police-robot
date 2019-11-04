# Robot Code
# (c) Jessie Newman 2019
# Gr. 12 Digital Electronics

# To-do Next:
    # Need to have start at startup and we're ready!


#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
from gpiozero import Motor, LED
import time

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


# Button Holds Variables
up_isHeld = False
down_isHeld = False
left_isHeld = False
right_isHeld = False
aBtn_isHeld = False
bBtn_isHeld = False
plus_isHeld = False
minus_isHeld = False
home_isHeld = False
btn1_isHeld = False
btn2_isHeld = False

# find the wiimote, no matter the event number
# will obv need error handling l8r
wiimote_loc = "Not Found"
motion_loc = "Not Found"
devices = [InputDevice(path) for path in list_devices()]

while(wiimote_loc == "Not Found" or motion_loc == "Not Found"):
    print("Attempting to find remote...")
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if(device.name == label_wiimote_buttons):
            wiimote_loc = device.path
        if(device.name == label_wiimote_accel):
            motion_loc = device.path
    time.sleep(2)
print("Remote connected!")

# creates object to store data
myDevices = map(InputDevice, (wiimote_loc, motion_loc))
myDevices = {dev.fd: dev for dev in myDevices}

#wiimote_buttons = InputDevice(wiimote_loc)
#wiimote_nunchuck = InputDevice(nunchuck_loc)
leftRight = 0;
y = 0;
direction = "none"
delay = 0.5
nerfAlreadyShooting = false;

while True:
    r, w, x = select(myDevices, [], [])
    for fd in r:
        for event in myDevices[fd].read():
            # Getting button events
            if event.type == ecodes.EV_KEY:
                if event.code == up:
                    #print("Up")
                    up_isHeld = event.value
                elif event.code == down:
                    #print("Down")
                    down_isHeld = event.value
                elif event.code == left:
                    #print("Left")
                    left_isHeld = event.value
                elif event.code == right:
                    #print("Right")
                    right_isHeld = event.value
                elif event.code == aBtn:
                    #print("(A)")
                    aBtn_isHeld = event.value
                elif event.code == bBtn:
                    #print("(B)")
                    bBtn_isHeld = event.value
                elif event.code == plus:
                    #print("(+)")
                    plus_isHeld = event.value
                elif event.code == minus:
                    #print("(-)")
                    minus_isHeld = event.value
                elif event.code == home:
                    #print("(Home)")
                    home_isHeld = event.value
                elif event.code == btn1:
                    #print("(1)")
                    btn1_isHeld = event.value
                elif event.code == btn2:
                    #print("(2)")
                    btn2_isHeld = event.value
            
            # Getting tilt
            if(event.code == 3): # forward-backward tilt
                y = event.value
            if(event.code == 4): # left-right turn
                leftRight = event.value
            
            #### Motor Control ####
            # Wheels
            if(aBtn_isHeld and y>-90 and leftRight<20 and leftRight>-40 and direction != "forward"): # forwards
                print("Going forwards")
                direction = "forward"
                leftWheelsInh.off()
                rightWheelsInh.off()
                time.sleep(delay)
                
                leftWheels.forward()
                rightWheels.backward()
                leftWheelsInh.on()
                rightWheelsInh.on()
            elif(leftRight>=35 and y>-90 and aBtn_isHeld and direction != "left"): # left
                print("Going left")
                direction = "left"
                leftWheelsInh.off()
                rightWheelsInh.off()
                time.sleep(delay)
                leftWheels.backward()
                rightWheels.forward()
                leftWheelsInh.on()
                rightWheelsInh.on()
            elif(leftRight<=-50 and y>-90 and aBtn_isHeld and direction != "right"): # right
                print("Going right")
                direction = "right"
                leftWheelsInh.off()
                rightWheelsInh.off()
                time.sleep(delay)
                leftWheels.forward()
                rightWheels.backward()
                leftWheelsInh.on()
                rightWheelsInh.on()
            elif(y<-100 and aBtn_isHeld and direction != "backward"): # backwards by tilting backwards
                print("Going backward")
                direction = "backward"
                leftWheelsInh.off()
                rightWheelsInh.off()
                time.sleep(delay)
                leftWheels.backward()
                rightWheels.backward()
                leftWheelsInh.on()
                rightWheelsInh.on()

            elif(not (aBtn_isHeld) and direction != "none"): # wheels aren't moving
                direction = "none"
                print("Not moving")
                leftWheelsInh.off()
                rightWheelsInh.off()
                time.sleep(delay)
            
            # Lower Arm
            if(btn1_isHeld): # move up
                print("Lower Arm up")
                lowerArm.forward()
                lowerArmInh.on()
            elif(btn2_isHeld): # move down
                print("Lower Arm down")
                lowerArm.backward()
                lowerArmInh.on()
            else: # not moving
                lowerArmInh.off()
            
            # Upper Arm
            if(right_isHeld): # move up
                print("Upper arm up")
                upperArm.forward()
                upperArmInh.on()
            elif(left_isHeld): # move down
                print("Upper arm down")
                upperArm.backward()
                upperArmInh.on()
            else: # not moving
                upperArmInh.off()
            
            # Extend/Retract Claw
            if(down_isHeld): # extend
                print("Extend claw")
                clawExtend.forward()
                clawExtendInh.on()
            elif(up_isHeld): # retract
                print("Retract claw")
                clawExtend.backward()
                clawExtendInh.on()
            else: # not moving
                clawExtendInh.off()
            
            # Claw Open/Close
            if(minus_isHeld): # close claw
                print("Close claw")
                clawClose.forward()
                clawCloseInh.on()
            elif(plus_isHeld): # open claw
                print("Open claw")
                clawClose.backward()
                clawCloseInh.on()
            else: # not moving
                clawCloseInh.off()
            
            # Nerf Shooter
            if(bBtn_isHeld):
                if(!nerfAlreadyShooting):
                    print("Start shooting!")
                    nerfMotors.on()
                    time.sleep(0.5) # wait for motors to get up to speed
                # whether we were already shooting or not
                #forward coil half a second
                nerfCoilForward.on()
                time.sleep(0.5)
                #turn off
                nerfCoilForward.off()
                #back coil on
                nerfCoilBackward.on()
                time.sleep(0.5)
            else: #done shooting
                if(nerfAlreadyShooting):
                    print("Done shooting")
                    nerfAlreadyShooting = false
                    nerfMotors.off()
            
