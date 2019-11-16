import os
import glob
from time import sleep, strftime, time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = '/sys/bus/w1/devices/28-000008c71ecb'
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000
		return temp_c

with open("/home/pi/ds18b20_freezer.csv", "a") as log:
	temp = read_temp()
	log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))
