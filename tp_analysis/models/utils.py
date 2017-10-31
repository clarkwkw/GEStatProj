import os, errno

def ensure_dir_exist(dir):
	try:
		os.makedirs(dir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise