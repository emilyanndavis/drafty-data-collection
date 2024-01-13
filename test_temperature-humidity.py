# This program is for basic testing of the features of the
# AHT-20 light/color/proximity/gesture sensor, and
# most of the code comes from the adafruit_ahtx0 docs.

import time
import board
import adafruit_ahtx0

i2c = board.I2C()
aht20 = adafruit_ahtx0.AHTx0(i2c)

def c_to_f(c):
    return c * 9 / 5 + 32

while True:
    print("Temperature: %0.1f C" % aht20.temperature)
    print("Temperature: %0.1f F" % c_to_f(aht20.temperature))
    print("Humidity: %0.1f %%" % aht20.relative_humidity)
    print('\n')
    time.sleep(2)