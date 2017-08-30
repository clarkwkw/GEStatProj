# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
import json
import logging
import utils
import math

_query_conds = "?show-fields=headline,body,wordcount&shouldHideAdverts=true"

class GetTextsSpider(scrapy.Spider):
	name = "get_texts"
	handle_httpstatus_list = [500, 403, 429]
	custom_settings = {
		'ITEM_PIPELINES': {
			'guardian.pipelines.TextsPipeline': 300
		}
	}

	def __init__(self, api_key = "", output_dir = "", text_list_file = "", *args, **kwargs):
		super(GetTextsSpider, self).__init__(*args, **kwargs)
		utils.create_dir(output_dir)
		if len(api_key) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'api_key' to be a string")
		if len(output_dir) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'output_dir' to be a string")
		if len(text_list_file) == 0:
			raise scrapy.exceptions.CloseSpider("expected 'text_list_file' to be a string")

		self.api_key = api_key
		self.output_dir = output_dir

		with open(text_list_file, "r") as f:
			self.all_texts = json.load(f)['texts']

		if utils.is_file_exists(output_dir+"/master_record.json"):
			with open(output_dir+"/master_record.json", "r") as f:
				json_file = json.load(f)
				self.master_record = json_file["master_record"]
				self.last_unallocated_number = json_file["last_unallocated_number"]
		else:
			self.master_record = {text["gid"]: "" for text in self.all_texts}
			self.last_unallocated_number = 1

		self.text_name_prefix = "Guardian"
		self.text_name_length = int(math.floor(math.log(len(self.all_texts))/math.log(10)) + 1)

	def save_master_record(self):
		with open(self.output_dir+"/master_record.json", "w") as f:
			json.dump({"master_record": self.master_record, "last_unallocated_number": self.last_unallocated_number}, f, indent = 4)

	def start_requests(self):
		for text in self.all_texts:
			if len(self.master_record[text["gid"]]) > 0:
				continue
			yield scrapy.http.Request(url = text['url']+_query_conds, method = "GET", headers = {"api-key": self.api_key}, callback = self.parse)

	def parse(self, response):
		try:
			json_response = utils.simple_check(response)
		except Exception as e:
			logging.error("request_failed: %s"%e.message)
			raise scrapy.exceptions.CloseSpider("request_failed: %s"%e.message)
		result = {}
		result["gid"] = json_response["content"]["id"]
		result["section"] = json_response["content"]["sectionId"]
		result["headline"] = utils.remove_html(json_response["content"]["fields"]["headline"])
		result["text"] = utils.remove_html(json_response["content"]["fields"]["body"])
		result["wordcount"] = json_response["content"]["fields"]["wordcount"]

		yield result