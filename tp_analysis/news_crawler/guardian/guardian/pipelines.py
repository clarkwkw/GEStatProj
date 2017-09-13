# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TextListPipeline(object):
	def open_spider(self, spider):
		self.records = []

	def close_spider(self, spider):
		with open(spider.output_path, "w") as f:
			json.dump({"texts": self.records}, f, indent = 4)

	def process_item(self, item, spider):
		self.records.append(item)
		return item

class TextsPipeline(object):
	def close_spider(self, spider):
		spider.save_master_record()

	def process_item(self, item, spider):
		f_name = "{output_dir:s}/{prefix:s}-{number:0{width}d}.json".format(output_dir = spider.output_dir, prefix = spider.text_name_prefix, number = spider.last_unallocated_number, width = spider.text_name_length)
		with open(f_name, "w") as f:
			text = json.dumps(item, indent = 4)
			text = text.decode('unicode_escape').encode('ascii','ignore')
			f.write(text)
		spider.master_record[item["gid"]] = f_name
		spider.last_unallocated_number += 1
		return item