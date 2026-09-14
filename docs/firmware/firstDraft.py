from machine import Pin, PWM
import time

#used as guides:
#motor: https://randomnerdtutorials.com/esp32-stepper-motor-28byj-48-uln2003/
#pwm: https://linuxhint.com/pwm-esp32-micropython-thonny-ide/

#inputs
butt1 = Pin(5, Pin.IN, Pin.PULL_UP) #cycle thru 15 20 25 30
butt2 = Pin(6, Pin.IN, Pin.PULL_UP) #start/reset
#Pin.PULL_UP is bc there is no resistor attached

#leds
red = PWM(Pin(8)) #timer finished
blue = PWM(Pin(7)) #waiting
green = PWM(Pin(9)) #timer working

Frequency = 1000 #0 to 78125, website uses 5k

red.freq(Frequency)
blue.freq(Frequency)
green.freq(Frequency)

#motor configuration
STEPS_PER_REVOLUTION = 2048

#motor pins
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

step_number = 0

#functions for LED
def led_off():
    red.duty(0)
    blue.duty(0)
    green.duty(0)

def set_blue():
    red.duty(0)
    blue.duty(1023)
    green.duty(0)

def set_green(brightness):
    red.duty(0)
    blue.duty(0)
    green.duty(brightness)

def set_red(brightness):
    red.duty(brightness)
    blue.duty(0)
    green.duty(0)

#reset LED pulsing
def reset_pulse():
    global pulse_brightness
    global pulse_direction

    pulse_brightness = 0
    pulse_direction = 1

#functions for stepper
def step_motor(direction):
    global step_number

    sequence = step_sequence[step_number]

    IN1.value(sequence[0])
    IN2.value(sequence[1])
    IN3.value(sequence[2])
    IN4.value(sequence[3])

    step_number += direction
    step_number = step_number % 4

def motor_off():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


#timer stuff
presets = [
    15,
    20,
    25,
    30
#     15 * 60,    # 15 minutes
#     20 * 60,    # 20 minutes
#     25 * 60,    # 25 minutes
#     30 * 60     # 30 minutes
]

preset_number = 0
selected_time = presets[preset_number]
remaining_time = selected_time
running = False
finished = False
returning = False

#functions for clockhand
steps_taken = 0
last_step_time = time.ticks_ms()
start_time = time.ticks_ms()
last_return_step_time = time.ticks_ms()

def get_step_interval():
    # Time for one complete revolution divided by number of steps
    return (30 * 1000) / STEPS_PER_REVOLUTION

def get_target_steps():
    return int((selected_time / 30) * STEPS_PER_REVOLUTION)


#button setup
last_butt1 = 1
last_butt2 = 1
last_butt_time = time.ticks_ms()
BUTT_DELAY = 200

#led pulsing
pulse_brightness = 0
pulse_direction = 1

last_pulse_time = time.ticks_ms()

def update_pulse(color):

    global pulse_brightness
    global pulse_direction
    global last_pulse_time

    current_time = time.ticks_ms()

    #change brightness every 5 ms
    if time.ticks_diff(current_time, last_pulse_time) >= 5:

        last_pulse_time = current_time

        pulse_brightness += pulse_direction * 10

        if pulse_brightness >= 1023:
            pulse_brightness = 1023
            pulse_direction = -1

        if pulse_brightness <= 0:
            pulse_brightness = 0
            pulse_direction = 1

        if color == "green":
            set_green(pulse_brightness)

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

    remaining_time = selected_time
    running = False
    finished = False

    if steps_taken > 0:
        returning = True
        last_return_step_time = time.ticks_ms()
    else:
        returning = False
        step_number = 0
        motor_off()

    #reset LED pulse
    reset_pulse()

    #waiting LED
    set_blue()
    last_step_time = time.ticks_ms()
    start_time = time.ticks_ms()

#init

set_blue()
reset_pulse()
motor_off()

#actual program

while True:

    current_time = time.ticks_ms()

    #button 1: cycle thru options
    butt1_state = butt1.value()
    if butt1_state == 0 and last_butt1 == 1:

        #only can change if preset mode is active
        if not running and not finished and not returning:
            preset_number += 1
            if preset_number >= len(presets):
                preset_number = 0
            selected_time = presets[preset_number]
            remaining_time = selected_time
            finished = False
            print(
                "Timer:",
                selected_time,# // 60,
                "minutes"
            )
            set_blue()

    last_butt1 = butt1_state

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
                print("Timer started")

    last_butt2 = butt2_state

    #if timer running
    if running:

        #pulse green led
        update_pulse("green")

        #move hand
        target_steps = get_target_steps()
        step_interval = get_step_interval()

        if steps_taken < target_steps:
            if time.ticks_diff(current_time, last_step_time) >= step_interval:
                last_step_time = current_time
                step_motor(1)
                steps_taken += 1

        #check remaining time
        elapsed_seconds = time.ticks_diff(current_time, start_time) / 1000
        remaining_time = selected_time - elapsed_seconds

        #timer finished
        if elapsed_seconds >= selected_time:
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

            if steps_taken > 0:

                if time.ticks_diff(current_time, last_return_step_time) >= 1: #smaller number = faster
                    last_return_step_time = current_time
                    step_motor(-1)
                    steps_taken -= 1

            else:
                returning = False
                step_number = 0
                motor_off()

    #waiting for timer
    else:
        set_blue()

        #return hand to starting position
        if returning:

            if steps_taken > 0:

                if time.ticks_diff(current_time, last_return_step_time) >= 1:
                    last_return_step_time = current_time
                    step_motor(-1)
                    steps_taken -= 1

            else:
                returning = False
                step_number = 0
                motor_off()

    #lil delay
    time.sleep_ms(5)