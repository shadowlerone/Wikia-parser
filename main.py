import re
import json
import forFT

pattern = re.compile(
	r"(\{\{TableContent(Bugs){0,1}\|type=((bug)|(fish))\n((\|).*\n){0,20}\}\})", re.IGNORECASE|re.MULTILINE)


def months(i):
	if i == "+":
		return 1
	else:
		return 0

bug_key = 0

fish_key = 0


def bug_to_dict(NorthText, SouthText):
	Northtmp = NorthText.replace("| ", "").replace("[[", "").replace("]]", "").replace(
		"{{", "").replace("}}", "").split("\n")
	Southtmp = SouthText.replace("| ", "").replace("[[", "").replace("]]", "").replace(
		"{{", "").replace("}}", "").split("\n")
	name = Northtmp[1]
	habitat = Northtmp[4]
	time = Northtmp[5].replace("<small>", "").replace("</small>","")
	# print(Northtmp)
	# print(Northtmp[5])
	# print(time)
	try:
		price = int(Northtmp[3].replace(",", ""))
	except:
		price = None
	if time == "all day":
		times = []
	else:
		times = []
		x = time.split("&")
		for i in x:
			sa, en = i.split(" - ")
			sax = sa.strip().split(" ")
			ene = en.strip().split(" ")
			# print(f"sa:{sa}, en:{en}, sax:{sax}, ene:{ene}")
			if sax[1] == "pm":
				s = int(sax[0]) + 12
			else:
				s = int(sax[0])
			if ene[1] == "pm":
				e = int(ene[0]) + 12
			else:
				e = int(ene[0])
			times.append({"start":s, "end":e})
	# print(Northtmp[6:18])
	nM = list(map(months, Northtmp[6:18]))
	sM = list(map(months, Southtmp[6:18]))
	json_template = {
		"id": f"b{str(bug_key).zfill(4)}",
		"name": name,
		"habitat": habitat,
		"times":times,
		"price":price,
		"northernMonths": nM,
		"southernMonths": sM,
	}
	return json_template

def fish_to_dict(NorthText, SouthText):
	global fish_key
	Northtmp = NorthText.replace("| ", "").replace("[[", "").replace("]]", "").replace(
		"{{", "").replace("}}", "").split("\n")
	Southtmp = SouthText.replace("| ", "").replace("[[", "").replace("]]", "").replace(
		"{{", "").replace("}}", "").split("\n")
	name = Northtmp[1]
	if Northtmp[1].lower() != Southtmp[1].lower():
		# print(f"{Northtmp[1]} not {Southtmp[1]}")
		raise TypeError
	habitat = Northtmp[4]
	time = Northtmp[6].replace("<small>", "").replace("</small>","")
	# print(time)
	if time == "all day":
		times = []
	else:
		times = []
		x = time.split("&")
		for i in x:
			sa, en = i.split(" - ")
			sax = sa.strip().split(" ")
			ene = en.strip().split(" ")
			# print(f"sa:{sa}, en:{en}, sax:{sax}, ene:{ene}")
			if sax[1] == "pm":
				s = int(sax[0]) + 12
			else:
				s = int(sax[0])
			if ene[1] == "pm":
				e = int(ene[0]) + 12
			else:
				e = int(ene[0])
			times.append({"start":s, "end":e})
	size = Northtmp[5]
	price = int(Northtmp[3].replace(',', ""))
	# print(Northtmp[7:19])
	nM = list(map(months, Northtmp[7:19]))
	sM = list(map(months, Southtmp[7:19]))
	json_template = {
		"id": f"f{str(fish_key).zfill(4)}",
		"name": name,
		"habitat": habitat,
		"size": size,
		"price":price,
		"times":times,
		"northernMonths": nM,
		"southernMonths": sM,
	}
	return json_template

def fish_to_json(NorthList, SouthList):
	fish = []
	global fish_key
	for value in NorthList:
		fish.append(fish_to_dict(value[0], SouthList[fish_key][0]))
		fish_key += 1
	return fish

def bug_to_json(NorthList, SouthList):
	bug = []
	global bug_key
	for value in NorthList:
		bug.append(bug_to_dict(value[0], SouthList[bug_key][0]))
		bug_key += 1
	return bug

def main():
	items = forFT.main()
	NorthFish = open("inputs/NorthFish.txt").read().lower()
	NorthFishList = pattern.findall(NorthFish)
	SouthFish = open("inputs/SouthFish.txt").read().lower()
	SouthFishList = pattern.findall(SouthFish)
	NorthBug = open("inputs/NorthBug.txt").read().lower()
	NorthBugList = pattern.findall(NorthBug)
	SouthBug = open("inputs/SouthBug.txt").read().lower()
	SouthBugList = pattern.findall(SouthBug)
	js = {
		"fish":fish_to_json(NorthFishList, SouthFishList),
		"bugs": bug_to_json(NorthBugList, SouthBugList),
		"items": items
	}
	json.dump(js, open("out/FT/data.json", "w"))
	return js
	



# NorthFishList = re.findall(r"(\{\{TableContent(Bugs){0,1}\|type=((bug)|(fish))\n((\|).*\n){0,20}\}\})", NorthFish)
if __name__ == "__main__":
	main()
	# print(main())
