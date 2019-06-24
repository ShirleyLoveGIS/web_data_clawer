#!/usr/bin/python3
# -*- coding:utf8 -*-
import flickrapi
import time
import datetime
import os, sys
import urllib.request

_root = 'C:/zxy/flickr/Data'


_min_taken_date='2011-12-24'
_max_taken_date='2012-01-02'

_place = 'San Francisco'
_bbox='-122.514587,37.708069,-122.357117,37.832397'
#
_place = 'City_of_Las_Vegas'
_bbox='-115.406575,36.129558,-115.062078,36.401493'
#
_place = 'City_of_Las_Vegas_north'
_bbox='-115.212087,36.184819,-114.893015,36.435261'

#_place = 'New York City'
#_bbox='-74.255591,40.496115,-73.700009,40.915533'
#
#_place = 'Seattle'
#_bbox='-122.441233,47.494557,-122.234312,47.73417'
#
#_place = 'Chicago'
#_bbox='-87.940114,41.644543,-87.524137,42.023039'
#
#_place = 'Yellow Sto ne'
#_bbox='-111.154305,44.132448,-109.833929,45.107849'  

api_key = '6c329aa1ddc3e69cb584127792a5d425'
api_secret = '9a94c095665cc368'
flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)

def saveImage(path, img):
	if not os.path.exists(path):
		if img:
			hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
			req = urllib.request.Request(img, headers=hdr)
			i = 0
			image=None        
			while(True):
				i = i + 1
				if i > 3:
					break
				try:
					image = urllib.request.urlopen(req)
				except:
					time.sleep(3)
				break
			if image is not None:
				fd = open(path, 'wb')
				fd.write(image.read())
				fd.close()
			print('Save:\t{0}'.format(path))
			return
	print('Pass:\t{0}'.format(path))

def saveMeta(path, photo):
	now = datetime.datetime.now()    
	with open(path + photo.get('id') + '.txt', 'w',encoding='utf-8')  as meta:
		try:
				meta.write('Time:\t' + now.strftime("%Y-%m-%d %H:%M:%S")+ '\n')
				meta.write('PotoID:\t{0}\n'.format(str(photo.get('id'))))
				meta.write('Owner:\t{0}\n'.format(str(photo.get('owner'))))
				meta.write('Secret:\t{0}\n'.format(str(photo.get('secret'))))
				meta.write('Title:\t' + str(photo.get('title','')) + '\n')
				meta.write('Desc:\t' + str(photo.get('description','') +'\n'))
				meta.write('Upload:\t{0}\n'.format(str(photo.get('dateupload'))))
				meta.write('Taken:\t{0}\n'.format(str(photo.get('datetaken'))))
				meta.write('Lat:\t{0}\n'.format(photo.get('latitude')))
				meta.write('Lon:\t{0}\n'.format(photo.get('longitude')))
				meta.write('Place:\t{0}\n'.format(photo.get('place_id')))
				meta.write('WOE:\t{0}\n'.format(photo.get('woeid')))
				meta.write('Tags:\t' + str(photo.get('tags')) +'\n')   
				meta.write('URL_C:\t{0}\n'.format(str(photo.get('url_c'))))
				meta.write('URL_L:\t{0}\n'.format(str(photo.get('url_l'))))
				meta.write('URL_O:\t{0}\n'.format(str(photo.get('url_o'))))
		except Exception as ex:
				print(ex)

def getLast():
	rootDir = _root + '/' + _place + '/' + _max_taken_date[:_max_taken_date.index('-')] + '/'
	date_last = _max_taken_date
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			if fname.endswith('.txt'):
				dt = parseTakenTime(dirName + '/' + fname)
				if date_last > dt:
					date_last = dt
	return date_last

def getLast2():	
	date_last = _max_taken_date
    	
	return date_last


def parseTakenTime(meta):
	with open(meta,encoding='utf-8')  as f:
		for line in f:
			if line.startswith('Taken'):
				return line[line.index('\t')+1:line.index(' ')]

def download(min_taken_date,max_taken_date):
	for photo in flickr.walk(
		api_key = api_key,
		#tag_mod='all',
		#tags='chongqing',
		min_taken_date= min_taken_date,
		max_taken_date= max_taken_date,
		geo_context=0,
		extras='description,date_upload,date_taken,geo,tags,machine_tags,url_c,url_l,url_o',
		sort='date-taken-desc',
		has_geo='1',
		per_page=100,
		media='photos',
		#woe_id='20070171'
		bbox=_bbox
		):
		now = datetime.datetime.now()
		print('...................................')
		print('Time:\t' + now.strftime("%Y-%m-%d %H:%M:%S"))
		print('PotoID:\t' + str(photo.get('id')))
		print('Owner:\t' + str(photo.get('owner')))
		print('Secret:\t' + str(photo.get('secret')))
		print('Title:\t' + str(photo.get('title')))
		print('Desc:\t' + str(photo.get('description')))
		print('Upload:\t'+ str(photo.get('dateupload')))
		print('Taken:\t'+ str(photo.get('datetaken')))
		print('Lat:\t' + str(photo.get('latitude')))
		print('Lon:\t' + str(photo.get('longitude')))
		print('Place:\t' + str(photo.get('place_id')))
		print('WOE:\t' +  str(photo.get('woeid')))
		print('Tags:\t' + str(photo.get('tags')))
		print('MTags:\t' + str(photo.get('machine_tags')))
		print("URL_C:\t" + str(photo.get('url_c')))
		print("URL_L:\t" + str(photo.get('url_l')))
		print("URL_O:\t" + str(photo.get('url_o')))
	
		date_taken = datetime.datetime.strptime(photo.get('datetaken'), '%Y-%m-%d %H:%M:%S')
		path = _root + '/' + _place + '/' + date_taken.strftime('%Y-%m-%d')+ '/' + str(photo.get('owner')) + '/'
		fld = os.path.dirname(path)
		if not os.path.exists(fld):
			os.makedirs(fld, 493);
		
		img_url = None
		if photo.get('url_c'):
			img_url = photo.get('url_c')

		if photo.get('url_o'):
			img_url = photo.get('url_o')	

		if photo.get('url_l'):
			img_url = photo.get('url_l')
		
		if img_url:	
			saveMeta(path, photo)
			saveImage(path + img_url[img_url.rindex('/')+1:], img_url)



#_max_taken_date = getLast()
_min_taken_date = datetime.datetime.strptime(_min_taken_date, '%Y-%m-%d')
_max_taken_date = datetime.datetime.strptime(_max_taken_date, '%Y-%m-%d')
start_time = _min_taken_date
end_time = start_time + datetime.timedelta(days=1)
while end_time != _max_taken_date:
    download(start_time.strftime('%Y-%m-%d'),end_time.strftime('%Y-%m-%d'))
    start_time = end_time
    end_time = end_time + datetime.timedelta(days=1)
