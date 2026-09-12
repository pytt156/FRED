from machine import ADC, Pin

light_sensor = ADC(Pin(26))

def read_light():
    light = light_sensor.read_u16()
    light_data = {"light": light}
    print(light_data)

    return light_data