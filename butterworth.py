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
    # TODO: probably test the freq response of the
    # filter formed, by using freqs command
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    # TODO: A debug print here, suggests that y has a lot of
    # NAN values. Try to find out what is happening, or go 
    # through this link: http://stackoverflow.com/questions/8811518/scipy-lfilter-returns-only-nans
    return y
    
def main():
    sample_rate, bkgnd = scipy.io.wavfile.read('records/a3.wav')
    bkgnd = np.mean(bkgnd, axis=1, dtype=np.int16)
    t = range(len(bkgnd))
    sig = np.array(butter_bandpass_filter(bkgnd, 10, 2000, sample_rate, 5), dtype=np.int16)
    scipy.io.wavfile.write('records/butterworth.wav', sample_rate, sig.real)

if __name__ == '__main__':
    main()
