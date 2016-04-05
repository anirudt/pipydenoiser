import scipy.io.wavfile
import numpy as np
import pdb
import matplotlib.pyplot as plt
import wave
import cmath, math
import optparse

desc = "This is an audio processing tool, to eliminate background noise present in audio clips."

def parseCmd():
    p = optparse.OptionParser(description=desc)
    p.add_option('-q', '--quiet', dest='qu', action='store_true', default = False, help='Do not print graphs')
    p.add_option('-v', '--verbose', dest='ve', action='store_true', default = False, help='Print graphs')
    p.add_option('-i', '--input', dest='inp', default = '', help='File input')
    p.add_option('-o', '--output', dest='out', default = '', help='File output')
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
        w_hc = 2000*N/Fs*1.0
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

def get_params(opts):
    """ 
    Returns parameters of the audio file 
    in the following order:
    [nchannels, sampwidth, framerate, nframes, comptype, compname, samplerate]
    """
    if opts.inp:
        f = wave.open(opts.inp, 'rb')
        [Fs, g] = scipy.io.wavfile.read('records/myvoice.wav') 
    else:
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
    H1 = combing(X, Fs, H)

    num = sum([H[i]!=H1[i] for i in range(len(H))])
    print "#Harmonics", num

    Y = [H[i]*X[i] for i in range(len(X))]
    Y1 = [H1[i]*X[i] for i in range(len(X))]
    # pdb.set_trace()

    # Assuming that it is fftshifted initially.
    Yi = np.fft.ifftshift(Y)
    y = np.fft.ifft(Yi)

    Yi = np.fft.ifftshift(Y1)
    y1 = np.fft.ifft(Yi)
    return y, Y, y1, Y1

def combing(X, Fs, H):
    avg = np.mean(abs(X))
    alpha = 5
    thresh = alpha*avg
    print thresh
    H = [H[i] if abs(X[i])<thresh else 0 for i in range(len(H))]
    return H


def capture_bkgnd(opts):
    if opts.inp:
        sample_rate, bkgnd = scipy.io.wavfile.read(opts.inp)
    else:
        sample_rate, bkgnd = scipy.io.wavfile.read('records/myvoice.wav')
    # Takes the average of both channels
    bkgnd = np.mean(bkgnd, axis=1, dtype=np.int16)
    t = range(len(bkgnd))

    a = get_params(opts)
    Fs = a[-1]

    N = len(bkgnd)
    freq_resp = np.fft.fft(bkgnd)

    freq_resp = (np.fft.fftshift(freq_resp))
    freq_axis = (np.arange(-Fs/2,Fs/2,Fs*1.0/len(bkgnd)))

    y, Y, y1, Y1 = filter(freq_resp, '2', sample_rate)

    # COMBED OUTPUTs
    real_y1 = np.array([b[i].real for i in range(len(b))], dtype=np.int16)
    real_y1 = vol_add(real_y1, 5)

    print "SNR is ", get_SNR(freq_resp, Y)

    # NORMAL OUTPUT
    real_y = np.array([y[i].real for i in range(len(y))], dtype=np.int16)
    data_up = vol_add(real_y, 5)

    # Getting requisite plots.
    if opts.ve:
        graphify_plot(freq_axis, np.abs(freq_resp), "frequency axis", \
            "amplitude", "Voice Freq Plot", "voice")

        graphify_plot(freq_axis, np.abs(Y), "frequency axis", \
            "amplitude", "Filtered Voice Freq Plot", "filt_voice_freq")
        graphify_plot(freq_axis, np.abs(B), "frequency axis", \
            "amplitude", "Filtered Voice Freq Plot Combed", "comb_filt_voice_freq")
        graphify_plot(t, real_y1, "Time axis", \
            "amplitude", "Filtered Voice Time Plot Combed", "comb_filt_voice")
        graphify_plot(t, real_y, "Time axis", \
            "amplitude", "Filtered Voice Time Plot", "filt_voice")
        graphify_plot(t, data_up, "Time axis", \
            "amplitude", "Filtered Voice Time Plot", "filt_voice_high")
        graphify_plot(t, bkgnd, "Time axis", \
            "amplitude", "Original Voice Time Plot", "my_voice")

    # Writing the filtered output to a file
    if opts.out:
        scipy.io.wavfile.write(out, sample_rate, real_y)
        scipy.io.wavfile.write('high'+out, sample_rate, data_up)
        scipy.io.wavfile.write('comb'+out, sample_rate, real_y1)
    else:
        scipy.io.wavfile.write('records/proc_myvoice.wav', sample_rate, real_y)
        scipy.io.wavfile.write('records/proc_myvoice_high.wav', sample_rate, data_up)
        scipy.io.wavfile.write('records/comb_proc_myvoice.wav', sample_rate, real_y1)

def vol_add(data, gain):
    """
    Returns a signal with gain as follows:
    Gain = 20*log(gain).
    where 
    gain-> argument
    """
    data_up = np.array([gain*data[i] for i in range(len(data))], dtype=np.int16)
    return data_up

if __name__ == '__main__':
    # TODO: Auto-capture background noise signal
    opts = parseCmd()
    print get_params(opts)
    capture_bkgnd(opts)
    # load_ideal_filter('1', 1000)
    # TODO: Auto-capture required signal
