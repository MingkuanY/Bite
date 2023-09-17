import smbus
from time import sleep, time
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

# Function to initialize MPU6050
def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

# Function to read 16-bit raw data from the MPU6050
def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# Initialize I2C bus and MPU6050 device address
bus = smbus.SMBus(1)  # Use bus 1; change to 0 for older boards
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

# Initialize state variables
state = 0
timestamp = 0

# Initialize variables for calculating the average derivative
derivative_buffer = []

# Define the threshold variable for average derivative
threshold_avg_derivative = 0.06  # Change this threshold as needed

while True:
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

    # Calculate the derivative of acceleration and add it to the buffer
    if len(raw_accel_data) > 1:
        acceleration_derivative = A - raw_accel_data[-2]
        derivative_buffer.append(acceleration_derivative)
    
    # Keep the derivative buffer length to 10 samples
    if len(derivative_buffer) > 10:
        derivative_buffer.pop(0)
        # Calculate the average derivative over the last 10 samples
        avg_derivative = np.mean(derivative_buffer)

    if len(derivative_buffer) == 10:
        # State Machine
        if state == 0:  # Waiting for hand to be still and perpendicular
            if (abs(Ax) - 1 <= 0.2 and abs(Ay) <= 0.2 and abs(Az) <= 0.2 and avg_derivative < threshold_avg_derivative):
                if timestamp == 0:
                    print("STATE 0.1")
                    timestamp = time()
                elif time() - timestamp > 1 and avg_derivative < threshold_avg_derivative:
                    print("STATE 0.2")
                    state = 1
                    timestamp = time()
                else:
                    print("STATE 0.3")
                    timestamp = 0
            else:
                print("STATE 0.4")
                timestamp = 0
                print(Ax, Ay, Az)
        elif state == 1:  # Hand is still and perpendicular, waiting to be turned 90 degrees flat
            print("STATE 1.0")
            if (time() - timestamp < 2 and abs(Ax) <= 0.2 and abs(Ay) <= 0.2 and abs(Az) - 1 <= 0.2 and avg_derivative < threshold_avg_derivative):
                print("STATE 1.1")
                state = 2
            else:
                print("STATE 1.2")
                state = 0
                timestamp = 0
        elif state == 2:
            print("STATE 2: Taking a photo!")
            # Add your code here to trigger the photo capture
            sleep(1)  # Sleep for 1 second
            state = 0

        sleep(0.04)  # Sleep for a short interval before the next reading
