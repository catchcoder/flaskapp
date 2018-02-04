"""
Raspberry Pi, outputs controlled by web interface (python,flask)
"""

from flask import Flask, render_template, request, redirect
import time
import os
import sqlite3
from RPi import GPIO

app = Flask('__name__')
db_location = 'data.sqlite3'
db_table = 'GPIO_Outputs'
conn = sqlite3.connect(db_location)
cur = conn.cursor()

sql = ' create table if not exists {} (id integer)'.format(db_table)
cur.execute(sql)
conn.commit()

# try:
# Try and import GPIO for Raspberry Pi,
# If it fails import fake GPIO for CI.
#     import RPi.GPIO as GPIO
# except ImportError:
# Import fake GPIO https://pypi.python.org/pypi/fakeRPiGPIO/0.2a0.


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, False)


def check_led_state(pin):
    """
    Checks and returns LED output state
    """
    return GPIO.output(pin)


@app.route('/')
def index():
    return render_template('index.html', led_state=check_led_state(17))


@app.route('/ledon')
def ledon():
    GPIO.output(17, True)
    return render_template('index.html', led_state=check_led_state(17))


@app.route('/ledoff')
def ledoff():
    GPIO.output(17, False)
    return render_template('index.html', led_state=check_led_state(17))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
