from machine import Pin
from dht import DHT11

dht_sensor = DHT11(Pin(12))

def read_dht11():

    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()

    dht_data = {"temperature": temp, "humidity": humidity}
    print(dht_data)
    return dht_data

