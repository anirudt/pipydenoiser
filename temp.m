[x, Fs] = audioread('records/myvoice.wav');

xdft = fft(x);
half_xdft = xdft(1:length(x)/2+1); % only retaining the positive frequencies
freq = 0:Fs/length(x):Fs/2; % frequency vector from 0 to the Nyquist

t = 0:1:length(x)-1;
back_to_time = ifft(xdft);
figure, plot(t, abs(back_to_time));
figure, plot(freq, abs(half_xdft));
