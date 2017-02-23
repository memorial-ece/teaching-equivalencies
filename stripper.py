def hollahollagetdolla():
	file = open('2011-12/9.2 Engineering One Courses.html')
	lines = file.readlines()
	course = re.findall(r'<p class="courseNumber">(.*?)</p>', str(lines))
	courses = str(course)
	print courses.strip()
	james = open('parser.txt', 'w')
	james.write(courses)
	james.close()