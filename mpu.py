import smbus
from time import sleep, time
import numpy as np

# Create a bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    omega = 0.5 * fs
    low = lowcut / omega
    high = highcut / omega
    b, a = butter_bandpass_coeffs(low, high, order)
    return b, a

def butter_bandpass_coeffs(low, high, order=5):
    nyquist = 0.5
    low_omega = 2.0 * nyquist * low
    high_omega = 2.0 * nyquist * high

    # Calculate the coefficients
    b = butter_bandpass_b_coeffs(low_omega, high_omega, order)
    a = butter_bandpass_a_coeffs(low_omega, high_omega, order)
    
    return b, a

def butter_bandpass_b_coeffs(low_omega, high_omega, order=5):
    b_coeffs = np.zeros(order + 1)
    b_coeffs[0] = high_omega - low_omega
    b_coeffs[1] = 0.0
    for j in range(2, order + 1):
        b_coeffs[j] = ((-1) ** (j - 1)) * (np.sin(j * high_omega) - np.sin(j * low_omega)) / j
    return b_coeffs

def butter_bandpass_a_coeffs(low_omega, high_omega, order=5):
    a_coeffs = np.zeros(order + 1)
    a_coeffs[0] = 1.0
    for j in range(1, order + 1):
        a_coeffs[j] = 0.0
    return a_coeffs

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = np.zeros_like(data)
    for i in range(len(data)):
        for j in range(min(i, order), -1, -1):
            y[i] += (b[j] * data[i - j]) - (a[j] * y[i - j])
    return y

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

def MPU_Init():
    # Initialize MPU6050
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

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

# Sampling frequency (adjust as needed)
fs = 25.0  # 25 samples per second

# Define bandpass filter parameters
lowcut = 1.0  # 1 Hz
highcut = 2.0  # 2 Hz
order = 6  # Filter order

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

    # Apply bandpass filter to 'A' data
    filtered_A = butter_bandpass_filter(np.array([A]), lowcut, highcut, fs, order=order)[0]

    # Check if the MPU is upright with a maximum error of 5 degrees in every axis
    if (abs(Ax) <= 0.5 and abs(Ay) <= 0.5 and abs(Az - 1) <= 0.5):
        print(filtered_A)

    sleep(1.0 / fs)  # Sleep for a short interval before the next reading