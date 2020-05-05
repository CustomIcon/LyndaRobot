#!/usr/bin/env python
# spongemock __main__.py
# author: Noah Krim
# email: nkrim62@gmail.com

from __future__ import print_function

import argparse
import re
from pyperclip import copy
import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main():
	parser = init_parser()
	args = parser.parse_args()
	try:
		out = mock(' '.join(args.text), args.bias, args.seed or args.strseed or None)
	except Exception as e:
		eprint('Error: '+sys.argv[0]+': '+str(e))
		return 1
	if args.copy:
		try:
			copy(out)
		except Exception:
			eprint('Warning: '+sys.argv[0]+': could not copy the output to the clipboard because of an unexpected error. '
				+'If using Linux, pleaes make sure you have all the proper modules installed for pyperclip '
				+'(more info: https://tkinter.unpythonic.net/wiki/How_to_install_Tkinter).')
	print(out)
	return 0

def init_parser():
	parser = argparse.ArgumentParser(description='Mock some text like spongebob would. mOCk SoMe TexT lIKe SpONGebOb wOuLd.')
	parser.add_argument('text', nargs='+', help='the text to mock. ThE tExT tO mOCk.')
	parser.add_argument('-c', '--copy', action='store_true', help='Mocked text will be copied to the clipboard.')
	parser.add_argument('-b', '--bias', type=float, default=0.5, 
		help='This bias is used to succesively increase the chance of swapping from the previously-mocked case. '
			+'A value of `0` will ensure the chance is always 50/50, '
			+'and a value of `1` will ensure that after the first random choice the capitalization perfectly oscilates. '
			+'Default is `0.5`.')
	seed_group = parser.add_mutually_exclusive_group()
	seed_group.add_argument('-s', '--seed', type=parsable_seed, help='Seed for random number generator. Can be any number or string (numbers are parsed).')
	seed_group.add_argument('-S', '--strseed', help='Seed for random number generator. Does not attempt to parse the string to a number.')
	return parser

def parsable_seed(str_seed):
	# Try int parse
	if re.match(r'^-?\d+$', str_seed):
		return int(float(str_seed))
	# Try float parse
	try:
		return float(str_seed)
	except Exception:
		pass
	return str_seed

if __name__ == '__main__':
	if __package__ is None:
		from os import path
		sys.path.append( path.dirname(path.abspath(__file__) ) )
		from spongemock import mock
	else:
		from .spongemock import mock
	main()
else:
	from .spongemock import mock 