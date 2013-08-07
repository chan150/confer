import sys, os, json, csv, re, difflib
p = os.path.abspath(os.path.dirname(__file__) + '/../../data/kdd2013')

papers = {}
sessions = {}
schedule = []

days = {}


abstract = '''
The annual ACM SIGKDD conference is the premier international forum for data mining and big data researchers and practitioners from academia, industry, and government to share their ideas, research results and experiences. KDD-2013 will feature keynote presentations, oral paper presentations, poster sessions, workshops, tutorials, panels, exhibits, demonstrations, and the KDD Cup competition.
'''


def get_class(t):
	v =  int(re.match(r'\d+', t).group())
	if(v < 12 and v > 9):
		return 'morning'
	elif(v<5):
		return 'afternoon'
	else:
		return 'evening'


def load_files():
	data = open(p+'/papers.txt').read()
	rows = re.split(r'\n\n', data)
	for row in rows:
		try:
			details = re.split(r'\n', row)
			authors = [{'name':author[:author.index(',')], 'affiliation': author[author.index(',')+1:]} for author in re.split(r';', details[2][9:])]
			papers[details[0][10:]] = {'title':details[1][7:], 'authors': authors, 'abstract':abstract}
		except:
			pass
	data = open(p+'/sessions.txt').read()
	rows = re.split(r'\n\n', data)
	for row in rows:
		try:
			details = re.split(r'\n', row)
			sessions[details[0][9:]] = {'s_title':details[1][7:], 'submissions':[d[10:] for d in details[2:]]}
		except:
			pass
	data = open(p+'/program.txt').read()
	rows = re.split(r'\n\n', data)
	days = {}
	day_time = {}
	for row in rows:
		try:
			details = re.split(r'\n', row)
			if(details[0][6:].strip() in days):
				if(details[1][6:].strip() in days[details[0][6:].strip()]):
					days[details[0][6:].strip()][details[1][6:].strip()].append({'session': details[2][9:], 'room': details[3][6:]})
				else:
					day_time[details[0][6:].strip()].append(details[1][6:].strip())
					days[details[0][6:].strip()][details[1][6:].strip()] = [{'session': details[2][9:], 'room': details[3][6:]}]
			else:
				d = details[0][6:].strip()
				schedule.append({'id': d, 'day': d[0: d.index('-')].title(), 'date': d[d.index('-')+2:]})
				days[details[0][6:].strip()] = {}
				day_time[details[0][6:].strip()] = [details[1][6:].strip()]

				days[details[0][6:].strip()][details[1][6:].strip()] = [{'session': details[2][9:], 'room': details[3][6:]}]

		except:
			pass
	for s in schedule:
		t = days[s['id']]
		s['slots'] = [{'time':k, 'sessions': t[k], 'slot_class':get_class(k)} for k in day_time[s['id']]]
		del s['id']

	print schedule
	

def prepare_paper_and_schedule_json():
	load_files()
	p = open('data/kdd2013/papers.json','w')
	p.write(json.dumps(papers))
	p = open('server/static/conf/kdd2013/data/papers.json','w')
	p.write('entities='+json.dumps(papers))
	p = open('server/static/conf/kdd2013/data/sessions.json','w')
	p.write('sessions='+json.dumps(sessions))
	p = open('server/static/conf/kdd2013/data/schedule.json','w')
	p.write('schedule='+json.dumps(schedule))


def main():
	prepare_paper_and_schedule_json()
       

if __name__ == "__main__":
        main()
