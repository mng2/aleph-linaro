import csv
import re
import sys
import matplotlib.pyplot as plt

fin = csv.reader(open(sys.argv[1],'rb'))

abscissae = []
ordinates = []
flag = 0

for row in fin:
  if flag==1:
    ordinates.append(float(row[0])/1e6)
    abscissae.append(float(row[1]))
  
  elif row!=[]:
    temp=row[0].split(' ')
    if temp[0]=='trace_data':
      flag = 1
    
  
fig = plt.figure()
ax2 = fig.add_subplot(111)
ax2.plot(ordinates,abscissae)
ax2.set_xlim(0,62.5)
ax2.set_ylim(-120,0)
ax2.set_title('Aleph DAC Output Spectrum, 14.9 MHz sine')
ax2.set_ylabel('Power (dBm)')
ax2.set_xlabel('Frequency (MHz)')
plt.show()

print "done"
 


