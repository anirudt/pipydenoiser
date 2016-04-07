## What?
Python audio filtering module.

## TODO:
* Analyse the noise and search for harmonics
* Study about standard Audio Pre-processing techniques.
* Read clip frame by frame, formatting from ```wave``` module
* Dumping / Loading the filter coeffs, for faster computation
* Combing + ButterWorth.

## Capturing Audio from the Pi:
* To record a clip, type in ```rec filename.wav```.
* To play the clip, type in ```aplay filename.wav```.

## Things Done
* Test for more data, similar conditions.
* Getter function for params
* Normalise the x axis into frequency, and try to locate the voice-frequency component approximately.
* Pass a normal LPF around it and try, get results
* Get way for amplifying the audio, adding dB gain
* Make a function for calculating SNR.
* Adding OptParsing for convenience
* Added Combing filter, for removing certain high power harmonics, using a naive thresholding method.
* Adding ButterWorth filter, working
