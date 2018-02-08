#!/usr/bin/python
"""
Raspberry Pi, outputs controlled by web interface (python,flask)
Info for sysfs: https://www.kernel.org/doc/Documentation/gpio/sysfs.txt
https://elinux.org/RPi_Low-level_peripherals
"""

from flask import Flask, render_template, request, redirect, url_for
import time
import os
from datetime import datetime
# import sqlite3
from RPi import GPIO

app = Flask('__name__')
# db_location = 'data.sqlite3'
# db_table = 'GPIO_Outputs'
# conn = sqlite3.connect(db_location)
# cur = conn.cursor()

# sql = ' create table if not exists {} (id integer)'.format(db_table)
# cur.execute(sql)
# conn.commit()

# try:
# Try and import GPIO for Raspberry Pi,
# If it fails import fake GPIO for CI.
#     import RPi.GPIO as GPIO
# except ImportError:
# Import fake GPIO https://pypi.python.org/pypi/fakeRPiGPIO/0.2a0.


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO_PINS = [17, 27, 22, 10, 9, 11, 5, 6, 13]
gpio_pin_state = {}


def setup_outputs():
    """ Setup GPIOs for outputs.
    """
    for pin in GPIO_PINS:
        GPIO.setup(pin, GPIO.OUT)


setup_outputs()

GPIO.setup(2, GPIO.OUT)
GPIO.output(2, False)

gpio_path = "/sys/class/gpio/gpio{}/value"
# gpio_path = "/home/chris/repos/flaskapp/value"


def check_gpio_state(pin):
    """ Checks and returns output state
    """
    try:
        with open(gpio_path.format(pin)) as gpiopin:
            status = gpiopin.read(1)
    except Exception:
        status = 0

    return True if status == "1" else False


def check_all_gpios():
    """
    """
    global gpio_pin_state
    gpio_pin_state = {}

    for pin in GPIO_PINS:
        gpio_pin_state[pin] = check_gpio_state(pin)


def allonoroff(state):
    """
    """
    for pin in GPIO_PINS:
        GPIO.output(pin, state)


def swap_states():
    """
    """
    for pin in GPIO_PINS:
        GPIO.output(pin, not check_gpio_state(pin))


@app.route('/')
def index():
    # led_state = GPIO.output(17)
    check_all_gpios()
    return render_template('index.html', gpio_pin_state=gpio_pin_state)


@app.route('/gpioon/<int:gpio_pin>')
def gpioon(gpio_pin):
    GPIO.output(gpio_pin, True)
    return redirect(url_for('index'))


@app.route('/gpiooff/<int:gpio_pin>')
def gpiooff(gpio_pin):
    GPIO.output(gpio_pin, False)
    return redirect(url_for('index'))


@app.route('/switch')
def switch():
    swap_states()
    return redirect(url_for('index'))


@app.route('/all/<state>')
def all(state):
    if state == "off":
        allonoroff(False)
    else:
        allonoroff(True)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
