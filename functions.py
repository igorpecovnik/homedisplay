#!/usr/bin/python
from bs4 import BeautifulSoup
import os, pygame, pywapi, pygame, urllib2, codecs

device = "/dev/fb2"		# your main framebuffer display is usually /dev/fb0

def bus( i ):
	with open("file.txt") as f:   
		lenght = sum(1 for _ in f)
		if lenght == 0 or lenght <= i*2:
			return 0, "No data", "No data"
		f.seek(0, 0)		
		lines = f.readlines()[i*2:i*2+2]
		line0 = lines[0].replace("\n", " ")
		line1 = lines[1].replace("\n", " ")	
		f.close()
	return lenght, line0, line1


def weather ( location, n ):   
	fontpath = "tt0246m_.ttf"
	font = pygame.font.Font(fontpath, 16)		
	weather_com_result = pywapi.get_weather_from_yahoo(location, 'metric')
	degree_sign= u'\N{DEGREE SIGN}' 
	
	if n == "wind":
			vrni = str(int(round(float(weather_com_result['wind']['speed']),0)))
			vrni = '{:>2}'.format(vrni)
	elif n == "text":
			vrni = weather_com_result['condition']['text']
	elif n == "humidity":
			vrni = weather_com_result['atmosphere']['humidity']
	elif n == "inside":
			while True:
				f = open('/run/amb-temp', 'r').readline()
				if f != "":
					vrni = str(int(round(float(f),0)))
					break
	else:
			vrni = weather_com_result['condition']['temp']			
			vrni = '{:>2}'.format(vrni)
	return vrni

def busrefresh ( cutoff, postaja ):
	#postaja = [103071,103161]
	p = 0
	zunaj = {}
	while True :
		url = "http://www.trola.si/"+str(postaja)
		soup = BeautifulSoup(urllib2.urlopen(url), "html5lib")
		p = p + 1	
		druge = ""
		y = []
		for node in soup.findAll('td'):	
			y.append (''.join(node.findAll(text=True)))
		i = 2
		u = 1
		for index, item in enumerate(y):		
			j = 3*i-2
			k = 2+3*u
			if index == j:		
				i = i + 1
				result = item.strip(" p+r")
				if  "Gara" in result or "Center" in result:
					u = u + 1
					j = 3*i-2
					k = 2+3*u
				else:
					# text_file.write(result+"\n")
					druge = result
			if index == k:		
				u = u + 1			
				result = item.replace(',', '')
				result = result.replace("'", '')				
				# text_file.write(result+"\n")
				if result != "Ni prihodov.":
					line=result.split()
					r=int(line[0])
					# skip bus under cutoff minutes to go
					if r < cutoff and len(line)>1:
						r=int(line[1])
					#print str(p)+">"+druge+str(r)
					zunaj.update([(druge,r)])
		if p == 2:
			break
	return zunaj
	
class framebuffer :
	screen = None;
	def __init__(self):
		"Ininitializes a new pygame screen using the framebuffer"
		disp_no = os.getenv("DISPLAY")
		if disp_no:
			print "I'm running under X display = {0}".format(disp_no)
		
		os.putenv('SDL_FBDEV', device)
		drivers = ['fbcon', 'directfb', 'svgalib']
		found = False
		for driver in drivers:
			# Make sure that SDL_VIDEODRIVER is set
			if not os.getenv('SDL_VIDEODRIVER'):
				os.putenv('SDL_VIDEODRIVER', driver)
			try:
				pygame.display.init()	
			except pygame.error:
				print 'Driver: {0} failed.'.format(driver)
				continue
			found = True
			break

		if not found:
			raise Exception('No suitable video driver found!')
			
		pygame.mixer.init()
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		print "Framebuffer size: %d x %d" % (size[0], size[1])
		self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)	
		self.screen.fill((0,0,0))        
		pygame.font.init()
		pygame.display.update()
