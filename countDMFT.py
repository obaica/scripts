#!/usr/bin/env python

import sys,os
import argparse

def count_complete(args):
	"""
	This methods checks to see if the DMFT calculation is done
	by checking if "Done" is printed in INFO_TIME
	"""

	done_counter = 0

	#pathlist = os.listdir(args.path) 
	pathlist = sorted([int(d) for d in os.listdir(args.path) if os.path.isdir(d)])
	print(pathlist)

	for path in pathlist:

		pathstr = str(path)+os.sep+args.type+os.sep+'INFO_TIME'

		if os.path.exists(pathstr):
			fi=open(pathstr,'r')
			done_word=fi.readlines()[-1]
			fi.close()

			if done_word.split()[0] == 'Calculation':
				done_counter += 1
				print('Calculation complete at %s' %path)


			else:
				print('Calculation incomplete at %s' %path)


		else:
			print('INFO_TIME does not exist at %s' %path)

	
	print('%d DMFT calculations have been completed.'%done_counter)			

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This script checks to see if the DMFT calculation is complete.')
	parser.add_argument('path', type=str,default='./', help='Path to DMFT directory')
	parser.add_argument('-type',type=str,default='dmft',help='DMFT or HF',choices=['DMFT','HF'])
	args = parser.parse_args()
	count_complete(args)

		
