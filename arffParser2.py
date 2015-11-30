import os
import numpy as np
from scipy.io import wavfile
import operator
import sys

def run():
	print "Creating file voiceCepstrums2.arff..."

	files = []
	output = open("voiceCepstrums2.arff", 'w')

	for x in os.walk("AudioRecordings"):
		files.append(x)
	females = files[1][2]
	males = files[2][2]

	output.write("@relation voiceCepstrums\n\n")
	output.write("@attribute range1 Continuous\n")
	output.write("@attribute range2 Continuous\n")
	output.write("@attribute range3 Continuous\n")
	output.write("@attribute range4 Continuous\n")
	output.write("@attribute range5 Continuous\n")
	output.write("@attribute range6 Continuous\n")
	output.write("@attribute range7 Continuous\n")
	output.write("@attribute range8 Continuous\n")
	output.write("@attribute range9 Continuous\n")
	output.write("@attribute range10 Continuous\n")
	output.write("@attribute gender {male, female}\n\n")

	output.write("@data\n")

	for filename in males:
		if filename.endswith(".wav") or filename.endswith(".WAV"):
			sampFreq, data = wavfile.read('AudioRecordings/Male/' + filename)
			fftWindows = getFFTWindows(data)
			for i in range(0, 10):
				output.write(str(fftWindows[i]))
				output.write(", ")
			output.write("male\n")

	for filename in females:
		if filename.endswith(".wav") or filename.endswith(".WAV"):
			sampFreq, data = wavfile.read('AudioRecordings/Female/' + filename)
			fftWindows = getFFTWindows(data)
			for i in range(0, 10):
				output.write(str(fftWindows[i]))
				output.write(", ")
			output.write("female\n")

def getFFTWindows(input):
	windows = {}
	fft = np.fft.fft(input)
	windowLength = len(fft)/10
	for i in range(0, len(fft)):
		if i/windowLength in windows:
			windows[i/windowLength] = windows[i/windowLength] + fft[i][0].real
		else:
			windows[i/windowLength] = fft[i][0].real
	return windows

if __name__ == "__main__":
    run()