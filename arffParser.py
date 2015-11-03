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
	
	output.write("@data\n")

	for filename in males:
		if filename.endswith(".MP3"):
			sampFred, data = wavfile.read('AudioRecordings/Male/' + filename);
			cepstrum = getCepstrum(data)
			for i in range(0, 10):
				output.write(cepstrum[i])
				output.write(", ")
			output.write("male")

	output.write("\n")
	for filename in females:
		if filename.endswith(".MP3"):
			sampFred, data = wavfile.read('AudioRecordings/Female/' + filename);
			cepstrum = getCepstrum(data)
			for i in range(0, 10):
				output.write(cepstrum[i])
				output.write(", ")
			output.write("female")

def getCepstrum(input):
    return np.abs(np.fft.ifft((np.log((np.abs(np.fft.fft(input)))*(np.abs(np.fft.fft(input)))))))*np.abs(np.fft.ifft((np.log((np.abs(np.fft.fft(input)))*(np.abs(np.fft.fft(input)))))))

if __name__ == "__main__":
    run()