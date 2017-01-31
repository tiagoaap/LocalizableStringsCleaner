import os;
import string;
import sys;
import subprocess;
import getopt;
import re;

search_types = "{h,m,mm,xml}"

def read_file(file_path):
	with open(file_path, "r") as ins:
		array = []
		for line in ins:
			res = re.search("\"(.*)?\"", line.split(" ")[0])
			if res:
				array.append(clear_null_bytes(res.group(1)))			

		return array


def find_string_in_directory(locKey, directory):
	cmd = r"grep --include=\*." + search_types + " -rnw \'" + directory + "\' -e " + locKey
	print "Running " + cmd

	result_value = sys.maxint
	
	try:
		result_value = os.system(cmd)
	except Exception as e:
		print "There was a problem trying to find " + locKey;
	
	if result_value > 0:
		with open("unused_strings.txt", "a") as myfile:
			myfile.write(locKey+"\n")

def clear_null_bytes(string):
	return string.replace('\0', '')

def main(argv):
	
	strings_file = ''
	search_directory = ''
	
	try:
		opts, args = getopt.getopt(argv,"hf:d:",["ffile=","ddir="])
	except getopt.GetoptError:
		print 'search_unused_strings.py -f <strings_file> -d <search_directory>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'search_unused_strings.py -f <strings_file> -d <search_directory>'
			sys.exit()
		elif opt in ("-f", "--ffile"):
			strings_file = arg
		elif opt in ("-d", "--ddir"):
			search_directory = arg
	
	locKeys = read_file(strings_file)

	for key in locKeys:
		print "Searching for localizable key "+key
		find_string_in_directory(key, search_directory)

if __name__ == "__main__":
    main(sys.argv[1:])
