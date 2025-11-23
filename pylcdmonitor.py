from board import SCL, SDA
import busio
import adafruit_ssd1306
import time
import socket

from gpiozero import Button, CPUTemperature, LoadAverage, DiskUsage
import gpiozero.pins.lgpio
import lgpio

def __patched_init(self, chip=None):
    gpiozero.pins.lgpio.LGPIOFactory.__bases__[0].__init__(self)
    chip = 0
    self._handle = lgpio.gpiochip_open(chip)
    self._chip = chip
    self.pin_class = gpiozero.pins.lgpio.LGPIOPin

gpiozero.pins.lgpio.LGPIOFactory.__init__ = __patched_init


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

btn = Button(17)

cpuTemp = CPUTemperature()
load_avg_1 = LoadAverage(minutes=1)
load_avg_5 = LoadAverage(minutes=5)
load_avg_15 = LoadAverage(minutes=15)

while True:
    btn.wait_for_press()
    print("Button pressed")
    display.poweron()
    current = start_time = time.time()
    end_time = start_time + 30
    counter = 1
    IPAddr = get_ip()
    while current <= end_time:
        display.fill(0)
        display.text("CPU Temp :%.1f" % (cpuTemp.temperature), 0, 0, 1)
        display.text("Load : %2.0f %2.0f %2.0f" % (100 * load_avg_1.value, 100 * load_avg_5.value, 100 * load_avg_15.value), 0, 10, 1)
        display.text("IP :%s" % (IPAddr), 0, 20, 1)
        display.show()
        time.sleep(0.5)
        counter = counter + 1
        current = time.time()
    display.poweroff() 
    time.sleep(2)

