import scipy.io.wavfile
import numpy as np
import pdb
import matplotlib.pyplot as plt
import wave
import cmath, math
import optparse
from scipy.signal import butter, lfilter
from scipy import signal

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    
    #print np.all(np.abs(np.roots(a))<1), (low, high, order), np.max(np.roots(a))
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    w, h = signal.freqz(b, a)
    Y = np.fft.fftshift(np.fft.fft(y))
    freq_axis = (np.arange(-fs/2,fs/2,fs*1.0/len(data)))
    plt.plot(freq_axis, abs(Y))
    plt.show()
    plt.plot(w, 20 * np.log10(abs(h)))
    plt.show()
    return y

def stable_filter_finder(Fs):
    low = [5, 10, 15, 20]
    high = [1000, 1200, 1500, 2000]
    order = [1,3,5,7,9,11,13,15]
    fs = Fs
    for l in low:
        for h in high:
            for o in order:
                butter_bandpass(l, h, Fs, o)

def main():
    sample_rate, bkgnd = scipy.io.wavfile.read('records/a3.wav')
    bkgnd = np.mean(bkgnd, axis=1, dtype=np.int16)
    t = range(len(bkgnd))
    sig = np.array(butter_bandpass_filter(bkgnd, 10, 2000, sample_rate, 3), dtype=np.int16)
    #stable_filter_finder(sample_rate)
    scipy.io.wavfile.write('records/butterworth.wav', sample_rate, sig.real)

if __name__ == '__main__':
    main()
