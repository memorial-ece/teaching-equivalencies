#!/usr/bin/env python

import argparse
import calendar as cal
import collections
import sys
import csv
import re
from operator import *
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
dict_rando= collections.defaultdict(dict)
dict_year=collections.defaultdict(dict)
dict_gen=collections.defaultdict(dict)
dict_view_gen=collections.defaultdict(dict)

count=(-1)
p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
p2 = re.compile(r"((filen1[count])+......\w)")
filen1 = (p1.findall(str(args.filename)))
for x1 in filen1:
	x1=int(x1)
	if x1!=2008:
		x2=x1-1

	for filename in args.filename:
		p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
		filen2 = ''.join(p1.findall(str(filename)))
		filen2= int(filen2)
		if filen2==x1:
			f = open(filename)
			html = filename.endswith('.htm') or filename.endswith('.html')
			parse = cal.parseHTML if html else cal.parseText
			for (name,c) in parse(open(filename), prefix='ENGI').items():
				code=convert_parse_course_id(name,c)
				check=obscure_refference(name,c)
				dict_course[code].update(check)
				# print code
				# print dict_year[x1]!=dict_year[x2]

					# print dict_year[x1]
					# print dict_year[x2]
				# print dict_course
	dict_year[x1].update(dict_course)

for year,course in dict_year.items():
	span=year
	list_keys_year=dict_year[year].keys()
	if dict_gen==collections.defaultdict(dict):
		for i in range(len(list_keys_year)):
			dict_gen[list_keys_year[i]]=course[list_keys_year[i]]
	list_gen=dict_gen.keys()
	for c in list_keys_year:
		if c not in list_gen:
			dict_gen[c]=course[c]
		if c in list_gen:
			if dict_gen[c]!=(course[c]):
				dict_gen[c]=course[c]
	for c in list_gen:
		if c not in list_keys_year:
			dict_gen.pop(c)
	dict_view_gen[year]=dict_gen