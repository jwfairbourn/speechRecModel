import argparse
import os
import numpy as np
from scipy.io import wavfile
import operator
import sys
from features import mfcc
import matplotlib.pyplot as plt

debugging = True
DEFAULT_COEFFICIENTS = 10


########################
# HIGH-LEVEL FUNCTIONS
########################

def run(coefficients, outputFilename, graphFilename):

	info("Creating file " + outputFilename + "...")

	output = open(outputFilename, 'w')

	features = generateAttributes(coefficients)
	writeArffAttributes(features, output)

	maleFilenames, femaleFilenames = getAudioFiles()
	info("Found " +
	     str(len(maleFilenames)) + " male recordings and " +
	     str(len(femaleFilenames)) + " female recordings.")

	info("Generating features...")
	data = generateFeatureData(maleFilenames, femaleFilenames, coefficients)
	writeArffData(data, output)
	if graphFilename is not None:
		# createGraph(data, graphFilename)
		createAverageGraph(data, graphFilename)

	info("Done.")

def generateAttributes(coefficients):
	features = []
	for i in range(coefficients):
		n = i + 1
		feature = ("coefficient" + str(n), "real")
		features.append(feature)
	features.append( ("gender", ["male", "female"]) )
	return features

def generateFeatureData(maleFilenames, femaleFilenames, coefficients):
	data = []
	for filename in maleFilenames:
		features = generateFeatures(filename, "male", coefficients)
		data.append(features)
	for filename in femaleFilenames:
		features = generateFeatures(filename, "female", coefficients)
		data.append(features)
	return data


####################
# AUDIO PROCESSING
####################

def generateFeatures(filename, outputClass, coefficients):
	instance = []

	# Read the audio file.
	sampFreq, data = wavfile.read(filename)

	# Compute cepstral coefficients for each window
	mfcc_feat = mfcc(data, samplerate=sampFreq, numcep=coefficients)
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
			output.write("@ATTRIBUTE " + key + " {" + ",".join(value) + "}\n")
		else:
			output.write("@ATTRIBUTE " + key + " " + value + "\n")
	output.write("\n")

def writeArffData(data, output):
	output.write("@DATA\n")
	for instance in data:
		first = True
		for feature in instance:
			if not first:
				output.write(",")
			output.write(str(feature))
			first = False
		output.write("\n")

####################
# GRAPH GENERATION
####################
def createGraph(data, graphFilename):
	coefficientIds = range(len(data[0])-1)
	maleX = []
	maleY = []
	femaleX = []
	femaleY = []
	for instance in data:
		numCoefficients = len(instance)-1
		for coefficient in range(0, numCoefficients):
			if instance[len(instance)-1] == 'male':
				maleX.append(coefficient)
				maleY.append(float(instance[coefficient]))
			else:
				femaleX.append(coefficient+.2)
				femaleY.append(float(instance[coefficient]))
	plt.figure()
	plt.xlim(0, coefficientIds[len(coefficientIds)-1])
	plt.scatter(maleX, maleY, color="blue")
	plt.scatter(femaleX, femaleY, color="red")
	plt.savefig(graphFilename)

def createAverageGraph(data, graphFilename):
	maleData = filter(lambda instance: instance[len(instance)-1] == 'male', data)
	femaleData = filter(lambda instance: instance[len(instance)-1] == 'female', data)
	coefficientIds = range(len(data[0])-1)
	maleAverages = generateAverages(maleData)
	femaleAverages = generateAverages(femaleData)
	plt.figure()
	plt.xlim(0, coefficientIds[len(coefficientIds)-1])
	plt.scatter(coefficientIds, maleAverages, color="blue")
	plt.scatter(coefficientIds, femaleAverages, color="red")
	plt.savefig(graphFilename)


def generateAverages(instances):
	numCoefficients = len(instances[0])-1
	sums = np.zeros(numCoefficients, dtype="float32")
	for instance in instances:
		for coefficient in range(0, numCoefficients):
			sums[coefficient] += float(instance[coefficient])
	sums /= len(instances)
	return sums

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
	parser = argparse.ArgumentParser(prog='Feature Generator', description='CS478 Group Project: Speaker gender prediction based on a short phrase', add_help=True)
	parser.add_argument('-c', '--coefficients', type=int, action='store', help='The number of Cepstrum coefficients to generate', default=DEFAULT_COEFFICIENTS)
	parser.add_argument('output', metavar="output", type=str, action='store', help='The ARFF file to save to')
	parser.add_argument('-g', '--graph', type=str, action='store', help='The filename to save a graph to', default=None)

	args = parser.parse_args()
	coefficients = args.coefficients
	outputFilename = args.output
	graphFilename = args.graph

	run(coefficients, outputFilename, graphFilename)
