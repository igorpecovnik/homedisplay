#!/usr/bin/python
# This Python file uses the following encoding: utf-8
#--------------------------------------------------------------------------------------------------------------------------------
# Small home information display (c) Igor Pecovnik
#--------------------------------------------------------------------------------------------------------------------------------

# apt-get install python-pygame python-bs4 python-requests python-pywapi python-dev python-pip
# pip install html5lib beautifulsoup4
# install https://github.com/LeMaker/RPi.GPIO_BP
# dpkg-reconfigure locales # add si-utf8

import os, pygame, time, datetime, string, locale, commands
import functions
import RPi.GPIO as GPIO
from time import localtime,strftime
from functions import framebuffer
from collections import OrderedDict

locale.setlocale(locale.LC_TIME, "sl_SI.UTF-8")

# Sensors

PIR1 = 11
PIR2 = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR1,GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(PIR2,GPIO.IN,GPIO.PUD_DOWN)
 
# create instance of frame buffer screen
mytft = framebuffer()
# hide mouse pointer
pygame.mouse.set_visible(False)

# data initialisation 
weather_outside 					= functions.weather("SIXX0002","outside")
weather_inside 						= functions.weather("SIXX0002","inside")
weather_wind 						= functions.weather("SIXX0002","wind")
weather_humidity 					= functions.weather("SIXX0002","humidity")
weather_text	 					= functions.weather("SIXX0002","text")

# bus initialisation (time ignore, station)
left 				= functions.busrefresh(7,103071)
right 				= functions.busrefresh(7,103161)

# counters initialisation 
seconds = 1
n = 1
busnumber = 0
catsound = 0
while True:
		# clear the screen
		if GPIO.input(PIR1) == 1:
			background = "#ffffff"
			temperature =  "#000000"
			bustime = "#440000"
		#	if catsound == 0:
		#		catsound = 1
		#		sounda= pygame.mixer.Sound("angry4.wav")
		#		sounda.play()
		else:
			background = "#000000"
			temperature =  "#ffffff"
			bustime = "#ffd767"
		mytft.screen.fill(pygame.Color(background))
			
		# Clock and date
		#
		fontpath 			= "tt0246m_.ttf"		
		fontpath 			= "Lekton-Regular.ttf"
		fontsize			= 18	
		font 				= pygame.font.Font(fontpath, fontsize)			
		alphabet0 			= strftime("%A", localtime()).replace(' 0', ' ').decode("utf-8")		
		text_surface0		= font.render(alphabet0, True, pygame.Color(temperature))
		alphabet1 			= strftime("%d %B", localtime()).replace(' 0', ' ').decode("utf-8")		
		text_surface1		= font.render(alphabet1, True, pygame.Color(temperature))		
		fontpath 			= "ariblk.ttf"
		fontsize			= 30
		font 				= pygame.font.Font(fontpath, fontsize)			
		alphabet2 			= strftime("%H:%M", localtime())				
		text_surface2 		= font.render(alphabet2, True, pygame.Color(temperature))
		mytft.screen.blit(text_surface1, (160-(text_surface1.get_width()/2),54))
		mytft.screen.blit(text_surface2, (160-(text_surface2.get_width()/2),14))
		mytft.screen.blit(text_surface0, (160-(text_surface0.get_width()/2),4))			
		#
		# Temp outside and inside
		#		
		fontpath 			= "tt0246m_.ttf"		
		fontpath 			= "Lekton-Regular.ttf"
		
		font = pygame.font.Font(fontpath, 42)				
		degree_sign= u'\N{DEGREE SIGN}'		
		text_surface2 = font.render(weather_outside+degree_sign, True, pygame.Color(temperature)) # White text
		text_surface1 = font.render(weather_inside+degree_sign, True, pygame.Color(temperature)) # White text
		
		mytft.screen.blit(text_surface1, (15,15))	
		mytft.screen.blit(text_surface2, (245,15))
			
		
		# Wind and humidity
		text_surface3 = font.render(weather_wind, True, pygame.Color(temperature)) 
		text_surface4 = font.render(weather_humidity, True, pygame.Color(temperature))
		mytft.screen.blit(text_surface3, (15,80))
		mytft.screen.blit(text_surface4, (245,80))	
		# units with smaller font
		font = pygame.font.Font(fontpath, 22)
		text_surface5 = font.render("km/h", True, pygame.Color(temperature)) 
		text_surface6 = font.render("%", True, pygame.Color(temperature)) 
		mytft.screen.blit(text_surface5, (65,94))
		mytft.screen.blit(text_surface6, (290,94))		
		
				
		#
		# Bus
		#
		fontpath 			= "Lekton-Regular.ttf"
		#left 				= functions.busrefresh(6,103071)
		left				= OrderedDict(sorted(left.items(), key=lambda t: t[1]))
		vrstica 			= 0
		for key in left:
			#print "%s: %s" % (key, test[key])
			
			alphabet 			= str(left[key])
			alphabet			= format(alphabet,">2s")
			font 				= pygame.font.Font(fontpath, 24)		
			text_surface1 		= font.render(alphabet, True, pygame.Color(bustime)) # White text
			
			alphabet 			= key.rstrip()			
			font 				= pygame.font.Font(fontpath, 24)		
			text_surface2 		= font.render(alphabet, True, pygame.Color(bustime)) # White text
			
			mytft.screen.blit(text_surface2, (15,140+vrstica))
			mytft.screen.blit(text_surface1, (145,140+vrstica))
			vrstica = vrstica + 30

			
		#right 				= functions.busrefresh(6,103161)
		right				= OrderedDict(sorted(right.items(), key=lambda t: t[1]))
		vrstica 			= 0
		for key in right:
			#print "%s: %s" % (key, test[key])
			
			alphabet 			= str(right[key])
			font 				= pygame.font.Font(fontpath, 24)		
			text_surface1 		= font.render(alphabet, True, pygame.Color(bustime)) # White text
			
			alphabet 			= key.rstrip()
			font 				= pygame.font.Font(fontpath, 24)		
			text_surface2 		= font.render(alphabet, True, pygame.Color(bustime)) # White text
			
			mytft.screen.blit(text_surface2, (180,140+vrstica))
			mytft.screen.blit(text_surface1, (275,140+vrstica))
			vrstica = vrstica + 30	
	
	
	
	
	
	
	
				
				
		pygame.display.update()
		#pygame.image.save(mytft.screen,"screenshot.jpeg")
		time.sleep(1)
		
		seconds = seconds + 1
			
		if seconds == 15*n:
			left 				= functions.busrefresh(7,103071)
			right 				= functions.busrefresh(7,103161)
			n = n + 1
			#print "osv. bus"
		if seconds == 60:	
			weather_outside 	= functions.weather("SIXX0002","inside")
			weather_outside 	= functions.weather("SIXX0002","outside")
			weather_wind 		= functions.weather("SIXX0002","wind")
			weather_humidity 	= functions.weather("SIXX0002","humidity")
			weather_text	 	= functions.weather("SIXX0002","text")
			#print "Osvezi temp"			
			seconds = 0
			n = 1
		


