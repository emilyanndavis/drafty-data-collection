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
1. Ensure you have all the prerequisite hardware, software, and configuration listed in [Setup](#setup).
2. Connect the sensor(s) according to their official documentation.
3. Set up your data files. You have a couple of options:
    - Create two empty files: `most-recent.csv` and `all.csv`. Where you store them is up to you.
    - Alternatively: for the complete Drafty experience including the Jekyll-based website, fork and clone the [drafty repo](https://github.com/emilyanndavis/drafty). Find `most-recent.csv` and `all.csv` in the `_data` directory, and clear the contents of both files.
4. In `main.py`, find all the references to `most-recent.csv` and `all.csv`, and make sure the relative paths point to the correct locations based on where your CSV files are stored. Update the paths if needed.
5. If you plan to use the [Drafty companion website](https://github.com/emilyanndavis/drafty), and/or if you want to back up your data in a remote git repo: configure a method to automate authentication to your git repo. There are many ways to accomplish this. Here are just a couple of options:
    - Use [PyGithub](https://pypi.org/project/PyGithub/) to connect to the GitHub API with a personal access token. (Be sure to store your token in a separate file, and add that file to your `.gitignore` to avoid publicly sharing your token by mistake!)
    - Alternatively, load a shell script on your Raspberry Pi that adds your SSH key to the ssh-agent, as in this example in the GitHub docs: [Auto-launching ssh-agent on Git for Windows](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/working-with-ssh-key-passphrases?platform=windows#auto-launching-ssh-agent-on-git-for-windows). (Even though these instructions are for Windows, they will also work on Linux.)

    There are certainly other solutions as well. Choose whichever method best suits your needs!

6. Alternatively, if you _do not_ plan to use the Drafty companion website, _do not_ want to back up your data in a remote git repo, and/or just want to skip this part for now: locate the line in `main.py` that contains `git commit` and `git push` commands, and remove it or comment it out.
7. In `main.py`, locate the line that includes `sudo shutdown -P`. This line schedules a shutdown of the Raspberry Pi at the end of the specified duration. This is helpful if you are running your Pi on battery power and want to be sure it is safely shut down before you unplug it to recharge the battery. If you do not need this feature, remove or comment out that line of code.
8. In `main.py`, locate the lines that initialize `DURATION_HOURS` and `INTERVAL_MINUTES`. Customize either or both of these values if desired.
9. Install dependencies in the project directory with `pipenv install`.
10. Run `pipenv run python3 main.py`. To ensure the program continues to run in the event of lost connection/network timeout (e.g., if you are running the program from a remote terminal via ssh), include `nohup`, like this: `pipenv run nohup python3 main.py`.
11. If you are using the Drafty companion website, follow the instructions in the drafty README, under [Setting up your Drafty website](https://github.com/emilyanndavis/drafty#setting-up-your-drafty-website).
