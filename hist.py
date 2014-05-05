"""
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

channelA = []
channelB = []

fin = open('term2048.txt','rb')

for line in fin:
  #print lineno
  #lineno = lineno + 1
  temp = line.split(' ')
  if temp[0] != '!':
    channelA.append(int(temp[0],16)-32767)
    channelB.append(int(temp[1],16)-32767)
  


fig = plt.figure()
ax = fig.add_subplot(111)

#bins = np.linspace(-10, 10, 100)
bins=20

ax.hist(channelA, bins, alpha=0.5)#, legend='Channel A')
ax.hist(channelB, bins, alpha=0.5)#, legend='Channel B')
#ax.legend(loc='upper right')

#n, bins, patches = ax.hist(channelA, 20, facecolor='green', alpha=0.5)

ax.set_xlabel('Output Code')
ax.set_ylabel('Count')
ax.set_title("Terminated Input Histogram (centered at 32767)")
#ax.set_xlim(40, 160)
#ax.set_ylim(0, 0.03)
ax.grid(True)

plt.show()
