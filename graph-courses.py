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


courses = collections.defaultdict(list)
dict_course= collections.defaultdict(dict)
dict_gen=collections.defaultdict(dict)
dict_view_gen=collections.defaultdict(dict)

for filename in args.filename:
	p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
	filen2 = ''.join(p1.findall(str(filename)))
	html = filename.endswith('.htm') or filename.endswith('.html')
	parse = cal.parseHTML if html else cal.parseText
	for (name,c) in parse(open(filename)).items():
		codex=convert_parse_course_id(name,c)
		course=obscure_refference(name,c)
		courses[filen2].append(course)
		# print courses.items()

for year, cour in courses.items():
	dict_year = collections.defaultdict(dict)
	for course in cour:
		a=courses[year].index(course)
		code=course['name']
		dict_year[year]=courses[year][a]
		# print dict_year
		dict_course[code]=dict_year
		# print courses[year][a]
		print dict_year.items()
		dict_course[code]=dict_year.items()
		# print dict_course.items()

		# if code!=
# print dict_course.keys()












# for name,ye_de in dict_course.items():
# 	print dict_course
	# year=sorted(ye_de.items())
	# decs=dict_course[name].values()
	# print decs
	# a=-1
	# for i in range(len(decs)):
	# 	a=i+1
	# 	try:
	# 		if decs[i]==decs[a]:
	# 			print decs[i]
	# 			dict_gen[i]=decs[i]
	# 			print dict_gen
	#
	# 	except:
	# 		pass










		# compare=decs[i]
		# try:
		# 	i+=1
		# 	if compare==decs[i]:
		# 		print name
		# 		print decs
		# except:
		# 	print 'll'
	# print year_and_description
	# for i in range(len(compare)):
	# 	# print 'lol'
	# 	print
	# if dict_gen==collections.defaultdict(dict):
	# 	for i in range(len(compare)):
	# 		if dict_gen.values()!=compare:
	# 			pass
	# 		dict_gen[name]=compare[i]
	#
	# list_gen=dict_gen.keys()
	# print list_gen
	# for c in list_keys_year:
	# 	if c not in list_gen:
	# 		dict_gen[c]=course[c]
	# 	if c in list_gen:
	# 		if dict_gen[c]!=(course[c]):
	# 			dict_gen[c]=course[c]
	# for c in list_gen:
	# 	if c not in list_keys_year:
	# 		dict_gen.pop(c)
	# dict_view_gen[year]=dict_gen