from machine import Pin, PWM
import time

#used as guides:
#pwm: https://linuxhint.com/pwm-esp32-micropython-thonny-ide/

#inputs
butt1 = Pin(5, Pin.IN, Pin.PULL_UP) #cycle thru 15 20 25 30
butt2 = Pin(6, Pin.IN, Pin.PULL_UP) #start/reset
#Pin.PULL_UP is bc there is no resistor attached
#not press = 1
#pressed = 0

#leds
red = PWM(Pin(8)) #timer finished
green = PWM(Pin(7)) #timer working
blue = PWM(Pin(9)) #waiting mode

Frequency = 1000 #0 to 78125, website uses 5k

red.freq(Frequency)
blue.freq(Frequency)
green.freq(Frequency)

#motor configuration
STEPS_PER_REVOLUTION = 2048 # like variable says, number of steps to complete 1 revolution

#motor control pins
IN1 = Pin(1, Pin.OUT)
IN2 = Pin(2, Pin.OUT)
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)

#wave stepping sequence
step_sequence = [
    (1, 0, 0, 0),   # Coil 1 - orange
    (0, 0, 1, 0),   # Coil 2 - pink
    (0, 1, 0, 0),   # Coil 3 - yellow
    (0, 0, 0, 1)    # Coil 4 - blue
]
# since we want to do it in waves, we have to charge it one at a time to use it, moving one coil a little at a time

step_number = 0 #keep track of step number, will change thruought

#functions for LED
def led_off(): # led off = led off
    red.duty(0)
    blue.duty(0)
    green.duty(0)

#blue = waiting to start, can change timer mode
#green = timer is active
#red = timer ended, reseting
def set_blue(): #only blue is on, fully on
    red.duty(0)
    blue.duty(1023)
    green.duty(0)
#blue is on the whole time bc it serves as a waiting mode

def set_green(brightness): # have green be whatever brightness is set to
    red.duty(0)
    blue.duty(0)
    green.duty(brightness)
#green pulses bc it's "active"

def set_red(brightness): # have red be whatever brightness is set to
    red.duty(brightness)
    blue.duty(0)
    green.duty(0)
#red pulses to alert the user

#reset LED pulsing
def reset_pulse():
    global pulse_brightness
    global pulse_direction

    pulse_brightness = 0 #start with led turned off
    pulse_direction = 1 #1 means the brightness increases

#functions for stepper
def step_motor(direction): #direction 1 -> forward, -1 -> backward
    global step_number
    
    sequence = step_sequence[step_number] #get pattern from stepping sequence
    
    #pattern order, send it to four motor control pins
    IN1.value(sequence[0])
    IN2.value(sequence[1])
    IN3.value(sequence[2])
    IN4.value(sequence[3])

    #move to next step
    step_number += direction
    step_number = step_number % 4
    #%4 is a remainder of 4 and creates a repeating pattern of 0 1 2 3 0 1 2 3
    
#turns off all coils
def motor_off():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


#timer stuff
presets = [ #options for timers
    #these were tester values, 15-30 seconds
#     15,
#     20,
#     25,
#     30
    15 * 60,    # 15 minutes
    20 * 60,    # 20 minutes
    25 * 60,    # 25 minutes
    30 * 60     # 30 minutes
]

full_rev = 30 * 60 #time to get a full turn, * 60 for mins

#keeping track of which timer is active, 0 - 15, 1 - 20, 2 - 25, 3 - 30
preset_number = 0
selected_time = presets[preset_number]
remaining_time = selected_time #time left on timer

#running = running, timer is counting
# finished = timer ended
#returning = timer is moving back to orig position
running = False
finished = False
returning = False

#functions for clockhand
steps_taken = 0
last_step_time = time.ticks_ms() # stores last time motor moved
start_time = time.ticks_ms() # stores when timer started
last_return_step_time = time.ticks_ms() # lat time motor was moved while returning

def get_step_interval():
    # Time for one complete revolution divided by number of steps
    return (full_rev * 1000) / STEPS_PER_REVOLUTION

def get_target_steps(): #calcs motor steps to time
    return int((selected_time / full_rev) * STEPS_PER_REVOLUTION)


#button setup
last_butt1 = 1
last_butt2 = 1
last_butt_time = time.ticks_ms() #debounces basically
BUTT_DELAY = 200 # min time b/w presses

#led pulsing
pulse_brightness = 0
pulse_direction = 1

last_pulse_time = time.ticks_ms() #stores last time led brightness changed

def update_pulse(color): #led slowly brightens and dims

    global pulse_brightness
    global pulse_direction
    global last_pulse_time

    current_time = time.ticks_ms()

    #change brightness every 5 ms
    if time.ticks_diff(current_time, last_pulse_time) >= 5:

        last_pulse_time = current_time
        
        #incr or decr brightness
        pulse_brightness += pulse_direction * 10
        
        #if max brightness, go dimmer
        if pulse_brightness >= 1023:
            pulse_brightness = 1023
            pulse_direction = -1
        #if min brightness, go brighter
        if pulse_brightness <= 0:
            pulse_brightness = 0
            pulse_direction = 1
        #sets green @ brightness level
        if color == "green":
            set_green(pulse_brightness)
        #sets red
        elif color == "red":
            set_red(pulse_brightness)

#timer

def reset_timer():

    global remaining_time
    global running
    global finished
    global returning
    global steps_taken
    global step_number
    global last_step_time
    global start_time
    global last_return_step_time
    
    #put remaining time back to selected time option
    remaining_time = selected_time
    
    #stop timer since we are resetting it
    running = False
    finished = False

    #if motor moved, move it back to starting position
    if steps_taken > 0:
        returning = True
        last_return_step_time = time.ticks_ms() # when return movement started

        #resetting LED
        set_red(1023)

    else: #at start, dont move it
        returning = False
        step_number = 0
        motor_off()

        #waiting LED
        set_blue()

    #reset LED pulse
    reset_pulse()

    last_step_time = time.ticks_ms()
    start_time = time.ticks_ms()

#init

set_blue() #blue is on when turned on
reset_pulse()
motor_off()

#actual program

while True:

    current_time = time.ticks_ms()

    #button 1: cycle thru options
    butt1_state = butt1.value()
    if butt1_state == 0 and last_butt1 == 1: #debouncing more

        #only can change if preset mode is active
        if not running and not finished and not returning:
            preset_number += 1 # move to next preset option
            if preset_number >= len(presets): # cycle back to first preset when preset list is exhausted
                preset_number = 0
            selected_time = presets[preset_number] #get new selected time
            remaining_time = selected_time #reset remaining time to new option in case it held old one
            finished = False
            print( #print to thonny just in case
                "Timer:",
                selected_time //60, #divide to get minutes
                "minutes"
            )
            set_blue()

    last_butt1 = butt1_state # remember current state

    #button 2: start/reset
    butt2_state = butt2.value()
    if butt2_state == 0 and last_butt2 == 1:

        #debouncing
        if time.ticks_diff(current_time, last_butt_time) > BUTT_DELAY:
            last_butt_time = current_time

            #if timer is running OR finished, reset
            if running or finished or returning:
                reset_timer()
                print("Timer reset")

            #otherwise start timer
            else:
                running = True
                finished = False
                returning = False

                #reset green LED pulse
                reset_pulse()
                last_step_time = current_time
                start_time = current_time
                print("Timer started") #for testing tbh

    last_butt2 = butt2_state

    #if timer running
    if running:

        #pulse green led
        update_pulse("green")

        #move hand
        elapsed_seconds = time.ticks_diff(current_time, start_time) / 1000

        #calculate how many steps the hand should have taken by now
        target_steps = int((elapsed_seconds / full_rev) * STEPS_PER_REVOLUTION)

        if steps_taken < target_steps: #if not at correct step, move it forward
            step_motor(1)
            steps_taken += 1

        #check remaining time
        remaining_time = selected_time - elapsed_seconds

        #timer finished
        if elapsed_seconds >= selected_time: #reseting !
            remaining_time = 0
            running = False
            finished = True
            returning = True

            #reset red LED pulse
            reset_pulse()
            set_red(1023)
            last_return_step_time = current_time
            print("TIMER FINISHED!")

    #timer finished
    elif finished:

        #pulse red LED
        update_pulse("red")

        #return hand to starting position
        if returning:

            if steps_taken > 0: #if not back at starting position
                
                #moving it back !!!
                if time.ticks_diff(current_time, last_return_step_time) >= 1: #smaller number = faster
                    last_return_step_time = current_time
                    step_motor(-1) # move 1 step back
                    steps_taken -= 1 #count that ^

            else: #made it to start
                returning = False
                step_number = 0
                motor_off()

                #waiting LED
                set_blue()

    #waiting for timer
    else:

        #blue LED only when NOT resetting
        if not returning:
            set_blue()

        #return hand to starting position
        if returning:

            if steps_taken > 0: #checking for steps leftover
                
                
                #move motor backward quickly
                if time.ticks_diff(current_time, last_return_step_time) >= 1:
                    last_return_step_time = current_time
                    step_motor(-1)
                    steps_taken -= 1

            else:
                returning = False
                step_number = 0
                motor_off()

                #waiting LED
                set_blue()

    #lil delay
    time.sleep_ms(5)