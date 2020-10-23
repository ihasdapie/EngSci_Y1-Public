#!/usr/bin/python
import numpy as np 
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# load data
f = open('finaldata.csv') # your data file name
# your file should be in this format:
# time, amplitude
# I used ", " as a delimiter, if you used spaces or anything
# just change it in the .split() on line 15 to whatever you used
# amp. doesn't have to be in radians but should cross the x-axis

amp_err = 0.0117453 # 1 degree
time_err = 0.016666 # 1 frame


b = f.readlines()
b = [i.strip().split(', ') for i in b]

# yes, we are comparing floats
# don't really need to be that precise though: data isn't perfect anyways
b = [(float(i[0]), float(i[1])) for i in b]

nb = np.array([(i[0], i[1]) for i in b])
nbt = nb.transpose()

# find positive peaks(pp), negative peaks
pp = find_peaks(nbt[1], prominence=0.3)[0]
pn = find_peaks(nbt[1]*-1, prominence=0.3)[0] # you may have to change the prominence values depending on your setup. .3 should work for most
peaks = np.concatenate((pp, pn), axis=0)


# plot maxima on top of previous graph, just for show
plt.plot(nbt[0], nbt[1], 'g.', label="all data")
plt.plot(nbt[0][peaks], nbt[1][peaks], 'bo',label= "maxima")

plt.xlabel("Time, s")
plt.ylabel("Amplitude, θ")
plt.title("Amplitude vs Time")
plt.legend(loc='upper right')
plt.show()

# extract amplitue & time data

# for maxima
p_amp = nbt[1][pp][:len(pp)-1]
p_period = nbt[0][pp]
p_period = np.array([p_period[i]-p_period[i-1] for i in range(1, len(p_period))])
p_time_err = np.array([time_err for i in range(len(p_amp))]) # this is ugly
p_amp_err = np.array([amp_err for i in range(len(p_period))])


# for minima
n_amp = nbt[1][pn][:len(pn)-1]
n_period = nbt[0][pn]
n_period = np.array([n_period[i]-n_period[i-1] for i in range(1, len(n_period))])


n_time_err = np.array([time_err for i in range(len(n_amp))]) # this is ugly
n_amp_err = np.array([amp_err for i in range(len(n_period))])

# plot period vs amp for minima 
plt.errorbar(n_amp, n_period, yerr=  n_time_err, xerr = n_amp_err, fmt='.')
plt.xlabel("Amplitude, θ")
plt.ylabel("Period, T")
plt.title("Period vs Amplitude")
plt.show()


# plot period vs amp for maxima
plt.errorbar(p_amp, p_period, yerr=  p_time_err, xerr = p_amp_err, fmt='.')
plt.xlabel("Amplitude, θ")
plt.ylabel("Period, T")
plt.title("Period vs Amplitude")
plt.show()




# Note that if you used tracker data and had time in (1/60)s like me, 
# your graph period v. amp will have distinct horz. bars of data
# This is because of rounding error and you should see that
# whatever varience in there is experimentally zero.







