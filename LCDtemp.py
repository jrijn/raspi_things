#!/usr/bin/python
import os
import glob
from time import sleep, strftime, time
import Adafruit_CharLCD as LCD
import signal

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = '/sys/bus/w1/devices/28-000008c71ecb'
device_file = device_folder + '/w1_slave'

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
                           
lcd.set_backlight(1)

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
        
def initiate_lcd():
    lcd.set_backlight(1)
    lcd.message("Temp: ")
    lcd.cursor_pos = (0,0)

def main():
    temp = read_temp()
    lcd.clear()
    lcd.message("Temp: %d C" % temp)
   
    
# def keyboardInterruptHandler(signal, frame):
    # lcd.clear()
    # lcd.message("Quitting...")
    # sleep(2)
    # lcd.clear()
    # lcd.set_backlight(0)
    
    # exit(0)

# signal.signal(signal.SIGINT, keyboardInterruptHandler)

try:
    initiate_lcd()
    while True:
        main()
        sleep(0.1)
 
except KeyboardInterrupt:
    lcd.clear()
    lcd.message("Interrupted")
    sleep(2)
    lcd.clear()
    lcd.set_backlight(0)
    
# Print a two line message
# lcd.clear()
# lcd.message('Hej hej\nCleo!')

# Wait 5 seconds
# time.sleep(5.0)

# Demo showing the cursor.
# lcd.clear()
# lcd.show_cursor(True)
# lcd.message('Show cursor')

# time.sleep(5.0)

# Demo showing the blinking cursor.
# lcd.clear()
# lcd.blink(True)
# lcd.message('Blink cursor')

# time.sleep(5.0)

# Stop blinking and showing cursor.
# lcd.show_cursor(False)
# lcd.blink(False)

# Demo scrolling message right/left.
# lcd.clear()
# message = 'Mag ik nog een half koekje...?'
# lcd.message(message)
# for i in range(lcd_columns-len(message)):
    # time.sleep(0.5)
    # lcd.move_right()
# for i in range(lcd_columns-len(message)):
    # time.sleep(0.5)
    # lcd.move_left()

# Demo turning backlight off and on.
# lcd.clear()
# lcd.message('Flash backlight\nin 5 seconds...')
# time.sleep(5.0)
# Turn backlight off.
# lcd.set_backlight(0)
# time.sleep(2.0)
# Change message.
# lcd.clear()
# lcd.message('Goodbye!')
# Turn backlight on.
# lcd.set_backlight(1)
