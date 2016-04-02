[x, Fs]  = audioread('myvoice.wav'); 
sound(x, Fs);
% t = linspace(0,1,1e3);
% x = cos(2*pi*250*t)+randn(size(t));
xdft = fft(x);
% xdft = xdft(1:length(x)/2+1); % only retaining the positive frequencies
freq = -Fs/2:Fs/length(x):Fs/2; % frequency vector from 0 to the Nyquist
freq = freq(1:length(freq)-1);
% y = fftshift(xdft);
for i=1:1:(5*length(x)/Fs)
    xdft(i,:)=[0 0];
end
for i= ceil((1000*length(x)/Fs)):1:ceil(length(x)-(1000*length(x)/Fs))
    xdft(i,:)=[0 0];
end
for i= length(x)-ceil((5*length(x)/Fs)):1:length(x)
    xdft(i,:)=[0 0];
end
% freq = 1:1:length(x);
% [~,maxindex] = abs(xdft);
% plot(freq,abs(xdft));
y = ifft(xdft);
sound(real(y), Fs);
filename = 'voice5to1000.wav';
audiowrite(filename,real(y),Fs);
% y = ifft(xdft);
% figure, plot()
% fprintf('The maximum occurs at %2.1f Hz\n', freq(maxindex));
