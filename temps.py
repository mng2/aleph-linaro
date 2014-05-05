# read Atmel AT30TSE004A temp through I2C

from smbus import SMBus
i2c = SMBus(0)
atmelraw = i2c.read_i2c_block_data(0x1e,0x05,2)
atmeltemp = 16.0*(atmelraw[0] & 0xf) + (atmelraw[1] & 0xfe)/16.0
print "Atmel temp: ", atmeltemp

# read Zynq XADC temp through IIO driver (XAPP1172, UG480)

f = open('/sys/bus/iio/devices/iio:device0/in_temp0_raw','r')
zynqraw = f.read()
f.close()
zynqtemp = int(zynqraw)*503.975/4096 - 273.15
print "Zynq temp: ", zynqtemp



