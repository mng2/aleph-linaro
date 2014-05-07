"""
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

time = range(0,2048)
channelA = [np.sqrt(2)*np.sin(2*np.pi*14.9e6*t/125e6) for t in time]


fig = plt.figure()

ax2 = fig.add_subplot(211)

ax2.plot(channelA,color='green')

ax2.set_title("Terminated Input")
ax2.set_xlim(0, 2048)
ax2.set_xlabel('Sample Number (125 Msps)')
ax2.set_ylabel('Voltage (V)')


ax3 = fig.add_subplot(212)

ps = 10*np.log10(np.abs(np.fft.fft(channelA))**2 / 50. / 1000.) - 3.0

time_step = 1. / 125e6
freqs = np.fft.fftfreq(len(channelA), time_step)
idx = np.argsort(freqs)

ax3.plot(freqs[idx], ps[idx],color='green')
ax3.set_xlim(0,62.5e6)
ax3.set_ylabel('Power (dBm)')
#fig.tight_layout()
plt.show()
