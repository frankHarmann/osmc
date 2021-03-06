# Standard modules
import os
import shutil
import sys
import subprocess

# XBMC modules
import xbmc
import xbmcaddon
import xbmcgui

FOLDER = xbmc.translatePath(os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources'))

FONT_FOLDER = xbmc.translatePath(os.path.join(FOLDER, 'skins', 'Default', 'fonts'))

FONT_PARTIALS = os.path.join(FOLDER, 'lib', 'fonts.txt')
# FONT_PARTIALS = '/home/kubkev/.kodi/addons/service.osmc.settings/resources/lib/fonts.txt'


def import_osmc_fonts():

	alien_skin_folder = xbmc.translatePath('special://skin')

	print 'alien_skin_folder: %s' % alien_skin_folder

	alien_fonts_folder = os.path.join(alien_skin_folder, 'fonts/')

	possible_xml_locations = ['1080i', '720p', '1080p','16x9']

	for pos_loc in possible_xml_locations:

		alien_xml_folder = os.path.join(alien_skin_folder, pos_loc)

		print 'POSSIBLE XML LOCATION = %s' % alien_xml_folder

		try:

			alien_fonts = set(os.listdir(alien_fonts_folder))
			test = os.listdir(alien_xml_folder)
			alien_font_xml = os.path.join(alien_xml_folder, 'Font.xml')

			break

		except:

			pass

		print 'ISNT A FOLDER'

	else:

		print 'BREAKEN'

		return 'failed'

	print 'ACTUAL XML LOCATION = %s' % alien_xml_folder

	print 'alien_font_xml = %s' % alien_font_xml

	# check whether the fonts are already in the font xml, if they are then simply return.
	# the previous solution of checking for a backup fonts file is pointless as an update of the skin
	# would overwrite the Font.xml and leave the backup in place
	with open(alien_font_xml, 'r') as f:
		lines = f.readlines()
		for line in lines:
			if 'osmc_addon_OLD_Font72' in line:
				return 'ubiquited'

	# copy fonts to skins font folder 
	unique_files = set(os.listdir(FONT_FOLDER)) - alien_fonts

	for filename in unique_files:
		subprocess.call(["sudo", "cp", os.path.join(FONT_FOLDER, filename), alien_fonts_folder])

	with open(FONT_PARTIALS, 'r') as f:
		osmc_lines = f.readlines()

	with open(alien_font_xml, 'r') as af:
		alien_lines = af.readlines()

	new_lines = []

	count = 0

	for line in alien_lines:

		if '</fontset>' in line and count == 0:

			count += 1

			for l in osmc_lines:

				new_lines.append(l)

			new_lines.append(line)

		else:

			new_lines.append(line)

	# make backup of original Font.xml
	backup_file = os.path.join(alien_fonts_folder,'backup_Font.xml')
	
	print 'BACKUP FILE: %s' % backup_file

	subprocess.call(["sudo", "cp", alien_font_xml, backup_file])
	
	with open('/tmp/Font.xml', 'w') as bf:
		bf.writelines(new_lines)

	subprocess.call(["sudo", "mv", '/tmp/Font.xml', alien_font_xml])

	return 'reload_please'

if __name__ == "__main__":

	import_osmc_fonts()