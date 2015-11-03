import os
import numpy as np
from scipy.io import wavfile

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
	output.write("@attribute coefficient6 Continuous\n")
	output.write("@attribute coefficient7 Continuous\n")
	output.write("@attribute coefficient8 Continuous\n")
	output.write("@attribute coefficient9 Continuous\n")
	output.write("@attribute coefficient10 Continuous\n")
	output.write("@attribute gender {male, female}\n\n")

	output.write("@data\n")

	for filename in males:
		if filename.endswith(".wav") or filename.endswith(".WAV"):
			sampFreq, data = wavfile.read('AudioRecordings/Male/' + filename)
			cepstrum = getCepstrum(data)
			toOutput = []
			for coefficient in cepstrum:
				if coefficient[0] != float('Inf') and coefficient[0] != 0.0:
					toOutput.append(coefficient[0])
			for i in range(0, 10):
				output.write(str(toOutput[i]))
				output.write(", ")
			output.write("male\n")

	for filename in females:
		if filename.endswith(".wav") or filename.endswith(".WAV"):
			sampFreq, data = wavfile.read('AudioRecordings/Female/' + filename)
			cepstrum = getCepstrum(data)
			toOutput = []
			for coefficient in cepstrum:
				if coefficient[0] != float('Inf') and coefficient[0] != 0.0:
					toOutput.append(coefficient[0])
			for i in range(0, 10):
				output.write(str(toOutput[i]))
				output.write(", ")
			output.write("female\n")

def getCepstrum(input):
	return np.abs(np.fft.ifft((np.log((np.abs(np.fft.fft(input)))*(np.abs(np.fft.fft(input)))))))*np.abs(np.fft.ifft((np.log((np.abs(np.fft.fft(input)))*(np.abs(np.fft.fft(input)))))))

if __name__ == "__main__":
    run()