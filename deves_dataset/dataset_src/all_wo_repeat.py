"""Merge data from all other JSON files into a single file (excluding others.json), ensuring no duplicates, and save it as all_wo_repeat.json.
"""

import json
import os

SHORTCUT_PROJECT = os.getenv("SHORTCUT_PROJECT", "")
if SHORTCUT_PROJECT == "":
    raise Exception("The SHORTCUT_PROJECT environment variable is not set.")
src1_dir = os.path.join(SHORTCUT_PROJECT, "deves_dataset/dataset_src/")

excluded_names = ["example.com.json", "all_wo_repeat.json", "others.json", "1_all_detailed_records.json"]

file_names = os.listdir(src1_dir)
file_names = [i for i in file_names if i.endswith(".json") and i not in excluded_names]
print(file_names)

def judge_all_equal(a, b):
	"""Recursively check if all elements in the dictionary or list are equal
	a: dict or list
	b: dict or list
	"""

	if type(a) != type(b):
		return False
	if isinstance(a, dict):
		for key in a:
			if key not in b:
				continue
			if not judge_all_equal(a[key], b[key]):
				return False
		return True
	elif isinstance(a, list):
		for i in range(len(a)):
			if not judge_all_equal(a[i], b[i]):
				return False
		return True
	else:
		return a == b


all_data_dict = {}
URL_set = set()
for file_name in file_names:
	file_path = os.path.join(src1_dir, file_name)
	with open(file_path, "r", encoding="utf-8") as f:
		data = json.load(f)
	
	for d in data:
		Source = d["Source"]
		if Source == None:
			continue
		Source = Source.strip()
		if Source[-1] == "/":
			Source = Source[:-1]
		d["Source"] = Source

		URL = d["URL"]
		if URL == None:
			continue
		URL = URL.strip()
		if URL == "":
			continue
		if URL[-1] == "/":
			URL = URL[:-1]
		d["URL"] = URL
		if URL.startswith("https://www.icloud.com/shortcuts/"):
			URL = URL[33:]
			if URL not in URL_set:
				URL_set.add(URL)
				all_data_dict[URL] = [d]
			else:
				already_have = False
				tmp_dicts = all_data_dict[URL].copy()
				tmp_dict2 = d.copy()
				if 'Downloads' in tmp_dict2:
					tmp_dict2.pop('Downloads')
				if 'Favorites' in tmp_dict2:
					tmp_dict2.pop('Favorites')
				if 'Reads' in tmp_dict2:
					tmp_dict2.pop('Reads')
				if 'Rates' in tmp_dict2:
					tmp_dict2.pop('Rates')
				for tmp_dict1 in tmp_dicts:
					if 'Downloads' in tmp_dict1:
						tmp_dict1.pop('Downloads')
					if 'Favorites' in tmp_dict1:
						tmp_dict1.pop('Favorites')
					if 'Reads' in tmp_dict1:
						tmp_dict1.pop('Reads')
					if 'Rates' in tmp_dict1:
						tmp_dict1.pop('Rates')

					if judge_all_equal(tmp_dict1, tmp_dict2):
						already_have = True
						break
				if not already_have:
					all_data_dict[URL].append(d)
		else:
			continue

# Convert all_dict_data to a list.
all_data = []
for URL in all_data_dict:
	if len(all_data_dict[URL]) == 1:
		all_data_dict[URL][0]["multiple"] = False
		all_data.extend(all_data_dict[URL])
	else:
		for cur_data_dict in all_data_dict[URL]:
			cur_data_dict["multiple"] = True
		all_data.extend(all_data_dict[URL])

all_wo_repeat_path = os.path.join(src1_dir, "all_wo_repeat.json")
# with open(all_wo_repeat_path, "w", encoding="utf-8") as f:
# 	json.dump(all_data, f, ensure_ascii=False, indent=2)