from machine import Pin

motion_sensor = Pin(18, Pin.IN)

def read_motion():
    motion = motion_sensor.value() == 1
    motion_data = {"motion": motion}
    print(motion_data)

    return motion_data
