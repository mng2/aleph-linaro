# read Atmel AT30TSE004A temp through I2C


# read Zynq XADC temp through IIO driver (XAPP1172, UG480)

f = open('/sys/bus/iio/devices/iio:device0/in_temp0_raw','r')
zynqraw = f.read()
f.close()
zynqtemp = int(zynqraw)*503.975/4096 - 273.15
print "Zynq temp: ", zynqtemp



