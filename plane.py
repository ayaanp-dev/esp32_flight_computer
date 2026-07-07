import machine
import network
import espnow
import time
from bno055 import BNO055
from bmp280 import BMP280

i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
imu = BNO055(i2c)
baro = BMP280(i2c)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)


def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    host, msg = esp.recv(10) # 10ms timeout
    if msg:
        try:
            data = msg.decode('utf-8').split(',')
            joy1_x = int(data[0])
            joy1_y = int(data[1])
            joy2_x = int(data[2])
            joy2_y = int(data[3])
            
            print(f"Control Input - Joystick 1 | X: {joy1_x}, Y: {joy1_y}")
            print(f"Control Input - Joystick 2 | X: {joy2_x}, Y: {joy2_y}")
        except Exception as e:
            pass

    try:
        heading, roll, pitch = imu.euler()
    
        # BNO055 Vector Data (Acceleration, Linear Acceleration, Gravity)
        accel = imu.accelerometer()
        lin_accel = imu.linear_acceleration()
        gravity = imu.gravity()
        
        # BMP280 Environmental Data
        temp_c = baro.temperature
        pressure_hpa = baro.pressure
        
        # Output to Serial/REPL
        print("--- BNO055 IMU Data ---")
        print(f"Euler Angles (H/R/P): {heading}° | {roll}° | {pitch}°")
        print(f"Acceleration (X/Y/Z): {accel[0]} | {accel[1]} | {accel[2]} m/s²")
        print(f"Linear Acceleration (X/Y/Z): {lin_accel[0]} | {lin_accel[1]} | {lin_accel[2]} m/s²")
        print(f"Gravity (X/Y/Z): {gravity[0]} | {gravity[1]} | {gravity[2]} m/s²")
        
        print("\n--- BMP280 Environmental Data ---")
        print(f"Temperature: {temp_c:.2f} °C")
        print(f"Pressure: {pressure_hpa:.2f} hPa")
        print("----------------------------------\n")
        
    except Exception as e:
        print("Sensor error:", e)
        
    time.sleep_ms(20) # 50 hertz frequency control loop