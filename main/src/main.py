# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       adam                                                         #
# 	Created:      11/9/2026, 7:09:22 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       adam                                                         #
# 	Created:      11/9/2026, 7:09:22 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
from vex import *
brain = Brain()
controller = Controller()

#tick update time - in ms
update_interval = 20


#motor configuration
frontLeft = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
frontRight = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)


backLeft = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
backRight = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)

#lift motors
liftR = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
liftL = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)


#setup stopping modes
liftR.set_stopping(HOLD)
liftL.set_stopping(HOLD)
frontLeft.set_stopping(BRAKE)
backLeft.set_stopping(BRAKE)
frontRight.set_stopping(BRAKE)
backRight.set_stopping(BRAKE)




#qol function to wipe screen and reset cursor
def wipe_screen():
    controller.screen.clear_screen()
    controller.screen.set_cursor(1,1)

#function to check the sign (0, -1, 1) of a num
def get_sign(num):
    return (num > 0) - (num < 0)

#function to toggle global drivetrain motor speeds
def toggle_motor_speed():
    #allows function to access motor power and current speed config
    global motor_power
    global current_index

    #list of motor presets - 1st entry is the default
    motor_presets = [0.5, 0.75, 1]

    #code to detect and set motor speed
    length = len(motor_presets)
    if current_index == length-1:
        #wraps back to start of list if on the last entry
        current_index = 0
    else:
        current_index +=1
    motor_power = motor_presets[current_index]



#variables to keep track of motor speed multiplier
current_index = 0
motor_power = 0

#initialization to start motor script
toggle_motor_speed()
motor_power_old = motor_power

#sets 'a' button to toggle the motor speed function
controller.buttonA.pressed(toggle_motor_speed)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    while True:
        if motor_power_old != motor_power:
            wipe_screen()
            value = "speed: " + str(motor_power * 100) + "%"
            controller.screen.print(value)


        #poll input from controller
        turn = controller.axis4.position()/2
        forward = controller.axis3.position()
        lift_power = controller.axis2.position()

        #add turn values together; vex caps at 100%
        left_power = forward + turn
        right_power = forward - turn
            
        #caps input power
        if abs(intake_power) >= 100:
            intake_power = 100 * get_sign(intake_power)

        #controls the chain bar power
        if controller.buttonR2.pressing():
            chain_power = 10
        elif controller.buttonL2.pressing():
            chain_power = -10
        else:
            chain_power = 0

        #controls the claw motor power
        if controller.buttonLeft.pressing():
            claw_power = 10
        elif controller.buttonRight.pressing():
            claw_power = -10
        else:
            claw_power = 0

        #calculates the correct motor speeds for the robot
        left_power = int(left_power * motor_power)
        right_power = int(right_power * motor_power)

        #drivetrain spin code
        if left_power != 0:
            frontLeft.spin(FORWARD, left_power, PERCENT)
            backLeft.spin(FORWARD, left_power, PERCENT)
        else:
            frontLeft.stop()
            backLeft.stop()

        if right_power != 0:
            frontRight.spin(FORWARD, right_power, PERCENT)
            backRight.spin(FORWARD, right_power, PERCENT)
        else:
            frontRight.stop()
            backRight.stop()

        #lift
        if lift_power != 0:
            liftR.spin(FORWARD, lift_power, PERCENT)
            liftL.spin(FORWARD, lift_power, PERCENT)
        else:
            liftR.stop()
            liftL.stop()


        #keeps old motor speed in memory to determine when to update motor speed and lcd
        motor_power_old = motor_power
        wait(update_interval, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()