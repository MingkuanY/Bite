from picamera import PiCamera
from time import sleep
import requests
from PIL import Image
import time
import RPi.GPIO as GPIO
import smbus
from time import sleep
import numpy as np

# Define MPU6050 registers and their addresses
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, False)

def MPU_Init():
    # Initialize MPU6050
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def beep(repeat):
   for i in range(0, repeat):
      for pulse in range(60): # square wave loop
         GPIO.output(15, True)
         time.sleep(0.005)     # high for .001 sec
         GPIO.output(15, False)      
         time.sleep(0.005)     # low for .001 sec
      time.sleep(0.02)        # add a pause between each cycle


def read_raw_data(addr):
    # Read 16-bit raw data from the MPU6050
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    # Concatenate higher and lower value and convert to signed value
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# Initialize I2C bus and MPU6050 device address
bus = smbus.SMBus(1)  # Use bus 1, you can also use bus 0 for older boards
Device_Address = 0x68  # MPU6050 device address

# Initialize MPU6050
MPU_Init()

print("Reading Data of Gyroscope and Accelerometer")

# Initialize a fixed-size buffer for raw acceleration data
max_buffer_size = 25  # Adjust this as needed
raw_accel_data = []

# Initialize moving average filters for 'A' data
ma_filter_25 = []
ma_filter_5 = []

last_print_time = None
current_time = 0  # Initialize current_time to zero

img = 'images_test/image.jpg'
api_user_token = '6705bb3b9162a8b1826bbdce19d5d52fad669bf0'
headers = {'Authorization': 'Bearer ' + api_user_token}


camera = PiCamera()
trigger = False
prev_trigger = False


while True:
    trigger = True

    # Read sensor data
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    # Calculate accelerometer values
    Ax = acc_x / 16384.0 / 0.935
    Ay = acc_y / 16384.0 / 0.935
    Az = acc_z / 16384.0 / 0.935
    A = (Ax**2 + Ay**2 + Az**2)**0.5

    # Append raw 'A' data to the buffer and limit its size
    raw_accel_data.append(A)
    if len(raw_accel_data) > max_buffer_size:
        raw_accel_data.pop(0)  # Remove the oldest data point

    big_filter_size = 6
    small_filter_size = 3

    # Apply the moving average filter (25)
    ma_filter_25.append(np.mean(raw_accel_data[-big_filter_size:]))

    # Apply the moving average filter (5)
    if len(raw_accel_data) >= 5:
        ma_filter_5.append(np.mean(raw_accel_data[-small_filter_size:]))
    else:
        ma_filter_5.append(0)  # Set to 0 if there are not enough data points

    diff = ma_filter_25[-1] - ma_filter_5[-1]
    
    # Check if the MPU is upright with a maximum error of 5 degrees in every axis
    # 
    MPU_IS_UPRIGHT = False

    if (abs(Ax) <= 0.2 and abs(Ay) <= 0.2 and abs(Az - 1) <= 0.2):
        if MPU_IS_UPRIGHT is False:
            print("MPU IS UPRIGHT")
            MPU_IS_UPRIGHT = True
            trigger = True
			
        if (abs(diff) >= 0.09 and current_time == 0):
            current_time = time.time()
        elif (abs(diff) >= 0.09 and time.time() - current_time < 2):
            last_print_time = time.time()
        else:
            current_time = 0

    sleep(0.04)  # Sleep for a short interval before the next reading

    if trigger and not prev_trigger:
        beep(1)
        camera.capture('images_test/image.jpg')
        input_image_path = "images_test/image.jpg"
        output_image_path = "images_test/image.jpg"
        image = Image.open(input_image_path)
        # Rotate the image (for example, rotating 90 degrees)
        angle = 270  # Change this angle to your desired rotation angle
        rotated_image = image.rotate(angle)

        # Reduce the resolution by 50 percent
        width, height = rotated_image.size
        new_width = int(width * 0.5)
        new_height = int(height * 0.5)
        resized_image = rotated_image.resize((new_width, new_height))

        # Save the modified image
        resized_image.save(output_image_path)

        # Close the images
        image.close()
        rotated_image.close()
        resized_image.close()

        
        sleep(1)
        # Single/Several Dishes Detection
        url = 'https://api.logmeal.es/v2/image/segmentation/complete'
        resp = requests.post(url,files={'image': open(img, 'rb')},headers=headers)

        print(resp.status_code)
        print(resp.json()['imageId'])

        # Nutritional information
        url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
        resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)
        print(resp.json()) # display nutritional info
    

    prev_trigger = trigger



