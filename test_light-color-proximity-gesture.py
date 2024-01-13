# This program is for basic testing of the features of the
# APDS-9960 light/color/proximity/gesture sensor, and
# most of the code comes from the adafruit_apds9960 docs.

import board
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import time

i2c = board.I2C()
apds = APDS9960(i2c)


### Proximity ###
# apds.enable_proximity = True

# while True:
#    print(apds.proximity)


### Light & Color ###
apds.enable_color = True

# APDS9960.color_gain = 3; # min 0, max 3
# APDS9960.color_integration_time = 256; # min 1, max 256

while True:
    while not apds.color_data_ready:
        time.sleep(0.005)
    r,g,b,c = apds.color_data
    print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r,g,b,c))
    temp = colorutility.calculate_color_temperature(r,g,b)
    print('Color temp: {0}'.format(temp))
    lux = colorutility.calculate_lux(r,g,b)
    print('Lux: {0}'.format(lux))


### Gestures ###
# apds.enable_proximity = True
# apds.enable_gesture = True

# while True:
#    gesture = apds.gesture()
#    if gesture == 1:
#        print("up")
#    if gesture == 2:
#        print("down")
#    if gesture == 3:
#        print("left")
#    if gesture == 4:
#        print("right")
