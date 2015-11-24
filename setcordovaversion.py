#!/usr/bin/env python 

#####
#
# Purpose: Set version and build numbers for Cordova app
#          for iOS and Android in config.xml
#
# Author: Simon Prickett
#
#####

import codecs
import os
import sys
import getopt
from xml.dom import minidom

#####
#
# Checks if the version string provided is in the correct format
#
#####
def isValidCordovaVersionString(versionString):
	versionStringComponents = versionString.split('.')

	if (len(versionStringComponents) == 3):
		# We have the right number of component parts
		# Check each is actually a number
		for i in range(len(versionStringComponents)):
			try:
				int(versionStringComponents[i])
			except ValueError:
				return False

		return True
	else:
		return False	

def isValidCordovaBuildString(buildString):
	try:
		int(buildString)
		return True
	except ValueError:
		return False

#####
#
# Open project's config.xml file and set the version number 
# and build number according to the parameters.
#
#####
def setVersionAndBuildNumbers(versionNumber, buildNumber, configFile):
	# Determine which platforms this project has, supports 
	# iOS and Android at the moment

	print 'Opening project\'s config.xml file'
	xmlTree = minidom.parse(configFile)
	widgetElem = xmlTree.getElementsByTagName('widget')

	if (len(widgetElem) == 1):
		widgetElem = widgetElem[0]
	else:
		# Failed invalid XML
		print '*****ERROR: Failed to find a single <widget> element in config.xml'
		sys.exit(1)

	print 'Setting version number to ' + versionNumber
	widgetElem.setAttribute('version', versionNumber)

	print 'Setting iOS build number to ' + buildNumber
	widgetElem.setAttribute('ios-CFBundleVersion', buildNumber)
	
	print 'Setting Android build number to ' + buildNumber
	widgetElem.setAttribute('android-versionCode', buildNumber)

	# Persist the XML back to config.xml as utf-8
	with codecs.open(configFile, 'wb', 'utf-8') as out:
		xmlTree.writexml(out, encoding='utf-8')

#####
# Entry point, run the script...
#####
if (len(sys.argv) == 4):
	if (os.path.isfile(sys.argv[3])):
		# Check that first arugment is valid, Cordova needs 0.0.0 type format
		if (isValidCordovaVersionString(sys.argv[1])):
			# Check that the second argument is valid, Cordova needs a number
			if (isValidCordovaBuildString(sys.argv[2])):
				setVersionAndBuildNumbers(sys.argv[1], sys.argv[2], sys.argv[3])
				print sys.argv[3] + ' updated successfully'
			else:
				print '*****ERROR: buildNumber must be an integer number'
				sys.exit(1)
		else:
			print '*****ERROR: versionNumber must be of the form 0.0.0'
			sys.exit(1)
	else:
		print '*****ERROR: ' + sys.argv[3] + ' file does not exist'
else:
	print '*****ERROR: Expecting 3 parameters: versionNumber buildNumber config.xml'
	sys.exit(1)