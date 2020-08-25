 
import time
import Adafruit_DHT as dht

while True:
    h,t = dht.read_retry(dht.DHT11,16)
    print('Humidity', h, '%', ', temperature', t, 'C')
    time.sleep(1) 