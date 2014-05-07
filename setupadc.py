import spidev

spi = spidev.SpiDev()

print "Opening SPI device 1 (LTC2185 L)..."
spi.open(32766,1)
print "Resetting device..."
spi.xfer2([0x00,0x80])
print "Setting output mode to DDR LVDS..."
spi.xfer2([0x03,0x01])
print "Setting output mode to offset binary..."
spi.xfer2([0x04,0x00])
spi.close()

print "Opening SPI device 2 (LTC2185 R)..."
spi.open(32766,2)
print "Resetting device..."
spi.xfer2([0x00,0x80])
print "Inverting clock phase..."
spi.xfer2([0x02,0x08])
print "Setting output mode to DDR LVDS..."
spi.xfer2([0x03,0x01])
#print "Setting format to 2's complement..."
#spi.xfer2([0x04,0x01])
spi.close()

print "Done."

