import os
import numpy as np
from scipy.io import wavfile
import operator
import sys
from features import mfcc

debugging = True
outputFilename = "test10.arff"


########################
# HIGH-LEVEL FUNCTIONS
########################

def run():

	info("Creating file " + outputFilename + "...")

	output = open(outputFilename, 'w')

	features = [
		("coefficient1", "Continuous"),
		("coefficient2", "Continuous"),
		("coefficient3", "Continuous"),
		("coefficient4", "Continuous"),
		("coefficient5", "Continuous"),
		("coefficient6", "Continuous"),
		("coefficient7", "Continuous"),
		("coefficient8", "Continuous"),
		("coefficient9", "Continuous"),
		("coefficient10", "Continuous"),
		("gender", ["male", "female"])
	]
	writeArffAttributes(features, output)

	maleFilenames, femaleFilenames = getAudioFiles()
	info("Found " +
	     str(len(maleFilenames)) + " male recordings and " +
	     str(len(femaleFilenames)) + " female recordings.")

	info("Generating features...")
	data = generateFeatureData(maleFilenames, femaleFilenames)
	writeArffData(data, output)

	info("Done.")

def generateFeatureData(maleFilenames, femaleFilenames):
	data = []
	for filename in maleFilenames:
		features = generateFeatures(filename, "male")
		data.append(features)
	for filename in femaleFilenames:
		features = generateFeatures(filename, "female")
		data.append(features)
	return data


####################
# AUDIO PROCESSING
####################

def generateFeatures(filename, outputClass):
	instance = []

	# Read the audio file.
	sampFreq, data = wavfile.read(filename)

	# Compute cepstral coefficients for each window
	mfcc_feat = mfcc(data, samplerate=sampFreq, numcep=10)
	# Compute mean vector from ceptral coefficients
	mean_vector = mfcc_feat.mean(axis=0)
	for i in range(0, len(mean_vector)):
		instance.append(str(mean_vector[i]))

	# Add the output class too.
	instance.append(outputClass)

	return instance

########################
# ARFF FILE GENERATION
########################

def writeArffAttributes(features, output):
	output.write("@relation voiceCepstrums\n\n")
	for feature in features:
		key = feature[0]
		value = feature[1]
		if type(value) == list:
			output.write("@attribute " + key + " {" + ", ".join(value) + "}\n")
		else:
			output.write("@attribute " + key + " " + value + "\n")
	output.write("\n")

def writeArffData(data, output):
	output.write("@data\n")
	for instance in data:
		first = True
		for feature in instance:
			if not first:
				output.write(", ")
			output.write(str(feature))
			first = False
		output.write("\n")


##############
# FILESYSTEM
##############

def getAudioFiles():
	files = []
	for f in os.walk("AudioRecordings"):
		files.append(f)
	femaleFilenames = prepareAudioFilenames(files[1][2], "AudioRecordings/Female/")
	maleFilenames = prepareAudioFilenames(files[2][2], "AudioRecordings/Male/")
	return maleFilenames, femaleFilenames

def prepareAudioFilenames(filenames, prefix):
	filtered = filter(lambda filename: filename.endswith(".wav") or filename.endswith(".WAV"), filenames)
	return map(lambda filename: prefix+filename, filtered)


##############
# UTILITIES
##############

def info(message):
	print message

def debug(message):
	if debugging:
		print message


########
# MAIN
########

if __name__ == "__main__":
    run()
