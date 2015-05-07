
## PiPyDenoiser
Python module which denoises audio signals for the RaspberryPi. Effectively, it reduces background noise using conventional filtering techniques.

## Places to be used
Audio Input to the Raspberry Pi, or in clips with low SNR and high amplitude low frequency noise.

## Key Features
* Audio parameter getter
* Amplifying audio signals
* Ideal Filtering at software level
* Adding option parsing to enable better software engineering
* Butterworth bandpass filter to reduce background noise
* Artificial Combing to reduce high power harmonics

## Process Flow
![Process Flow](flow.png)

## Tool Usage
* To find out how to use the tool, use

  ```$ ./proc.py -h ``` for help instructions

* Additionally, to provide an input file, 

  ```$ ./proc.py -i inp_file.wav```
  [Currently, the tool supports only wav formats].

* Similarly, a ```-o``` is used to provide path to an output file.

  ```$ ./proc.py -o out_file.wav```

* If you are working remotely without X-support, you can process the audio using the quiet mode as follows:

  ```$ ./proc.py -q```

* Or, verbose mode for best visualisation! 

  ```$ ./proc.py -v```

* The ideal filter is the one enabled by default. If you wish to use an alternative Butterworth filter, we use the following argument:  

  ```$ ./proc.py -f b```.

* Artificial combing is enabled by using the ```-c``` option. This is however enabled only in the ideal filtering mode.

* You can add a certain volume gain by using the ```-k``` option. However, note that this is not in dB, but it is amplitude scaling in the time domain.

* Let us look at a composite command using all of these arguments.

  ```$ ./proc.py -i records/lab1_woac.wav -c -v -g 10 -f b ```, where we process the audio using the input file from the given path, with artificial combing, verbose output, gain as 10, and Butterworth filter.

## Brief Description
* Human voice signals have a frequency range of 300 Hz to 3.4 kHz. To reduce the bandwidth further [to curtail the noise signals], we use a bandwidth of about 5 Hz to 2000 Hz. 

* There are options to use an ideal filter, butterworth and artificial combing.

  * Ideal Filter: To analyse the frequency response, and objectively keep/remove certain frequency components.

  * Butterworth filter: To implement a practical realization of the above ideal filter.

  * Artificial Combing: It was observed that the noise signal had several high power harmonics in the low frequency range even after applying the ideal filter. Thus, to eliminate them, a naive thresholding was applied, which enabled our signal to get enhanced.
