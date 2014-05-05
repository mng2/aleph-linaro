# read Atmel AT30TSE004A temp through I2C
# read Zynq XADC temp through IIO driver (XAPP1172, UG480)

import time
from smbus import SMBus

bus = SMBus(0)

while(1):
	atmelraw = bus.read_i2c_block_data(0x1e,0x05,2)
	
	f = open('/sys/bus/iio/devices/iio:device0/in_temp0_raw','r')
	zynqraw = f.read()
	f.close()
	
	atmeltemp = 16.0*(atmelraw[0] & 0xf) + (atmelraw[1] & 0xfe)/16.0
	
	zynqtemp = int(zynqraw)*503.975/4096 - 273.15
	
	print "Atmel temp: ", atmeltemp
	print "Zynq temp: ", zynqtemp
	time.sleep(5)


