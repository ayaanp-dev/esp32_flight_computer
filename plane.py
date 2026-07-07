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
        temp = baro.temperature
        press = baro.pressure
        
    except Exception as e:
        print("Sensor error:", e)
        
    time.sleep_ms(20) # 50 hertz frequency control loop