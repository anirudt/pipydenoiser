import scipy.io.wavfile as wave
from scipy.fftpack import *
import numpy as np
import pdb
import matplotlib.pyplot as plt
# TODO: Import the auto-record module, and 
# record the sounds with and without signal.

# Helper Functions
def graphify_plot(x, y, xlabel, ylabel, title, name, axis=None):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(x, y)
    plt.grid = True
    plt.savefig(name+'.png')
    plt.show()
    if axis != None:
        plt.axis(axis)

def capture_bkgnd():
    sample_rate, bkgnd = wave.read('records/empty.wav')
    pdb.set_trace()
    freq_resp = fft(bkgnd)
    freq_resp = np.fft.fftshift(freq_resp)
    length = len(freq_resp)
    print "Length of the response is ", length
    freq_axis = range(-length/2, length/2)
    graphify_plot(freq_axis, freq_resp, "frequency axis", \
            "amplitude", "Voice Freq Plot", "freq_resp")

if __name__ == '__main__':
    # TODO: Auto-capture background noise signal
    # This signal could be used as our noise estimate
    capture_bkgnd()

    # TODO: Auto-capture required signal

    # TODO: Perform necessary processing.
    pdb.set_trace()
