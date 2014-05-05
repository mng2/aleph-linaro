import spidev

spi = spidev.SpiDev()

print "Opening SPI device 1 (LTC2185 L)..."
spi.open(32766,1)
print "Resetting device..."
spi.xfer2([0x00,0x80])
print "Setting output mode to DDR LVDS..."
spi.xfer2([0x03,0x01])

spi.close()

print "Done."

