from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import re
import time
import requests

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

# Constants
#BASE_URL = 'https://de.wikipedia.org/wiki/Bildtafel_der_Verkehrszeichen_in_der_Bundesrepublik_Deutschland_seit_2017'
#BASE_URL = 'https://en.wikipedia.org/wiki/Road_signs_in_the_United_States' #last;454error
BASE_URL =  'https://en.wikipedia.org/wiki/Road_signs_in_China'
#BASE_URL = 'https://en.wikipedia.org/wiki/Road_signs_in_Russia'
DOWNLOAD_LOCATION = 'CN' #'/home/rich/Documents/Projects/scrapers/scraper_esl_discussions/testoutput'
PATH_STORE_IMAGES = 'CN' #'/home/rich/Documents/Projects/scrapers/scraper_road_signs_de'
 
#######################################################
# add geckodriver to path
# media types for download config: https://www.freeformatter.com/mime-types-list.html
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
# set location for downloads
profile.set_preference('browser.download.dir', DOWNLOAD_LOCATION)
# do not show download dialogs
profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
 'application/pdf, application/msword')
 
 
# set webdriver with configure profile
gecko_path = '../geckodriver'
driver = webdriver.Firefox(profile, executable_path=gecko_path)
 
driver.get(BASE_URL)
time.sleep(1)
 
# find list elements by xpath, then get the image element get the link
signs = driver.find_elements_by_xpath(
 "//li[@class='gallerybox']/div")
 
print(f"Found {len(signs)} images")
 
# create new directorires
svg_dir = os.path.join(PATH_STORE_IMAGES, 'svg')
print(svg_dir)
if not os.path.exists(svg_dir):
 os.mkdir(svg_dir)
png_dir = os.path.join(PATH_STORE_IMAGES, 'png')
print(png_dir)
if not os.path.exists(png_dir):
 os.mkdir(png_dir)
 
# loop over all signs
for i in range(len(signs)):
 print(i)
 time.sleep(1)
 # find all road sign image by xpath
 img = signs[i].find_element_by_xpath(
 ".//a[@class='image']/img") # the '.' is needed to refer to the current element
 # find text for road sign
 gallery_text = signs[i].find_element_by_class_name(
 'gallerytext').text
 # get text, split on first line break
 gallery_text = gallery_text.partition('\n')
 # get first line, remove white spaces and only keep letters, numbers, umlaute
 first_line = gallery_text[0].strip()
 first_line = re.sub(
 '[^-A-Za-z0-9äöüÄÖÜß]+', '_', first_line)
 
 # get rest of description text
 other_lines = gallery_text[2]
 other_lines = other_lines if len(
 other_lines) < 100 else other_lines[0:50]
 # remove white spaces, new lines
 other_lines = '_'.join(other_lines.split())
 # remove all special characters
 other_lines = re.sub(
 '[^-A-Za-z0-9äöüÄÖÜß]+', '_', other_lines)
 # create new filename
 new_filename = f'{first_line}_{other_lines}' if len(
 other_lines) > 0 else f'{first_line}'
 # download image
 png_file_path = img.get_attribute('src')
 urllib.request.urlretrieve(png_file_path, os.path.join(png_dir, f'{new_filename}.png'))
 
 # download svg by defining base path for all svgs
 base_url_svg = 'https://upload.wikimedia.org/wikipedia/commons/'
 # find svg path for image (this path is to a png, we can derive the svg path from there)
 svg_path = signs[i].find_element_by_xpath(
 ".//a[@class='image']/img").get_attribute('src')
 # cut out needed parts and download
 svg_path = svg_path.split('thumb/', 1)[1]
 svg_path = svg_path.split('.svg/', 1)[0]
 if svg_path[-3:] == "gif":
    svg_path = svg_path.split('.gif/', 1)[0]
    end_svg_path = '.gif'
 elif svg_path[-3:] == "png":
    svg_path = svg_path.split('.png/', 1)[0]
    end_svg_path = '.png'
 elif svg_path[-3:] == "jpg":
    svg_path = svg_path.split('.jpg/', 1)[0]
    end_svg_path = '.jpg'   
 else:
    end_svg_path = ".svg"
    
 # download svg
 svg_file_path = base_url_svg + svg_path + end_svg_path
 #print("path", svg_file_path)
 if end_svg_path == '.gif':
    urllib.request.urlretrieve(svg_file_path, os.path.join(svg_dir, f'{new_filename}.gif'))
 elif end_svg_path == '.png':
    urllib.request.urlretrieve(svg_file_path, os.path.join(svg_dir, f'{new_filename}.png'))
 elif end_svg_path == '.jpg':
    urllib.request.urlretrieve(svg_file_path, os.path.join(svg_dir, f'{new_filename}.jpg'))   
 else:
    urllib.request.urlretrieve(svg_file_path, os.path.join(svg_dir, f'{new_filename}.svg'))
 #else:
 #   print("file_not_found")
 
time.sleep(1)
driver.close()