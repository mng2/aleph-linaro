
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import windowing

window = windowing.blackmanharris(2048)
plt.plot(window)
plt.title("Blackman-Harris window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")


plt.figure()
A = np.fft.fft(window, 2048) / (len(window)/2.0)
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(np.abs(np.fft.fftshift(A / abs(A).max())))
plt.plot(freq, response)
#plt.axis([-0.5, 0.5, -120, 0])
plt.title("Frequency response of the Blackman-Harris window")
plt.ylabel("Normalized magnitude [dB]")
plt.xlabel("Normalized frequency [cycles per sample]")

plt.show()
