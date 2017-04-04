#!/usr/bin/python
#  Copyright 2017 Keegan Joseph Brophy
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Usage:
	Startup.py execute (FUNCTION) [ARGS]
	Startup.py intake (<FILE>)...
	Startup.py populate (<FILE>)...
	Startup.py -h --help

Options:
	execute (docustomexport)[Table] Any table form class.py
	execute (docustomimport)[Table]	Any table form class.py
	populate [file location] gen all data from offerings folder program will crash if the year exceeds 2030
	execute (peeweetable)[DropType] droptypes are 'DropReCreate' 'Drop' 'Create' shortcuts 'pt', 'drc' , 'd' , 'c'

"""
import docopt
from Core import *
from import_courses import *


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	try:
		function = (arguments['FUNCTION'])
		arg = str(arguments['ARGS'])
		filename = arguments['<FILE>']
		if function=='pt':
			if arg=='d':
				arg='Drop'
			if arg=='c':
				arg='Create'
			if arg=='drc':
				arg='DropReCreate'
			peeweetable(arg)
		if function == 'docustomexport':
			docustomexport(arg)
		if function == 'docustomimport':
			docustomimport(arg)
		if function == 'peeweetable':
			if arg=='d':
				arg='Drop'
			if arg=='c':
				arg='Create'
			if arg=='drc':
				arg='DropReCreate'
			peeweetable(arg)
		# if function == 'test1':
		# if function == 'test2':
		# if function == 'test3':
		if arguments['populate']==True:
			populate(filename)
		if arguments['intake']==True:
			import_courses(filename)

	except docopt.DocoptExit as e:
		print e.message