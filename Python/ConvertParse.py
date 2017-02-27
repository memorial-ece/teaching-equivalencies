def convert_parse_labs(name,course):
	labs = course['lab hours'] if 'lab hours' in course else 0
	if labs == 'at least 9 hours per semester':
		labs = 9
	if labs == 'at least 12 hours per semester':
		labs = 12
	if labs == 'at least ten 2-hour sessions per semester':
		labs = 20
	if labs == 'at least five 3-hour sessions per semester':
		labs = 15
	if labs == 'at least three 1-hour sessions per semester':
		labs = 3
	if labs == 'at least one 4-hour session per semester':
		labs = 4
	if labs == 'at least four 2-hour sessions per semester':
		labs = 8
	if labs == 'at least eight 1-hour sessions per semester':
		labs = 8
	if labs == 'at least four 3-hour sessions per semester':
		labs = 12
	if labs == 'at least ten 3-hour sessions per semester':
		labs = 30
	if labs == 'at least three 3-hour sessions per semester':
		labs = 9
	if labs == 'at least six 3-hour laboratory sessions per semester':
		labs = 18
	if labs == 'at least four 3-hour sessions per term':
		labs = 12
	if labs == 'at least nine 2-hour sessions per semester':
		labs = 18
	if labs == 'at least eight 3-hour sessions per semester':
		labs = 24
	if labs == 'at least eight 2-hour sessions per semester':
		labs = 16
	if labs == 'at least one 3-hour session per semester':
		labs = 3
	if labs == 'at least 6 hours per semester':
		labs = 6
	if labs == 'at least two 2-hour sessions per semester':
		labs = 4
	if labs == 'at least six 3-hour sessions per semester':
		labs = 18
	if labs == 'at least four 1-hour sessions per semester':
		labs = 4
	if labs == 'scheduled as required':
		labs = 3
	if labs == 'at least four 3-hour sessions per semester.':
		labs = 12
	if labs == 'at least five 1-hour sessions per semester':
		labs = 5
	if labs == 'at least ten 3-hour lab sessions per semester':
		labs = 10
	if labs == 'at least 20 hours per semester':
		labs = 20
	if labs == 'at least nine 3-hour sessions per semester':
		labs = 27
	if labs == 'at least three 1.5-hour sessions per semester':
		labs = 4.5
	if labs == 'at least nine 3-hour laboratory sessions per semester':
		labs = 27
	if labs == 'five 3-hour sessions per semester':
		labs = 15
	if labs == 'at least seven 2-hour sessions per semester':
		labs = 14
	if labs == 'at least six 2-hour sessions per semester':
		labs = 6
	if labs == 'at least 4 three-hour sessions per semester':
		labs = 12
	if labs == 'at least two 3-hour sessions per semester':
		labs = 6
	labs1=str(labs)
	return labs1

def convert_parse_credit_hours(name,course):
	credit_hours = course['credit-hours'] if 'credit-hours' in course else 0
	credit_hours1=str(credit_hours)
	return credit_hours1

def convert_parse_lecture_hours(name, course):
	lecture_hours = course['lecture hours'] if 'lecture hours' in course else 0
	if lecture_hours == 'at least 10 lecture hours per semester':
		lecture_hours = 10
	if lecture_hours == 'at least 15 lecture hours per semester':
		lecture_hours = 15
	if lecture_hours == 'scheduled as required':
		lecture_hours = 3
	if lecture_hours == 'at least 25 lecture hours per semester':
		lecture_hours = 25
	lecture_hours1=str(lecture_hours)
	return lecture_hours1
def convert_parse_title(name, course):
	title = course['title'] if 'title' in course else None
	return title
def convert_parse_comments(name, course):
	comments = course['description'] if 'description' in course else None
	return comments
def convert_parse_course_id(name, course):
	course_id = course['number'] if 'number' in course else None
	course_id1=str(course_id)
	return course_id1
