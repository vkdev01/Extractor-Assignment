import requests
import sys
import time
import os

from urllib.parse import unquote

units = {	
'B' : {'size':1, 'speed':'B/s'},
'KB' : {'size':1024, 'speed':'KB/s'},
'MB' : {'size':1024*1024, 'speed':'MB/s'},
'GB' : {'size':1024*1024*1024, 'speed':'GB/s'}
}


def check_unit(length): # length in bytes
	if length < units['KB']['size']:
		return 'B'
	elif length >= units['KB']['size'] and length <= units['MB']['size']:
		return 'KB'
	elif length >= units['MB']['size'] and length <= units['GB']['size']:
		return 'MB'
	elif length > units['GB']['size']:
		return 'GB'


def downloadFile(url, directory) :# takes download link and directory where file to be saved

	if not os.path.exists(directory):
		os.makedirs(directory)
	

	localFilename = url.split('/')[-1] # file name
	localFilename = unquote(localFilename).encode("ascii", "ignore").decode().strip().replace(' ', '_')

	with open(directory + '/' + localFilename, 'wb') as f:
		start = time.time() # start time
		r = requests.get(url, stream=True)

		total_length = float(r.headers.get('content-length')) 
		d = 0 
		
		if total_length is None:
			f.write(r.content)
		else:
			for chunk in r.iter_content(8192):
				
				d += float(len(chunk))
				f.write(chunk) # writing the file in chunks of 8192 bytes

				# amount downloaded in proper units
				downloaded = d/units[check_unit(d)]['size']

				tl = total_length / units[check_unit(total_length)]['size'] 
				
				trs = d // (time.time() - start)

				download_speed = trs/units[check_unit(trs)]['size']
				
				speed_unit = units[check_unit(trs)]['speed']

				done = 100 * d / total_length
				
				fmt_string = "\r%6.2f %s [%s%s] %7.2f%s  /  %4.2f %s  %7.2f %s"
				
				set_of_vars = ( float(done), '%',
								'*' * int(done/2),  
								'_' * int(50-done/2),  
								downloaded, check_unit(d),  
								tl, check_unit(total_length),  
								download_speed, speed_unit)

				sys.stdout.write(fmt_string % set_of_vars)
				sys.stdout.flush()

	return localFilename, (time.time() - start)


def start_download(url, dir):
	print('')
	print(f"\rDownloading {url} ...\n", flush=True, end='')
	file_name = downloadFile(url, dir)
	return file_name
