import sys
import argparse
import logging
import codecs
import os
import urllib2
import json
import time
from operator import itemgetter
from datetime import datetime

api_url="https://ello.co/api/v1/availability/username?value="
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
secs_to_pause_between_api_calls=10
output_sep="\t"


def main():
	parser = argparse.ArgumentParser(description='Simple python script that checks if your preferred usernames are available @ Ello.co')
	parser.add_argument('-i', action='store', dest='input_file', help='input file with one username per line (e.g. usernames.txt)', required=True)
	parser.add_argument('-o', action='store', dest='output_file', help='output file (e.g. available.txt)', required=True)
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	args = parser.parse_args()

	# print ello logo
	indent="           "
	print("")
	print(indent+"          MMMMMMMMM")
	print(indent+"       MMMMMMMMMMMMMMM")
	print(indent+"     MMMMMMMMMMMMMMMMMMM")
	print(indent+"   MMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+"  MMMMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+" NMMMMMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+" MMMMMMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+"MMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+"MMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+"MMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
	print(indent+"NMMMMM  MMMMMMMMMMMMM..MMMMMM")
	print(indent+" MMMMMM. MMMMMMMMMMM. MMMMMM")
	print(indent+" MMMMMMM..MMMMMMMMM. MMMMMMM")
	print(indent+"  MMMMMMMM          MMMMMMM")
	print(indent+"   MMMMMMMMMMMDMMMMMMMMMMM")
	print(indent+"    MMMMMMMMMMMMMMMMMMMN")
	print(indent+"     MMMMMMMMMMMMMMMMMMN")
	print(indent+"          MMMMMMMMM" )
	print(indent+"             MM")
	print("")
	print("  simple python script that checks if your preferred") 
	print("           usernames are available @ ello.co")
	print("                    version: 1.0")
	print("----------------------------------------------------")
	print("")
	# Initialize default logging behaviour
	logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)-6s %(message)s',datefmt="%H:%M:%S")

    # Attempt to open input file with preferred usernames
	logging.info("opening " + args.input_file +" for reading")
	try:
		usernames = codecs.open(args.input_file, 'r', 'utf8')
	except Exception as e:
		logging.error("Failed to open file " + args.input_file + " Error: " + str(e.args) )
		sys.exit(1)
	# Attempt to open output file for available usernames
	logging.info("opening "+args.output_file +" for writing")
	print("")
	try:
		output_file = codecs.open(args.output_file, 'w', 'utf8')
	except Exception as e:
		logging.error("Failed to open output file " + args.output_file + "Error: " + str(e.args))
		sys.exit(1)

	for username in usernames:
		username = username.rstrip()
		if not username:
			continue
		logging.info("querying .. "+ str(username))
		try:
			result=urllib2.urlopen(urllib2.Request(api_url + str(username), headers=hdr)).read()[13:-1]
			if result=="true":
				logging.info('\033[92m' + "  :-)        " + u'\u2713' + " " + u'\u2713' + '\033[0m')
				output_file.write(str(username) + '\n')
			else:
				logging.info('\033[93m' + "  :'-(       " + "x" + '\033[0m')
		except:
			logging.error("failed to contact ello.co api :-(")
		time.sleep(secs_to_pause_between_api_calls)
	output_file.close()
	print "done."
        print ""
if __name__ == '__main__':
    main()
