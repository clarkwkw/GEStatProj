# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
import json
import logging
import utils

#_sections = ["education", "science", "technology", "higher-education-network", "environment", "global-development"]
_sections = ["business"]
_base_url = "https://content.guardianapis.com/search"
_page_size = 50

class ListTextsSpider(scrapy.Spider):
	name = "list_texts"
	handle_httpstatus_list = [500, 403, 429]
	custom_settings = {
		'ITEM_PIPELINES': {
			'guardian.pipelines.TextListPipeline': 300
		}
	}
	def __init__(self, api_key = "", output_path = "", sections = _sections, from_date = "", to_date = "", *args, **kwargs):
		super(ListTextsSpider, self).__init__(*args, **kwargs)
		
		if len(api_key) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'api_key' to be a string")
		if len(output_path) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'output_path' to be a string")
		if type(sections) is not list or len(sections) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'sections' to be a list of strings")
		if len(from_date) == 0 or len(to_date) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'sections' to be a list of strings")

		self.api_key = api_key
		self.output_path = output_path
		self.query_conds = []

		self.query_conds.append("section=%s"%("|".join(sections)))
		self.query_conds.append("page-size=%d"%_page_size)
		if len(from_date) > 0:
			self.query_conds.append("from-date=%s"%from_date)
		if len(to_date) > 0:
			self.query_conds.append("to-date=%s"%to_date)

		self.cur_page = 0
		self.total_pages = 0

	def generate_query_str(self, page = -1):
		query_conds = self.query_conds
		if page <= 0:
			return "?%s"%("&".join(query_conds))
		else:
			return "?%s"%("&".join(query_conds + ["page=%d"%page]))

	def start_requests(self):
		query_str = self.generate_query_str()
		yield scrapy.http.Request(url = _base_url+query_str, method = "GET", headers = {"api-key": self.api_key}, callback = self.handle_initial_request)

	def handle_initial_request(self, response):
		try:
			json_response = utils.simple_check(response)
		except Exception as e:
			logging.error("initial_request_failed")
			raise scrapy.exceptions.CloseSpider("initial_request_failed")

		self.total_pages = json_response['pages']
		print("No. of pages: %d"%self.total_pages)
		for i in range(2, self.total_pages + 1):
			query_str = self.generate_query_str(page = i)
			yield scrapy.http.Request(url = _base_url+query_str, method = "GET", headers = {"api-key": self.api_key}, callback = self.parse)

		for item in self.parse(response):
			yield item
		
	def parse(self, response):
		result_keys = {"gid": "id", 
						"section": "sectionId", 
						"date": "webPublicationDate", 
						"url": "apiUrl"}
		try:
			json_response = utils.simple_check(response)
		except Exception as e:
			logging.error("request_failed")
			raise scrapy.exceptions.CloseSpider("request_failed: %s"%e.message)

		for json_result in json_response["results"]:
			result = {}
			for key, raw_key in result_keys.items():
				result[key] = json_result[raw_key]
			yield result
		print("Parsed page %d"%json_response["currentPage"])