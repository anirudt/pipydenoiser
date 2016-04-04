import scipy.io.wavfile
#from scipy.fftpack import *
import numpy as np
import pdb
import matplotlib.pyplot as plt
from pydub import AudioSegment
import wave
import cmath, math
import optparse

desc = "This is an audio processing tool, to eliminate background noise present in audio clips."

def parseCmd():
    p = optparse.OptionParser(description=desc)
    p.add_option('-q', '--quiet', dest='qu', action='store_true', default = False, help='Do not print graphs')
    p.add_option('-v', '--verbose', dest='ve', action='store_true', default = False, help='Print graphs')
    (opts, args) = p.parse_args()
    return opts

#################################################################################################
# IDEAL FILTER GETTER
def load_ideal_filter(opt, N, Fs):
    H = []
    if opt == '1':
        # CONSTRICTED LPF
        w_lc = 15*N/Fs*1.0
        w_hc = 300*N/Fs*1.0
    if opt == '2':
        # BROADER LPF
        w_lc = 5*N/Fs*1.0
        w_hc = 1000*N/Fs*1.0
    if opt == '3':
        # ALL PASS FILTER
        w_lc = 0.0
        w_hc = N*1.0
    for i in range(N):
        if i >= (N//2-w_hc) and i <= (N//2-w_lc):
            H.append(1)
        elif i >= (N//2+w_lc) and i <= (N//2+w_hc):
            H.append(1)
        else:
            H.append(0)
    freq_axis = list(np.arange(-Fs/2,Fs/2,Fs*1.0/N))
    if opts.ve:
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
    Input Power = Noise + Signal Power = norm(X)^2 / N;
    Output Power = Signal Power = norm(Y)^2 / N;
    SNR = 10 log (Signal)
    """
    X = np.array(X)
    Y = np.array(Y)
    Px = sum(abs(X)*abs(X))
    Py = sum(abs(Y)*abs(Y))
    return 10.0*math.log(Py/(Px-Py))

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
def filter(X, s, Fs):
    # Sample first half:
    H = load_ideal_filter(s, len(X), Fs)
    Y = [H[i]*X[i] for i in range(len(X))]
    # pdb.set_trace()

    # Assuming that it is fftshifted initially.
    Yi = np.fft.ifftshift(Y)
    y = np.fft.ifft(Yi)
    return y, Y

def capture_bkgnd(opts):
    sample_rate, bkgnd = scipy.io.wavfile.read('records/myvoice.wav')

    # Takes the average of both channels
    bkgnd = np.mean(bkgnd, axis=1, dtype=np.int16)
    t = range(len(bkgnd))

    a = get_params()
    Fs = a[-1]
    #pdb.set_trace()
    N = len(bkgnd)
    freq_resp = np.fft.fft(bkgnd)
    #pdb.set_trace()
    freq_resp = (np.fft.fftshift(freq_resp))
    freq_axis = (np.arange(-Fs/2,Fs/2,Fs*1.0/len(bkgnd)))

    y, Y = filter(freq_resp, '2', sample_rate)
    print "SNR is ", get_SNR(freq_resp, Y)
    real_y = np.array([y[i].real for i in range(len(y))], dtype=np.int16)

    # Getting requisite plots.
    if opts.ve:
        graphify_plot(freq_axis, np.abs(freq_resp), "frequency axis", \
            "amplitude", "Voice Freq Plot", "voice")

        graphify_plot(freq_axis, np.abs(Y), "frequency axis", \
            "amplitude", "Filtered Voice Freq Plot", "filt_voice_freq")
        graphify_plot(t, real_y, "Time axis", \
            "amplitude", "Filtered Voice Time Plot", "filt_voice")
        graphify_plot(t, bkgnd, "Time axis", \
            "amplitude", "Original Voice Time Plot", "my_voice")

    # Writing the filtered output to a file
    scipy.io.wavfile.write('records/proc_myvoice.wav', sample_rate, real_y)

# TODO: Enhance this module.
def vol_add():
    f = AudioSegment.from_wav('records/myvoice.wav')
    f1 = f + 10
    f.export('records/hi_myvoice.wav', "wav")

if __name__ == '__main__':
    # TODO: Auto-capture background noise signal
    opts = parseCmd()
    print get_params()
    capture_bkgnd(opts)
    # load_ideal_filter('1', 1000)
    # TODO: Auto-capture required signal
