"""
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sys

channelA = []
channelB = []
channelC = []
channelD = []

#print sys.argv
fin = open(sys.argv[1],'rb')

for line in fin:
  #print lineno
  #lineno = lineno + 1
  temp = line.split(' ')
  if temp[0] != '!':
    channelA.append(int(temp[0],16)-32768)
    channelB.append(int(temp[1],16)-32768)
    channelC.append(int(temp[2],16)-32768)
    channelD.append(int(temp[3],16)-32768)
  


voltageA = [a/65535. for a in channelA]

fig = plt.figure()

ax2 = fig.add_subplot(111)

ax2.plot([a*1000./65535. for a in channelA],color='green')
ax2.plot([a*1000./65535. for a in channelB],color='blue')
ax2.plot([a*1000./65535. for a in channelC],color='red')
ax2.plot([a*1000./65535. for a in channelD],color='orange')
ax2.set_title("5 MHz Input from function generator")
ax2.set_xlim(0, 2048)
ax2.set_xlabel('Sample Number (125 Msps)')
ax2.set_ylabel('Voltage (mV)')

#fig.tight_layout()
plt.show()
