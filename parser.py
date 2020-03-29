# Fandom Table Parser
import json
import re
import typing
header_template = re.compile(r"[^\!\|\t\n\r ]*=\".*\"( \| )*", re.IGNORECASE|re.MULTILINE)

class Table(object):
	def __init__(self, file: str = "", name:str = ""):
		string = file
		# print(string)
		self.name = name
		lines = string.split("\n")
		# defining headers
		self.headers = list(map(self.headerFormat, list(filter(self.isHeader, lines))))

		self.items = list(map(self.to_item, string.split("\n|-\n")))
		self.pop(0)

	def dump(self):
		json.dump(self.items, open(f"out/{self.name}.json", "w"))
	def dumps(self):
		json.dumps(self.items)

	def pop(self, index: int):
		return self.items.pop(index)

	@staticmethod
	def isHeader(text: str) -> str:
		return text.startswith("!")
	
	@staticmethod
	def headerFormat(headerText: str) -> str:
		return re.sub(header_template, "", headerText.replace("!", "", 1)).strip()
	
	def to_item(self, item_string: str) -> dict:
		item_list = item_string.replace("!", "").split("\n")
		# print(item_list)
		item = {}
		key = 0
		for i in item_list:
			try:
				if not self.isHeader(i):
					item.update({self.headers[key]: self.sanitize_item_string(i)})
			except IndexError:
				if not i.startswith("|}"):
					print(f"Error in Table {self.name}: No key {key} for {i}. Item: {item[self.headers[0]]}")
			key += 1
		return item
	@staticmethod
	def sanitize_item_string(item_text: str) -> str:
		out = re.sub(r"(?<=\[)[A-z#() ]+\||[\[\]]|(File:(.*))|[{}]|NH-", "", item_text , flags=re.IGNORECASE|re.VERBOSE)
		return re.sub(r"<br \/>", " ", out, flags=re.IGNORECASE|re.MULTILINE).replace("|", "", 1).strip()
		

def main(file) -> list:
	nextTitle = ""
	tableList = ""
	adding = False
	output = []
	with open(file) as fp:
		for line in fp:
			if adding:
				tableList += line
			if line.startswith("==="):
				nextTitle = Table.sanitize_item_string(line.replace("=", "").replace("/", " ").strip())
			if line.startswith("{|"):
				tableList += line
				adding = True
			if line.startswith("|}"):
				tmpTable = Table(tableList, nextTitle)
				output.append(tmpTable.items)
				tableList = ""
				nextTitle = ""
				adding = False
	return output
json.dump(main("table example.txt"), open("crafting.json", "w"))