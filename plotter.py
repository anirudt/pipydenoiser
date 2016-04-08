import proc
import pickle

time_taken_ideal = pickle.load(open('ideal_filt_list.li', 'rb'))
time_taken_butter= pickle.load(open('butter_filt_list.li', 'rb'))

print time_taken_ideal, time_taken_butter

t = range(3, 10)
#proc.graphify_plot(t, time_taken_ideal, "Record length", \
#              "Time Taken", "Ideal Filter Time Complexity", "ideal_filter_time")

proc.graphify_plot(t, time_taken_butter, "Record length", \
              "Time Taken", "Butterworth Filter Time Complexity", "butter_filter_time")
