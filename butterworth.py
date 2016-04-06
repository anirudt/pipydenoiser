import scipy.io.wavfile
import numpy as np
import pdb
import matplotlib.pyplot as plt
import wave
import cmath, math
import optparse
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
def main():
    sample_rate, bkgnd = scipy.io.wavfile.read('a3.wav')
    bkgnd = np.mean(bkgnd, axis=1, dtype=np.int16)
    t = range(len(bkgnd))
    sig = butter_bandpass_filter(bkgnd, 10, 2000, sample_rate, 5)
    scipy.io.wavfile.write('out/a3.wav', sample_rate, sig.real)
if __name__ == '__main__':main()