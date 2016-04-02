import scipy.io.wavfile
from scipy.fftpack import *
import numpy as np
import pdb
import matplotlib.pyplot as plt
from pydub import AudioSegment
import wave
# TODO: Import the auto-record module, and 
# record the sounds with and without signal.

# IDEAL FILTER GETTER
def load_ideal_filter(opt, N):
    if opt == '1':
        for i in range(N):
            if i >= N//2-300 && i <= N//2-15:
                H.append(1)
            if i >= N//2+15 && i <= N/2+300:
                H.append(1)
            else:
                H.append(0)
    if opt == '2':
        for i in range(N):
            if i >= N//2-1000 && i <= N//2-5:
                H.append(1)
            if i >= N//2+5 && i <= N/2+1000:
                H.append(1)
            else:
                H.append(0)
    return H

def get_SNR(X, Y):
    """ 
    Assuming that the output signal is pure signal, 
    we compute the SNR, also knowing that the input
    signal has both the pure signal and noise. We also assume
    that the signal and the noise are uncorrelated, hence:
    Input Power = norm(X)^2 / N;
    Output Power = norm(Y)^2 / N;
    """
    X = np.array(X)
    Y = np.array(Y)
    Px = sum(abs(X)*abs(X))
    Py = sum(abs(Y)*abs(Y))
    return 20.0*math.log(Py/Px)

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

    Y = filter(freq_resp, '1')

def filter(X, s):
    # Sample first half:
    H = load_ideal_filter(s)
    Y = [H[i]*X[i] for i in range(len(X))]

    # Assuming that it is fftshifted initially.
    Y = np.fft.ifftshift(Y)
    y = np.ifft(Y)
    return y

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
