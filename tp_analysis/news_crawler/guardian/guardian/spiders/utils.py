import json
import logging
import re
import os, errno

def simple_check(response):
	json_response = json.loads(response.body_as_unicode())
	if response.status == 429:
		raise Exception("API rate limit exceeded")
	if 'response' not in json_response or json_response['response']['status'] != 'ok':
		raise Exception("malformed response: %s"%json_response)
	return json_response['response']

def remove_html(text):
	return re.sub('<[^<]+?>', '', text)

def is_file_exists(file):
	return os.path.exists(file)

def create_dir(dir):
	try:
		os.makedirs(dir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise