import os
import numpy as np
from scipy.io import wavfile
import operator
import sys

def run():
	print "Creating file voiceCepstrums.arff..."

	files = []
	output = open("voiceCepstrums.arff", 'w')

	for x in os.walk("AudioRecordings"):
		files.append(x)
	females = files[1][2]
	males = files[2][2]

	output.write("@relation voiceCepstrums\n\n")
	output.write("@attribute coefficient1 Continuous\n")
	output.write("@attribute coefficient2 Continuous\n")
	output.write("@attribute coefficient3 Continuous\n")
	output.write("@attribute coefficient4 Continuous\n")
	output.write("@attribute coefficient5 Continuous\n")
	output.write("@attribute gender {male, female}\n\n")

	output.write("@data\n")

	for filename in males:
		if filename.endswith(".wav") or filename.endswith(".WAV"):
			sampFreq, data = wavfile.read('AudioRecordings/Male/' + filename)
			cepstrum = getCepstrum(data)
			frequencies = {}
			for i in range(0, len(data)):
				coefficient = data[i]
				if coefficient[0] != float('Inf') and coefficient[0] != 0.0:
					frequency = (i*sampFreq)/len(data)
					frequencies[frequency] = coefficient[0];
			sortedFrequencies = sorted(frequencies.items(), key=operator.itemgetter(1), reverse=True);
			sortedFrequencies = sortedFrequencies
			for i in range(0, 5):
				output.write(str(sortedFrequencies[i][0]))
				output.write(", ")
			output.write("male\n")

	for filename in females:
		if filename.endswith(".wav") or filename.endswith(".WAV"):
			sampFreq, data = wavfile.read('AudioRecordings/Female/' + filename)
			# time =float(len(data))/float(sampFreq)
			# frequency = 
			cepstrum = getCepstrum(data)
			frequencies = {}
			for i in range(0, len(data)):
				coefficient = data[i]
				if coefficient[0] != float('Inf') and coefficient[0] != 0.0:
					frequency = (i*44100)/len(data)
					frequencies[frequency] = coefficient[0];
			sortedFrequencies = sorted(frequencies.items(), key=operator.itemgetter(1), reverse=True);
			sortedFrequencies = sortedFrequencies
			for i in range(0, 5):
				output.write(str(sortedFrequencies[i][0]))
				output.write(", ")
			output.write("female\n")

def getCepstrum(input):
	return np.abs(np.fft.ifft((np.log((np.abs(np.fft.fft(input)))*(np.abs(np.fft.fft(input)))))))*np.abs(np.fft.ifft((np.log((np.abs(np.fft.fft(input)))*(np.abs(np.fft.fft(input)))))))

if __name__ == "__main__":
    run()