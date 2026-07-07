import machine
import network
import espnow
import time

joy1_x_pin = machine.ADC(machine.Pin(32))
joy1_y_pin = machine.ADC(machine.Pin(33))
joy2_x_pin = machine.ADC(machine.Pin(34))
joy2_y_pin = machine.ADC(machine.Pin(35))

for pin in [joy1_x_pin, joy1_y_pin, joy2_x_pin, joy2_y_pin]:
    pin.atten(machine.ADC.ATTN_11DB)
    pin.width(machine.ADC.WIDTH_12BIT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

# find the mac address of the other esp32 and put it here
PEER_MAC = b'\xaa\xff\xaa\xff\xaa\xff' 
esp.add_peer(PEER_MAC)

print("Ground Station Ready.")

while True:
    j1_x = joy1_x_pin.read()
    j1_y = joy1_y_pin.read()
    j2_x = joy2_x_pin.read()
    j2_y = joy2_y_pin.read()
    
    data_packet = f"{j1_x},{j1_y},{j2_x},{j2_y}"
    
    try:
        esp.send(PEER_MAC, data_packet.encode('utf-8'))
    except Exception as e:
        print("Transmission error", e)
        
    time.sleep_ms(20) # send updates at 50 hertz frequency