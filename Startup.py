#! /usr/bin/python
# Copyright 2017 Keegan Joseph Brophy
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
	Startup.py (FUNC) [ARGS]
	Startup.py -h --help

Options:
	(docustomexport)[Table] 	Any table form class.py
	(docustomimport)[Table]	Any table form class.py
	(error)[]	no args aditional used for helping humans check values of generation tables.
	(offergen)[year] gen all data from offerings folder year years piror to 2020 please
	(peeweetable)[DropType] droptypes are 'DropReCreate' 'Drop' 'Create'
"""
from docopt import docopt
from orginization_functions import *


if __name__ == '__main__':
	arguments = docopt(__doc__)
	try:
		function = (arguments['FUNC'])
		arg = str(arguments['ARGS'])
		if function == 'docustomexport':
			docustomexport(arg)
		if function == 'docustomimport':
			docustomimport(arg)
		if function == 'error':
			error()
		if function == 'offergen':
			offergen(arg)
		if function == 'peeweetable':
			peeweetable(arg)


	except docopt.DocoptExit as e:
		print 'lol'
		print e.message


