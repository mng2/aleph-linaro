import spidev

spi = spidev.SpiDev()

print "Opening SPI device 0 (AD9512)..."
spi.open(32766,0)
print "Disabling input 2..."
spi.xfer2([0x00,0x45,0x05])
print "Setting FPGA clock to 1x..."
spi.xfer2([0x00,0x53,0x80])
print "Setting DAC clock to 1x..."
spi.xfer2([0x00,0x4d,0x80])
# ADC L 0x4b, ADC R 0x4f, SATA 0x51
spi.xfer2([0x00,0x5a,0x01]) # update

spi.close()

print "Done."

