"""
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sys
import windowing as w

channelA = []
channelB = []
channelC = []
channelD = []

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
voltageB = [a/65535. for a in channelB]
voltageC = [a/65535. for a in channelC]
voltageD = [a/65535. for a in channelD]

fig = plt.figure()

#ax2 = fig.add_subplot(211)

#ax2.plot([a*1000./65535. for a in channelA],color='green')
#ax2.plot([a*1000./65535. for a in channelB],color='blue')
#ax2.plot([a*1000./65535. for a in channelC],color='red')
#ax2.plot([a*1000./65535. for a in channelD],color='orange')
#ax2.set_title("Terminated Input")
#ax2.set_xlim(0, 2048)
#ax2.set_xlabel('Sample Number (125 Msps)')
#ax2.set_ylabel('Voltage (mV)')


ax3 = fig.add_subplot(111)

window = w.blackmanharris(2048)

psA = 10*np.log10(np.abs(np.fft.fft(window*voltageA))**2 / 50. / 1000.) - 3.0 + 13.0-4.17# dBm
psB = 10*np.log10(np.abs(np.fft.fft(window*voltageB))**2 / 50. / 1000.) - 3.0 + 13.0-4.17# dBm
psC = 10*np.log10(np.abs(np.fft.fft(window*voltageC))**2 / 50. / 1000.) - 3.0 + 13.0-4.17# dBm
psD = 10*np.log10(np.abs(np.fft.fft(window*voltageD))**2 / 50. / 1000.) - 3.0 + 13.0-4.17# dBm

time_step = 1. / 125. # work in terms of MHz
freqs = np.fft.fftfreq(len(channelA), time_step)
idx = np.argsort(freqs)

#ax3.plot(freqs[idx], psA[idx],color='green',alpha=0.5)
ax3.plot(freqs[idx], psB[idx],color='blue',alpha=0.5)
ax3.plot(freqs[idx], psC[idx],color='red',alpha=0.5)
#ax3.plot(freqs[idx], psD[idx],color='orange',alpha=0.5)
ax3.set_xlim(0,62.5)
ax3.set_ylim(-120,0)
ax3.set_title('FFT Power Spectrum')
ax3.set_ylabel('Power (dBm)')
ax3.set_xlabel('Frequency (MHz)')

#fig.tight_layout()
plt.show()
