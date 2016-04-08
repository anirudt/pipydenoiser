#!/usr/bin/python
import os, time
import proc

time_taken_ideal = []
for i in range(30):
    st = time.time()
    os.system('rec records/time'+str(i)+'.wav trim 0 0:'+str(i))
    os.system('./proc.py -i records/time'+str(i)+'.wav -q')

time_taken_butter = []
for i in range(30):
    st = time.time()
    os.system('rec records/time'+str(i)+'.wav trim 0 0:'+str(i))
    os.system('./proc.py -i records/time'+str(i)+'.wav -q -f b')
    time_taken_butter.append(time.time() - st)

if __name__ == '__main__':
    t = range(30)
    proc.graphify_plot(t, time_taken_ideal, "Record length", \
            "Computation time", "Ideal Filter", "ideal_filt_time")
    proc.graphify_plot(t, time_taken_butter, "Record length", \
            "Computation time", "Butterworth Filter", "butter_filt_time")
