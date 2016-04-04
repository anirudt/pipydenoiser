## What?
Python audio filtering module.

## TODO:
* Analyse the noise and search for harmonics
* Get way for amplifying the audio, adding dB gain
* Study about standard Audio Pre-processing techniques.
* Make a function for calculating SNR.
* Read clip frame by frame, formatting from ```wave``` module
* Test for more data, similar conditions.

## Capturing Audio from the Pi:
* To record a clip, type in ```rec filename.wav```.
* To play the clip, type in ```aplay filename.wav```.

## Things Done
* Getter function for params
* Normalise the x axis into frequency, and try to locate the voice-frequency component approximately.
* Pass a normal LPF around it and try, get results
* Adding OptParsing for convenience
