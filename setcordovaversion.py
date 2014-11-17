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
# Check if the current folder is a Cordova folder
#
#####
def isCordovaProjectFolder():
	# Check for a set of folders that looks like a Cordova project
	files = [f for f in os.listdir('.') if os.path.isdir(f)]
	platformsFound = False
	pluginsFound = False
	wwwFound = False
	hooksFound = False

	for f in files:
		if (f == 'platforms'):
			platformsFound = True
		if (f == 'hooks'):
			hooksFound = True
		if (f == 'www'):
			wwwFound = True
		if (f == 'plugins'):
			pluginsFound = True

	# Check for a config.xml too then we can be pretty confident 
	# is is the right place!
	configXmlFound = os.path.isfile('config.xml')

	return (configXmlFound and platformsFound and pluginsFound and hooksFound and wwwFound)

#####
#
# Check if the project has a specific platform installed
#
#####
def hasPlatform(platformToCheck):
	return (os.path.isdir('platforms') and os.path.isdir('platforms/' + platformToCheck))

#####
#
# Open project's config.xml file and set the version number 
# and build number according to the parameters.
#
#####
def setVersionAndBuildNumbers(versionNumber, buildNumber):
	# Determine which platforms this project has, supports 
	# iOS and Android at the moment

	print 'Opening project\'s config.xml file'
	xmlTree = minidom.parse('config.xml')
	widgetElem = xmlTree.getElementsByTagName('widget')

	if (len(widgetElem) == 1):
		widgetElem = widgetElem[0]
	else:
		# Failed invalid XML
		print '*****ERROR: Failed to find a single <widget> element in config.xml'
		sys.exit(1)

	print 'Setting version number to ' + versionNumber
	widgetElem.setAttribute('version', versionNumber)

	if (hasPlatform('ios')):
		print 'Setting iOS build number to ' + buildNumber
		widgetElem.setAttribute('ios-CFBundleVersion', buildNumber)
	
	if (hasPlatform('android')):
		print 'Setting Android build number to ' + buildNumber
		widgetElem.setAttribute('android-versionCode', buildNumber)

	# Persist the XML back to config.xml as utf-8
	with codecs.open('config.xml', 'wb', 'utf-8') as out:
		xmlTree.writexml(out, encoding='utf-8')

#####
# Entry point, run the script...
#####
if (len(sys.argv) == 3):
	# Correct number of arguments, check if this is a 
	# Cordova project directory...
	if (isCordovaProjectFolder()):
		# Check that first arugment is valid, Cordova needs 0.0.0 type format
		if (isValidCordovaVersionString(sys.argv[1])):
			# Check that the second argument is valid, Cordova needs a number
			if (isValidCordovaBuildString(sys.argv[2])):
				setVersionAndBuildNumbers(sys.argv[1], sys.argv[2])
				print 'config.xml updated successfully'
			else:
				print '*****ERROR: buildNumber must be an integer number'
				sys.exit(1)
		else:
			print '*****ERROR: versionNumber must be of the form 0.0.0'
			sys.exit(1)
	else:
		print '*****ERROR: This script must be run inside a Cordova project folder'
		sys.exit(1)
else:
	print '*****ERROR: Expecting 2 parameters: versionNumber buildNumber'
	sys.exit(1)