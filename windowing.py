import numpy as np

def blackmanharris(M, sym=True):
    """Return a minimum 4-term Blackman-Harris window.

Parameters
----------
M : int
Number of points in the output window. If zero or less, an empty
array is returned.
sym : bool, optional
When True (default), generates a symmetric window, for use in filter
design.
When False, generates a periodic window, for use in spectral analysis.

Returns
-------
w : ndarray
The window, with the maximum value normalized to 1 (though the value 1
does not appear if `M` is even and `sym` is True).

Examples
--------
Plot the window and its frequency response:

>>> from scipy import signal
>>> from scipy.fftpack import fft, fftshift
>>> import matplotlib.pyplot as plt

>>> window = signal.blackmanharris(51)
>>> plt.plot(window)
>>> plt.title("Blackman-Harris window")
>>> plt.ylabel("Amplitude")
>>> plt.xlabel("Sample")

>>> plt.figure()
>>> A = fft(window, 2048) / (len(window)/2.0)
>>> freq = np.linspace(-0.5, 0.5, len(A))
>>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
>>> plt.plot(freq, response)
>>> plt.axis([-0.5, 0.5, -120, 0])
>>> plt.title("Frequency response of the Blackman-Harris window")
>>> plt.ylabel("Normalized magnitude [dB]")
>>> plt.xlabel("Normalized frequency [cycles per sample]")

"""
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, 'd')
    odd = M % 2
    if not sym and not odd:
        M = M + 1
    a = [0.35875, 0.48829, 0.14128, 0.01168]
    n = np.arange(0, M)
    fac = n * 2 * np.pi / (M - 1.0)
    w = (a[0] - a[1] * np.cos(fac) +
         a[2] * np.cos(2 * fac) - a[3] * np.cos(3 * fac))
    if not sym and not odd:
        w = w[:-1]
    return w

