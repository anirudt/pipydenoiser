import scipy.io.wavfile
from scipy.fftpack import *
import numpy as np
import pdb
import matplotlib.pyplot as plt
from pydub import AudioSegment
import wave
import cmath, math

#################################################################################################
# IDEAL FILTER GETTER
def load_ideal_filter(opt, N):
    H = []
    if opt == '1':
        w_lc = 15
        w_hc = 300
    if opt == '2':
        w_lc = 5
        w_hc = 1000
    for i in range(N):
        if i > (N//2-w_hc) and i < (N//2-w_lc):
            H.append(1)
            continue
        if i > (N//2+w_lc) and i < (N//2+w_hc):
            H.append(1)
            continue
        else:
            H.append(0)
    freq_axis = range(-N//2, N//2)
    graphify_plot(freq_axis, H, "frequency axis", \
            "amplitude", "Filter Plot", "filt")
    return H

#################################################################################################
# Getter Functions
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

def get_params():
    """ 
    Returns parameters of the audio file 
    in the following order:
    [nchannels, sampwidth, framerate, nframes, comptype, compname, samplerate]
    """
    f = wave.open('records/myvoice.wav', 'rb')
    [Fs, g] = scipy.io.wavfile.read('records/myvoice.wav') 
    list_p = list(f.getparams())
    print Fs
    list_p.append(Fs)
    return list_p

#################################################################################################
# Helper Functions for plotting
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

#################################################################################################
# Core Functionality
def filter(X, s):
    # Sample first half:
    H = load_ideal_filter(s, len(X))
    Y = [H[i]*X[i] for i in range(len(X))]
    # pdb.set_trace()

    # Assuming that it is fftshifted initially.
    Yi = np.fft.ifftshift(Y)
    y = ifft(Yi)
    return y, Y

def capture_bkgnd():
    sample_rate, bkgnd = scipy.io.wavfile.read('records/myvoice.wav')

    # Takes the average of both channels
    bkgnd = np.mean(bkgnd, axis=1)
    t = range(len(bkgnd))

    a = get_params()
    Fs = a[-1]
    #pdb.set_trace()
    freq_resp = fft(bkgnd)
    freq_resp = list(np.fft.fftshift(freq_resp))
    freq_axis = list(np.arange(-Fs/2,Fs/2,Fs*1.0/len(bkgnd)))
    length = len(freq_resp)
    print len(freq_axis), len(freq_resp)
    graphify_plot(freq_axis, np.abs(freq_resp), "frequency axis", \
            "amplitude", "Voice Freq Plot", "voice")

    y, Y = filter(freq_resp, '2')
    print "SNR is ", get_SNR(freq_resp, Y)
    graphify_plot(freq_axis, np.abs(Y), "frequency axis", \
            "amplitude", "Filtered Voice Freq Plot", "filt_voice_freq")
    real_y = np.array([y[i].real for i in range(len(y))], dtype=np.int16)
    graphify_plot(t, real_y, "Time axis", \
            "amplitude", "Filtered Voice Time Plot", "filt_voice")

    #TODO: Plot the real value of y versus time, and write to a 
    # wav file, and play it.
    # Reshaping the matrix
    out = np.array(list(real_y)+list(real_y), dtype = np.int16)
    out = out.reshape((len(bkgnd), 2))
    # pdb.set_trace()
    scipy.io.wavfile.write('records/proc_myvoice.wav', sample_rate, out)

# TODO: Enhance this module.
def vol_add():
    f = AudioSegment.from_wav('records/myvoice.wav')
    f1 = f + 10
    f.export('records/hi_myvoice.wav', "wav")

if __name__ == '__main__':
    # TODO: Auto-capture background noise signal
    print get_params()
    capture_bkgnd()
    # load_ideal_filter('1', 1000)
    # TODO: Auto-capture required signal
