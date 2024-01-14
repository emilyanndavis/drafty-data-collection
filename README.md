# Drafty Data Collection

## What is Drafty?
Drafty attempts to answer the question: "Just how drafty is it in that drafty room of the house?" A Raspberry Pi is installed in a poorly insulated enclosed porch and periodically takes readings of the ambient temperature, humidity, and light levels. For comparison with outdoor conditions, local weather data is retrieved from the National Weather Service.

## Setup
### Hardware and physical materials
The following hardware is required:
- Raspberry Pi with a 40-pin GPIO header (code has been written & tested on a Raspberry Pi 4)
- [Adafruit AHT20 Temperature & Humidity Sensor](https://learn.adafruit.com/adafruit-aht20)
- [Adafruit APDS-9960 Light, Color, Proximity, and Gesture Sensor](https://learn.adafruit.com/adafruit-apds9960-breakout)

The following materials are recommended:
- STEMMA QT/Qwiic 4-pin cables (for connecting sensors without soldering)
- A breadboard and assorted jumper wires (for more flexible arrangements of components)

### Software
The following software is required:
- Raspberry Pi OS (the code may work on other Linux distributions, but it has been tested only on Raspberry Pi OS Bookworm)
- Python >= 3.7.0
- [pipenv](https://pypi.org/project/pipenv)

### Configuration
#### Raspberry Pi
Make sure I2C is enabled on your Raspberry Pi. You can find this setting in the raspi-config tool or via the desktop GUI under Preferences > Raspberry Pi Configuration > Interfaces.

#### Local Weather
Local weather data is retrieved from the [National Weather Service's API Web Service](https://www.weather.gov/documentation/services-web-api). You will need to configure a couple of details to ensure you get the data you want.
1. Create a file at the root of this project and name it `weather_config.py`.
2. Add the following lines to `weather_config.py`:
    ```
    station_id = ''
    user_agent = ''
    ```
3. Choose a station to request weather observations from, and set `station_id` to the station's four-character identifier. You can find your nearest NWS station on this [list of all NWS Observed Weather Stations](https://forecast.weather.gov/stations.php).
4. Choose a unique string to identify your application, and set `user_agent` to this value. Per the [NWS Weather API docs](https://www.weather.gov/documentation/services-web-api):
    ```
    A User Agent is required to identify your application. This string can be anything, and the more unique to your application the less likely it will be affected by a security event. If you include contact information (website or email), we can contact you if your string is associated to a security event. This will be replaced with an API key in the future.

    User-Agent: (myweatherapp.com, contact@myweatherapp.com)
    ```

## Running sensor tests
1. First, ensure you have all the prerequisite hardware, software, and configuration listed in [Setup](#setup).
2. Connect the sensor(s) according to their official documentation.
3. Install dependencies in the project directory with `pipenv install`.
4. To test temperature/humidity, run `pipenv run python3 test_temperature-humidity`.
5. To test light/color/proximity/gestures, first comment/uncomment sections of `test_light-color-proximity-gesture.py` as desired, then run `pipenv run python3 test_light-color-proximity-gesture.py`.

## Running main.py
**Warning 1: main.py schedules a shutdown of the machine it is running on. To avoid surprises, you may wish to comment out or remove that part of the code.**

**Warning 2: main.py automatically pushes data to a remote git repo. This will fail unless you (1) have set up your own repo, (2) have updated the code to point to the correct directory & files, and (3) have implemented a method of automating authentication to your repo.**

1. First, read the warnings at the top of this section!
2. Update the code according to your needs (e.g., skip system shutdown, update path/file names, modify time interval and/or duration, etc.).
3. Ensure you have all the prerequisite hardware, software, and configuration listed in [Setup](#setup).
4. Connect the sensor(s) according to their official documentation.
5. Install dependencies in the project directory with `pipenv install`.
6. Run `pipenv run python3 main.py`. To ensure the program continues to run in the event of lost connection/network timeout (e.g., if you are running the program from a remote terminal via ssh), include `nohup`, like this: `pipenv run nohup python3 main.py`.
