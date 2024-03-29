# Periodically collects environmental data and pushes updates to remote git repo
# Automatically shuts down the Pi after a set time period so the battery pack can be recharged

# Standard Python modules
from datetime import datetime
import io
import math
import subprocess
import time

# Sensor-specific modules
import adafruit_ahtx0
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import board

# Modules for local weather data
import requests
from weather_config import station_id, user_agent

# Define total duration (how long to run program before shutting down)
DURATION_HOURS = 12 
DURATION_MINUTES = DURATION_HOURS * 60
DURATION_SECONDS = DURATION_MINUTES * 60
START = time.time()
END = START + DURATION_SECONDS

# Define time interval (how frequently to collect & store data)
INTERVAL_MINUTES = 15
INTERVAL_SECONDS = INTERVAL_MINUTES * 60

# Schedule system shutdown
SHUTDOWN_DELAY = max(math.ceil(DURATION_MINUTES), math.ceil(DURATION_MINUTES/INTERVAL_MINUTES) * INTERVAL_MINUTES)
subprocess.run("sudo shutdown -P \"+{0}\"".format(SHUTDOWN_DELAY), shell=True)

# Initialize sensor-related objects & settings
i2c = board.I2C()
aht20 = adafruit_ahtx0.AHTx0(i2c)
apds = APDS9960(i2c)
apds.enable_color = True
APDS9960.color_gain = 0; # min 0, max 3, driver default 1
APDS9960.color_integration_time = 72; # min 1, max 256, driver default 256

# Utility function for converting Celsius to Fahrenheit
def c_to_f(c):
  if c:
    return c * 9 / 5 + 32
  return None

# Request local weather data from NWS API
def get_local_weather():
	weather_base_url = 'https://api.weather.gov'
	request_url = weather_base_url + "/stations/" + station_id + "/observations/latest"
	request_headers = {'user-agent': user_agent}
	try:
		response = requests.get(request_url, headers=request_headers, timeout=5)
		if (response.status_code != requests.codes.ok):
			print('HTTP Error: NWS API returned status code', response.status_code)
			return None
		try:
			response_json = response.json()
			return response_json
		except requests.exceptions.JSONDecodeError:
			print('JSON Decode Error')
			return None
	except requests.exceptions.RequestException as e:
		print('Request Error:', e)
		return None		

while time.time() < END:
	# Collect data
	next_run = time.time() + INTERVAL_SECONDS
	now = datetime.now()
	temp_c = aht20.temperature
	temp_f = c_to_f(temp_c)
	humidity = aht20.relative_humidity
	while not apds.color_data_ready:
		time.sleep(0.005)
	r,g,b,c = apds.color_data
	if (r <= 0 and g <= 0 and b <= 0):
		color_temp = 0
	else:	
		color_temp = colorutility.calculate_color_temperature(r,g,b)
	lux = colorutility.calculate_lux(r,g,b)

	# Fetch local weather data
	response_json = get_local_weather()
	# Parse weather data
	try:
		nws_conditions = response_json.get('properties').get('textDescription')
	except:
		nws_conditions = None
	try:
		nws_temp_c = response_json.get('properties').get('temperature').get('value')
		nws_temp_f = c_to_f(nws_temp_c)
	except:
		nws_temp_c = None
		nws_temp_f = None
	try:
		nws_humidity = response_json.get('properties').get('relativeHumidity').get('value')
	except:
		nws_humidity = None

	# Format data as CSV
	csv_row = '{0:%Y-%m-%d %H:%M:%S},{1:0.1f},{2:0.1f},{3:0.1f},{4:0.1f},{5:0.1f},{6},{7},{8},{9},'.format(now, temp_c, temp_f, humidity, lux, color_temp, r, g, b, c)
	for prop in [nws_temp_c, nws_temp_f, nws_humidity]:
		try:
			csv_row += '{0:0.1f},'.format(prop)
		except:
			# If value cannot be formatted as a float, leave the field empty
			csv_row += ','
	if nws_conditions:
		csv_row += '{0}'.format(nws_conditions)
	csv_row += '\n'
	
	# Update most recent data
	most_recent = open("../drafty/_data/most-recent.csv", "w", encoding="utf-8")
	most_recent.write("time,temp_c,temp_f,humidity,lux,color_temp,red,green,blue,clear,nws_temp_c,nws_temp_f,nws_humidity,nws_conditions\n")
	most_recent.write(csv_row)
	most_recent.close()
	
	# Add most recent data to running log
	all_data = open("../drafty/_data/all.csv", "a", encoding="utf-8")
	all_data.write(csv_row)
	all_data.close()
	
	# Push data to remote repo
	subprocess.run("cd ../drafty && git add _data/most-recent.csv && git add _data/all.csv && git commit -m \"Auto update {0}\" && git push".format(now), shell=True)

	# Sleep for the remainder of the pre-defined interval, or a minimum of 60 seconds
	time.sleep(max(next_run - time.time(), 60))
