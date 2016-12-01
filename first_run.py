#!/usr/bin/env python
def main():
	import optparse
	import vocabulary
	import os
	parser = optparse.OptionParser()
	parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
	parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.5)
	parser.add_option("-k", dest="numberOfTopics", type="int", help="number of topics", default=20)
	parser.add_option("-i", dest="numberOfiteration", type="int", help="iteration count", default=100)
	(options,command_arguments)=parser.parse_args()
	dataFile_dir="/home/rooney/dataMiningPackage/DATASET"
	dataFiles=os.listdir(dataFile_dir)
	#for file in dataFiles:
	#	print file
	#definedTopics=[];
	print(len(dataFiles))



if __name__ == "__main__": 
    main()