import sys, json, csv, re, time

papers = {}
sessions = {}
schedule = []


def construct_id(s):
  return re.sub(r'\W+', '_', s)

def get_start_time (s_time):
  return int(re.match(r'\d+', s_time).group())

def get_date_time(s_date):
  dt = time.strptime(s_date, '%d-%m-%Y')
  return dt

def get_class(s_time):
  v =  get_start_time(s_time)
  if(v < 10 and v >= 7):
    return 'morning1'
  elif(v >= 8 and v < 12):
    return 'morning2'
  elif(v >= 12 and v < 15):
    return 'afternoon1'
  elif(v >= 15 and v < 18):
    return 'afternoon2'
  else:
    return 'evening'

def prepare_schedule (t_schedule):
  # sort schedule data
  for s_date in t_schedule:
    t_schedule[s_date] = sorted(
      t_schedule[s_date].items(), key = lambda x: get_start_time(x[0]))

  t_schedule = sorted(t_schedule.items(), key=lambda x: time.mktime(get_date_time(x[0])))
  for day_schedule in t_schedule:
    slots = []
    print day_schedule
    s_date = day_schedule[0]
    all_slots = day_schedule[1]
    for slot_info in all_slots:
      slot_time = slot_info[0]
      slot_sessions = slot_info[1]['sessions']
      slots.append({
        'time': slot_time,
        'sessions': slot_sessions,
        'slot_class': get_class(slot_time),
        'slot_id': construct_id(s_date + slot_time)
      })
    schedule.append({'date': s_date, 'slots': slots, 'day': s_date})

def prepare_data(data_file):
  f = open(data_file, 'rU')
  reader = csv.reader(f)
  reader.next()
  p_id = 1
  t_schedule = {}
  for row in reader:
    paper_id = 'paper_%s' %(p_id)
    s_date = unicode(row[0], "ISO-8859-1")
    s_time = unicode(row[1], "ISO-8859-1")
    paper_type = unicode(row[2], "ISO-8859-1")
    session = unicode(row[3], "ISO-8859-1")
    paper_title = unicode(row[4], "ISO-8859-1")
    paper_authors = unicode(row[5], "ISO-8859-1")
    paper_abstract = unicode(row[6], "ISO-8859-1")

    # prepare papers data
    papers[paper_id] = {
        'title': paper_title,
        'authors': [{'name': name.strip()}
            for name in paper_authors.strip('"').split(',')],
        'abstract': paper_abstract}
    
    # prepare sessions data
    s_id = construct_id(session)
    if(s_id in sessions):
      sessions[s_id]['submissions'].append(paper_id)
    else:
      sessions[s_id] = {
          'submissions': [paper_id], 's_title': session, 'room': 'TBD', 'time': s_time, 'date': s_date}

    p_id += 1


  # prepare schedule data
  for session in sessions:
    s_info = sessions[session]
    s_date = s_info['date']
    s_time = s_info['time']
    s_data = {'session': session, 'room': s_info['room']}
    if s_date in t_schedule:
      if s_time in t_schedule[s_date]:
        t_schedule[s_date][s_time]['sessions'].append(s_data)
      else:
        t_schedule[s_date][s_time] = {'time': s_time, 'sessions':[s_data] }
    else:
      t_schedule[s_date] =  {s_time: {'time': s_time, 'sessions':[s_data]}}

  print t_schedule
  prepare_schedule(t_schedule)


def main():
  conf = sys.argv[2]
  data_file = sys.argv[1]
  prepare_data (data_file)
  # write files
  p = open('data/' + conf + '/papers.json','w')
  p.write(json.dumps(papers, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf + '/data/papers.json','w')
  p.write('entities='+json.dumps(papers, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf + '/data/sessions.json','w')
  p.write('sessions='+json.dumps(sessions, indent=2, sort_keys=True))
  p = open('server/static/conf/' + conf +'/data/schedule.json','w')
  p.write('schedule='+json.dumps(schedule, indent=2, sort_keys=True))
  

if __name__ == "__main__":
  main()