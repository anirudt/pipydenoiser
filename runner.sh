#!/bin/bash
rec records/myvoice.wav trim 0 0:10
python proc.py
aplay records/proc_myvoice.wav
