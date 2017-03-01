#!/usr/bin/env python

import argparse
import calendar as cal
import collections
import sys
import csv
import re
from ConvertParse import *
reload(sys)
sys.setdefaultencoding('utf-8')

args = argparse.ArgumentParser()
args.add_argument('filename', nargs = '+')
args.add_argument('--format', choices = [ 'calendar', 'dot' ], default = 'dot')
args.add_argument('-o', '--output', default = '-')

args = args.parse_args()
output = sys.stdout if args.output == '-' else open(args.output, 'w')


courses = collections.defaultdict(dict)
dict_course= collections.defaultdict(dict)
dict_year=collections.defaultdict(dict)
dict_gen=collections.defaultdict(dict)
crn=0
count=(-1)
p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
p2 = re.compile(r"((filen1[count])+......\w)")
filen1 = (p1.findall(str(args.filename)))
for x1 in filen1:
	x1=int(x1)
	x2=x1
	if x1!=2008:
		x2=x1-1
	print x2
	# print x
	for filename in args.filename:
		p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
		filen2 = ''.join(p1.findall(str(filename)))
		filen2= int(filen2)
		if filen2==x1:
			f = open(filename)
			html = filename.endswith('.htm') or filename.endswith('.html')
			parse = cal.parseHTML if html else cal.parseText
			for (name,c) in parse(open(filename), prefix='ENGI').items():
				crn += 1
				b = str(crn)
				# print b
				check=obscure_refference(name,c)
				dict_course[crn].update(obscure_refference(name, c))
				dict_year[x1].update(dict_course)
				# print dict_year[x1][crn]["Title"]
				print crn
				print dict_year[x2][crn]["Title"]
				print dict_year[x1][crn]["Title"]

# print dict_year['2009'][1]['Title']