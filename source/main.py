import sys
import io
import os
import network
import machine
import uasyncio
import time
import random
from machine import Pin, ADC, PWM

pck_sss=''
pck_stop=1
pck_tmax=10000
chart_value=0
item='item'

mainurl='https://www.tutorialrepublic.com/examples/html/hello.html'

class DUP(io.IOBase):

	def __init__(self):
		global pck_sss

	def write(self, data):
		global pck_sss
		global pck_tmax
		pck_sss += str(data,'utf-8')
		if len(pck_sss)>pck_tmax:
			pck_sss = pck_sss[len(pck_sss)-pck_tmax:len(pck_sss)]
		return len(data)

	def readinto(self, data):
		return 0
		
def eprint(ss):
	os.dupterm(None)
	print(ss)
	global pck_sss
	global pck_tmax
	pck_sss += str(ss)+"<br>"
	if len(pck_sss)>pck_tmax:
		pck_sss = pck_sss[len(pck_sss)-pck_tmax:len(pck_sss)]
	os.dupterm(DUP())


#### Parsing function
def qs_parse(qs):
 
	parameters = {}
	ampersandSplit = qs.split("&")
 
	for element in ampersandSplit:
		equalSplit = element.split("=")
		parameters[equalSplit[0]] = equalSplit[1]

	return parameters
 

_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a + b, chr(int(a + b, 16)))
                 for a in _hexdig for b in _hexdig)

def unquote(ss):
	"""unquote('abc%20def') -> 'abc def'."""
	for i in range(len(ss)):
		if ss[i:i+1] == '+':
			ss = ss[:i]+' '+ss[i+1:]
	res = ss.split('%')
	utf = 0
	hex1 = 0
	hex2 = 0
	# fastpath
	if len(res) == 1:
		return ss
	ss = res[0]
	for item in res[1:]:
		if utf == 2:
			hex2 = _hextochr[item[:2]]
			if (ord(hex1)*256)+ord(hex2) >= 47488:
				ss += chr((ord(hex1)*256)+ord(hex2)-43840) + item[2:]			
			else:
				ss += chr((ord(hex1)*256)+ord(hex2)-43648) + item[2:]
			utf = 0
			continue
		if utf == 1:
			hex1 = _hextochr[item[:2]]
			utf = 2
			continue
		if item[:2] == 'E0' or item[:2] == 'e0':
			utf = 1
			continue
		try:
			ss += _hextochr[item[:2]] + item[2:]
		except KeyError:
			ss += '%' + item
		except:
			ss += chr(int(item[:2], 16)) + item[2:]
	return ss

try:
	file = open("init.txt","r")
	text = file.read()
except:
	file = open("init.txt","w")
	text = ",,1"
	file.write(text)
file.close()
init_text = text.split(",")
t0 = time.time()
if (len(init_text)>=3):
	if (init_text[2]=="1"):
		station = network.WLAN(network.AP_IF)
		station.active(True)
		station.config(essid="ESP32Peacock",password="")
	else:
		station = network.WLAN(network.STA_IF)
		station.active(True)
		station.connect(init_text[0],init_text[1])
		while station.isconnected() == False:
			if ((time.time()-t0)>10):
				station.active(False)
				station = network.WLAN(network.AP_IF)
				station.active(True)
				station.config(essid="ESP32Peacock",password="")
				break
			pass
else:
	station = network.WLAN(network.AP_IF)
	station.active(True)
	station.config(essid="ESP32Peacock",password="")

print("hello")

import gc
gc.collect()

import picoweb

def push_count():
	i = 0
	global pck_stop
	global pck_sss
	while 1:
		if pck_stop == 0:
			os.dupterm(DUP())
			try: 
				execfile("test2.py")
			except Exception as exc:
				sys.print_exception(exc)
			os.dupterm(None)	
		await uasyncio.sleep(1)
 
app = picoweb.WebApp(__name__)
apin = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

@app.route("/pin")
def index(req, resp):
	queryString = req.qs
	tout = " "
	if len(queryString)>0:
		parameters = qs_parse(queryString)
		if len(parameters)>0:
			tpin = unquote(parameters["pin"])
			tstate = unquote(parameters["state"])
			if tstate == "s": # Return pin state when &state=s
				yield from picoweb.start_response(resp)
				yield from resp.awrite(str(apin[int(tpin)]))					
			else:
				tout = "Pin"+tpin+" : "+tstate
				print(tout+"<br>")
				ppin = Pin(int(tpin), Pin.OUT)
				ppin.value(int(tstate))
				apin[int(tpin)]=int(tstate)
				yield from picoweb.start_response(resp)
				yield from resp.awrite(tout)	
		else:
			yield from picoweb.start_response(resp)
			yield from resp.awrite(" ")	
	else:
		yield from picoweb.start_response(resp)
		yield from resp.awrite(" ")	
	

@app.route("/load1")
def index(req, resp):
	yield from picoweb.start_response(resp)
	try:
		file = open("test.py","r")
		yield from resp.awrite(file.read())
		file.close()
	except:
		yield from resp.awrite(" ")	

@app.route("/load2")
def index(req, resp):
	yield from picoweb.start_response(resp)
	try:
		file = open("test2.py","r")
		yield from resp.awrite(file.read())
		file.close()
	except:
		yield from resp.awrite(" ")	

@app.route("/load3")
def index(req, resp):
	yield from picoweb.start_response(resp)
	try:
		file = open("web1.txt","r")
		yield from resp.awrite(file.read())
		file.close()
	except:
		yield from resp.awrite(" ")	

@app.route("/load4")
def index(req, resp):
	yield from picoweb.start_response(resp)
	try:
		file = open("web2.txt","r")
		yield from resp.awrite(file.read())
		file.close()
	except:
		yield from resp.awrite(" ")	

@app.route("/run1")
def index(req, resp):
	queryString = req.qs
	parameters = qs_parse(queryString)
	print('Setup:')
	print(unquote(parameters["code"]))
	file = open("test.py","w")
	file.write(unquote(parameters["code"]))
	file.close()

@app.route("/run2")
def index(req, resp):
	queryString = req.qs
	parameters = qs_parse(queryString)
	print('loop:')
	print(unquote(parameters["code2"]))
	file = open("test2.py","w")
	file.write(unquote(parameters["code2"]))
	file.close()
	
@app.route("/run3")
def index(req, resp):
	queryString = req.qs
	parameters = qs_parse(queryString)	
	print('web1:')
	print(unquote(parameters["web1"]))
	file = open("web1.txt","w")
	file.write(unquote(parameters["web1"]))
	file.close()
	
@app.route("/run4")
def index(req, resp):
	global pck_sss
	global pck_stop
	global item
	pck_stop = 0
	pck_sss = ''
	queryString = req.qs
	parameters = qs_parse(queryString)		
	print('web2:')
	print(unquote(parameters["web2"]))
	file = open("web2.txt","w")
	file.write(unquote(parameters["web2"]))
	file.close()
	os.dupterm(DUP())
	yield from picoweb.start_response(resp)
	try: 
		execfile("test.py")
	except Exception as exc:
		sys.print_exception(exc)
		pck_stop = 1
	os.dupterm(None)
	yield from resp.awrite(item+","+pck_sss)

@app.route("/boardreset")
def index(req, resp):
	global pck_stop
	pck_stop = 1
	yield from picoweb.start_response(resp)
	yield from resp.awrite('Board Reset')
	os.remove("test.py")
	os.remove("test2.py")
	os.remove("web1.txt")
	os.remove("web2.txt")
	machine.reset()

@app.route("/stop")
def index(req, resp):
	global pck_stop
	pck_stop = 1
	yield from picoweb.start_response(resp)
	yield from resp.awrite('Stop by user')
	machine.reset()

@app.route("/respond")
def index(req, resp):
	global chart_value
	global pck_stop
	chart_value = int(random.random()*100)
	if pck_stop == 0:
		yield from picoweb.start_response(resp)
		yield from resp.awrite(str(chart_value)+","+pck_sss)
	else:
		yield from picoweb.start_response(resp)
		yield from resp.awrite(str(chart_value)+", ")

@app.route("/post")
def index(req, resp):
	queryString = req.qs
	parameters = qs_parse(queryString)
	yield from picoweb.start_response(resp)
	print(unquote(parameters["code"]))
	yield from resp.awrite("<html><script>window.location= 'http://'+window.location.host+'/static/index.html'</script></html>")

@app.route("/hello")
def index(req, resp):
	yield from picoweb.start_response(resp)
	yield from resp.awrite("Hello world from picoweb running on the ESP32")

@app.route("/init")
def index(req, resp):
	yield from picoweb.start_response(resp)
	file = open("init.txt","r")
	yield from resp.awrite(file.read())
	file.close()

@app.route("/ip")
def index(req, resp):
	yield from picoweb.start_response(resp)
	file = open("/static/ipscan.html","r")
	yield from resp.awrite(file.read())
	file.close()

@app.route("/scan")
def index(req, resp):
	yield from picoweb.start_response(resp)
	yield from resp.awrite("http://"+station.ifconfig()[0]+":8081")

@app.route("/wifiset")
def index(req, resp):
	queryString = req.qs
	parameters = qs_parse(queryString)
	yield from picoweb.start_response(resp)
	print(unquote(parameters["ssid"]))
	print(unquote(parameters["password"]))
	print(unquote(parameters["apmode"]))
	file = open("init.txt","w")
	file.write(unquote(parameters["ssid"]))
	file.write(",")	
	file.write(unquote(parameters["password"]))
	file.write(",")	
	file.write(unquote(parameters["apmode"]))
	file.close()
	yield from resp.awrite("wifiset restart")
	machine.reset()

@app.route("/")
def index(req, resp):
	queryString = req.qs
	if len(queryString)>0:
		parameters = qs_parse(queryString)
		if len(parameters)>0:
			print(unquote(parameters["url"]))
			global mainurl
			mainurl = unquote(parameters["url"])
	yield from picoweb.start_response(resp)
	yield from resp.awrite("<html><script>window.location= 'http://'+window.location.host+'/static/index.html'</script></html>")

@app.route("/url")
def index(req, resp):
	yield from picoweb.start_response(resp)
	global mainurl
	yield from resp.awrite(mainurl)


loop = uasyncio.get_event_loop()
loop.create_task(push_count())

print(station.ifconfig()[0])
app.run(debug=True, host = station.ifconfig()[0])



