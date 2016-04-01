import scipy.io.wavfile
from scipy.fftpack import *
import numpy as np
import pdb
import matplotlib.pyplot as plt
from pydub import AudioSegment
import wave
# TODO: Import the auto-record module, and 
# record the sounds with and without signal.

# Getter Function
def get_params():
    """ Returns parameters of the audio file 
        in the following order:
        [nchannels, sampwidth, framerate, nframes, comptype, compname, samplerate]
    """
    f = wave.open('records/myvoice.wav', 'rb')
    [Fs, g] = scipy.io.wavfile.read('records/myvoice.wav') 
    list_p = list(f.getparams())
    print Fs
    list_p.append(Fs)
    return list_p

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

def graphify_stem(x, y, xlabel, ylabel, title, name, axis=None):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.stem(x, y)
    plt.grid = True
    plt.savefig(name+'stem.png')
    plt.show()
    if axis != None:
        plt.axis(axis)
def capture_bkgnd():
    sample_rate, bkgnd = scipy.io.wavfile.read('records/myvoice.wav')

    a = get_params()
    Fs = a[-1]
    #pdb.set_trace()
    freq_resp = fft(bkgnd)
    freq_resp = np.fft.fftshift(freq_resp)
    freq_axis = list(np.arange(-Fs/2,Fs/2,Fs*1.0/len(bkgnd)))
    length = len(freq_resp)
    print len(freq_axis), len(freq_resp)
    graphify_plot(freq_axis, abs(freq_resp), "frequency axis", \
            "amplitude", "Voice Freq Plot", "freq_resp_signal")


def vol_add():
    f = AudioSegment.from_wav('records/myvoice.wav')
    f1 = f + 10
    f.export('records/hi_myvoice.wav', "wav")

if __name__ == '__main__':
    # TODO: Auto-capture background noise signal
    # This signal could be used as our noise estimate
    print get_params()
    capture_bkgnd()

    # TODO: Auto-capture required signal

    # TODO: Perform necessary processing.
    #pdb.set_trace()
