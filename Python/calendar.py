from bs4 import BeautifulSoup
import re

course_number = re.compile('[0-9W]{4} [A-Z][a-z]+')
numeric = re.compile('^[0-9]+$')
special_topics = re.compile('[0-9]{4}-[0-9]{4} [A-Z][a-z]+')



def parse_prerequisites(s, prefix):
	prereqs = []

	for x in s.split(' or '):
		for y in x.split(','):
			y = y.strip()

			if y.startswith('permission of'):
				continue

			prereqs += [ prefix + ' ' + y if numeric.match(y) else y ]

	return prereqs


_ = lambda x, _ : x
codes = {
	'AR': ('attendance', _, _),
	'CH': ('credit-hours', lambda x, _ : int(x), _),
	'CO': ('co-requisite', _, _),
	'CR': ('exclusive with', _, _),
	'LC': ('lecture hours', _, _),
	'LH': ('lab hours', _, _),
	'OR': ('other information', _, _),
	'PR': ('prerequisites', parse_prerequisites, lambda xs: ', '.join(xs)),
	'UL': ('limitations', _, _),
}


def parseHTML(calfile, prefix = 'ENGI'):
	courses = {}
	soup = BeautifulSoup(calfile, 'html.parser')
	for block in soup.find_all(class_ = 'CourseBlock'):
		for c in block.find_all(class_ = 'course'):
			number = c.find(class_ = 'courseNumber').string.strip()
			name = '%s %s' % (prefix, number)
			title = c.find(class_ = 'courseTitle').string.strip()
			description = ''.join([
				d.string.strip()
					for d in c.find(class_ = 'courseDesc').p
					if d.string is not None
			])
			if 'inactive course' in description:
				continue
			course = {
				'credit-hours': 3,
				'description': description,
				'lecture hours': 3,
				'name': name,
				'number': number,
				'title': title,
			}
			courses[name] = course
			for attr in c.find_all(class_ = 'courseAttrs'):
				content = ' '.join([
					a.string.strip()
						for a in attr
						if a.string is not None
				])
				parts = content.split(':')
				key = parts[0]
				value = parts[-1].strip()

				(name,parse,reformat) = codes[key]
				course[name] = parse(value, prefix)
	return courses

def parseText(calfile, prefix = 'ENGI'):
	courses = {}
	for line in calfile:
		line = line.strip()
		if special_topics.match(line):
			continue
		if course_number.match(line):
			number = line.split()[0]
			name = '%s %s' % (prefix, number)
			course = {
				'credit-hours': 3,
				'description': line[5:].strip(),
				'lecture hours': 3,
				'name': name,
				'number': number,
			}
			courses[name] = course
		else:
			parts = line.split(':')
			if len(parts) < 2:
				raise ValueError("expected 'key: val', got '%s'" % line)
			key = parts[0]
			value = parts[-1].strip()
			(name,parse,reformat) = codes[key]
			course[name] = parse(value, prefix)
	return courses

def format(courses, output):
	for course in sorted(courses.values(), key = lambda c : c['number']):
		output.write('%d %s\n' % (course['number'], course['description']))

		for (code, (name,parse,reformat)) in sorted(codes.items()):
			if name in course:
				output.write('\t%s: %s\n' % (code, reformat(course[name])))

