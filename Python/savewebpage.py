import urllib2
def save():
	year=0
	bear=1
	for x in range(0,10):
		year+=01
		bear+=01
		ear=str(year)
		bea=str(bear)
		page=0037
		for x in range (0,8):
			page+=1
			age= str(page)
			url = 'http://www.mun.ca/regoff/calendar/201'+ear+'_201'+bea+'/sectionNo=ENGI-'+age
			response = urllib2.urlopen(url)
			webContent = response.read()
			f = open(ear+'.'+age+' Engineering One Courses.html', 'w')
			f.write(webContent)
			f.close