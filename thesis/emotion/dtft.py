#!/usr/bin/env python

import numpy as np

from scipy.fftpack import fft,fft2, fftshift

import matplotlib.pyplot as plt

t = np.arange(256) #0-255

sp = np.fft.fft(np.sin(t)) # Compute the one-dimensional discrete Fourier Transform

freq = np.fft.fftfreq(t.shape[0]) # Return the Discrete Fourier Transform sample frequencies.

print(freq)

plt.plot(freq, sp.real, freq, sp.imag)

plt.show()

