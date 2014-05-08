"""
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import windowing as w

channelA = []
channelB = []

fin = open('term2048.txt','rb')

for line in fin:
  #print lineno
  #lineno = lineno + 1
  temp = line.split(' ')
  if temp[0] != '!':
    channelA.append(int(temp[0],16)-32768)
    channelB.append(int(temp[1],16)-32768)
  


voltageA = [a/65535. for a in channelA]

fig = plt.figure()

ax2 = fig.add_subplot(311)

ax2.plot([a*1000./65535. for a in channelA],color='green')
ax2.plot([a*1000./65535. for a in channelB],color='blue')
ax2.set_title("Terminated Input")
ax2.set_xlim(0, 2048)
ax2.set_xlabel('Sample Number (125 Msps)')
ax2.set_ylabel('Voltage (mV)')

ax = fig.add_subplot(312)

#bins = np.linspace(-10, 10, 100)
bins=20

ax.hist(channelA, bins, alpha=0.5, facecolor='green')#, legend='Channel A')
ax.hist(channelB, bins, alpha=0.5, facecolor='blue')#, legend='Channel B')
#ax.legend(loc='upper right')

#n, bins, patches = ax.hist(channelA, 20, facecolor='green', alpha=0.5)

ax.set_xlabel('Output Code')
ax.set_ylabel('Count')
ax.set_title("Terminated Input Histogram (centered at 32767)")
#ax.set_xlim(40, 160)
#ax.set_ylim(0, 0.03)
ax.grid(True)

ax3 = fig.add_subplot(313)

ps = 10*np.log10(np.abs(np.fft.fft(voltageA))**2 / 50. / 1000.) - 3.0 # dBm
window = w.blackmanharris(2048)
pw = 10*np.log10(np.abs(np.fft.fft(voltageA*window))**2 / 50. / 1000.) - 3.0 # dBm

time_step = 1. / 125e6
freqs = np.fft.fftfreq(len(channelA), time_step)
idx = np.argsort(freqs)

ax3.plot(freqs[idx], ps[idx],color='green',alpha=0.5)
ax3.plot(freqs[idx], pw[idx],color='orange',alpha=0.75)
ax3.set_xlim(0,62.5e6)
ax3.set_ylabel('Power (dBm)')

#fig.tight_layout()
plt.show()
