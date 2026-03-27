from time import sleep_ms
from machine import Pin


def example1():
    led=Pin(25,Pin.OUT) #create LED object from pin2,Set Pin2 to output
    try:
        while True:
            led.value(0)        #Set led turn on
            sleep_ms(1000)
            led.value(1)        #Set led turn off
            sleep_ms(1000)
    except:
        pass

if __name__ == '__main__':
    example1()
