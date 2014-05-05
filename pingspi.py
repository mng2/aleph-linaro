import spidev
import time

var = int(raw_input("SPI device: "))

spi = spidev.SpiDev()
spi.open(32766, var)

try:
  while True:
    resp = spi.xfer2([0x80])
  #end while
except KeyboardInterrupt:
  spi.close()
#end try

