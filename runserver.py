from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from nanpy import Arduino
from nanpy import serial_manager
#from flask.ext.login import login_user, logout_user, current_user, login_required
from time import sleep
from datetime import datetime
import datetime as dt
from decorators import async
"""
direction pin for motor B is Digital 12. Speed pin for motor B is Digital 9 (PWM)
Diretion pin for motor A is Digital 13. Speed pin or motor A is Digital 10 (PWM)
YG GY

"""
serial_manager.connect('/dev/ttyACM0')
app = Flask(__name__)


DIR_B_PIN = 12 # direction pin b
SPEED_B_PIN = 9 # speed pin b
DIR_A_PIN = 13 # direction pin a
SPEED_A_PIN = 10 # speed pin a

LED_PIN_R = 3
LED_PIN_G = 5
LED_PIN_B = 6

@app.route('/led_test/<r>/<g>/<b>')
def led_test(r, g, b):
    r_val, g_val, b_val = int(r), int(g), int(b)
    Arduino.analogWrite(LED_PIN_R, r_val)
    Arduino.analogWrite(LED_PIN_G, g_val)
    Arduino.analogWrite(LED_PIN_B, b_val)
    return "r:%s, g:%s, b:%s" %(r_val, g_val, b_val)


@async
def go_forward():
    print "executing go_forward"
    speed = 255
    direction = 0
    Arduino.digitalWrite(DIR_B_PIN, direction)
    Arduino.analogWrite(SPEED_B_PIN, speed)
    Arduino.digitalWrite(DIR_A_PIN, direction)
    Arduino.analogWrite(SPEED_A_PIN, speed)
    Arduino.analogWrite(LED_PIN_G, 155)

@async
def go_backward():
    print "executing go_backward"
    speed = 255
    direction = 1
    Arduino.digitalWrite(DIR_B_PIN, direction)
    Arduino.analogWrite(SPEED_B_PIN, speed)
    Arduino.digitalWrite(DIR_A_PIN, direction)
    Arduino.analogWrite(SPEED_A_PIN, speed)
    Arduino.analogWrite(LED_PIN_R, 155)
    Arduino.analogWrite(LED_PIN_G, 155)
    Arduino.analogWrite(LED_PIN_B, 155)

@async
def go_left():
    print "executing go_left"
    speed = 255
    direction_a = 0
    direction_b = 1
    Arduino.digitalWrite(DIR_B_PIN, direction_b)
    Arduino.analogWrite(SPEED_B_PIN, speed)
    Arduino.digitalWrite(DIR_A_PIN, direction_a)
    Arduino.analogWrite(SPEED_A_PIN, speed)
    Arduino.analogWrite(LED_PIN_R, 0)
    Arduino.analogWrite(LED_PIN_G, 0)
    Arduino.analogWrite(LED_PIN_B, 155)

@async
def go_right():
    print "executing go_right"
    speed = 255
    direction_a = 1
    direction_b = 0
    Arduino.digitalWrite(DIR_B_PIN, direction_b)
    Arduino.analogWrite(SPEED_B_PIN, speed)
    Arduino.digitalWrite(DIR_A_PIN, direction_a)
    Arduino.analogWrite(SPEED_A_PIN, speed)
    Arduino.analogWrite(LED_PIN_R, 0)
    Arduino.analogWrite(LED_PIN_G, 0)
    Arduino.analogWrite(LED_PIN_B, 155)

@async
def stop():
    print "EXECUTING STOP"
    Arduino.analogWrite(SPEED_B_PIN, 0)
    Arduino.analogWrite(SPEED_A_PIN, 0)
    Arduino.analogWrite(LED_PIN_R, 200)
    Arduino.analogWrite(LED_PIN_G, 0)
    Arduino.analogWrite(LED_PIN_B, 0)

@async
def flash_yellows(STOP):
    while True:
        Arduino.analogWrite(LED_PIN_R, 155)
        Arduino.analogWrite(LED_PIN_G, 155)
        Arduino.analogWrite(LED_PIN_B, 0)
        sleep(0.5)

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/echo/', methods=['GET', 'POST'])
def control_car():
    if request.method == "POST":
        asdf = request.json['asdf']
        print asdf
        if asdf == "forward":
            go_forward()
        if asdf == "stop_forward":
            stop()
        if asdf == "backward":
            go_backward()
        if asdf == "stop_backward":
            stop()
        if asdf == "go_left":
            go_left()
        if asdf == "stop_left":
            stop()
        if asdf == "go_right":
           go_right()
        if asdf == "stop_right":
            stop()
        if asdf == "stop":
            stop()

        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
