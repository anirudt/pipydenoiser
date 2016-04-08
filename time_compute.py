#!/usr/bin/python
import os, time
import proc
import pickle
#for i in range(3, 10):
#    os.system('rec records/time'+str(i)+'.wav trim 0 0:'+str(i))

time_taken_ideal = []
for i in range(3, 10):
    st = time.time()
    os.system('./proc.py -i records/time'+str(i)+'.wav -q')

time_taken_butter = []
for i in range(3, 10):
    st = time.time()
    os.system('./proc.py -i records/time'+str(i)+'.wav -q -f b')
    time_taken_butter.append(time.time() - st)

if __name__ == '__main__':
    t = range(3, 10)
    pickle.dump(time_taken_ideal, open('ideal_filt_list.li', 'wb'))
    pickle.dump(time_taken_butter, open('butter_filt_list.li', 'wb'))
