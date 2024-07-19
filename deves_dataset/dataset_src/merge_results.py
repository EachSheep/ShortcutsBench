"""Merge duplicate data based on `1_all_detailed_records.json`, retaining only unique iCloud data entries. The final data is saved as `1_final_detailed_records.json`.

This involves merging entries such as:

```json
{
  "Source": "https://matthewcassinelli.com/sirishortcuts/library/free",
  "MemberOnly": false,
  "NameINStore": "Show my Regal Unlimited Card",
  "CategoryInStore": null,
  "DescriptionInStore": "Opens the Regal website to your Unlimited account page so you can tap to reveal the QR code for your card number.",
  "Downloads": null,
  "Favorites": null,
  "Reads": null,
  "Rates": null
}
```

In other words, deduplication is performed for all fields except for "URL", "records", and "shortcut".
"""

import json
import os

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
if SHORTCUT_DATA == "":
    raise Exception("The SHORTCUT_DATA environment variable is not set.")

all_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_all_detailed_records.json")
dump_file_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records.json")

with open(all_detailed_records_path, "r") as f:
    all_detailed_records = json.load(f)
before_cnt = len(all_detailed_records)


cur_dict = {}
cur_dicts = []
cnt = 0
for (record, next_record) in zip(all_detailed_records, all_detailed_records[1:]):
    Source = record.get("Source", None)
    MemberOnly = record.get("MemberOnly", None)
    NameINStore = record.get("NameINStore", None)
    CategoryInStore = record.get("CategoryInStore", None)
    DescriptionInStore = record.get("DescriptionInStore", None)
    Downloads = record.get("Downloads", None)
    Favorites = record.get("Favorites", None)
    Reads = record.get("Reads", None)
    Rates = record.get("Rates", None)
    URL = record.get("URL", None)
    get_json_from_url = record.get("get_json_from_url", None)
    multiple = record.get("multiple", None)
    records = record.get("records", None)
    shortcut = record.get("shortcut", None)
    # Check for Additional Fields in the Dictionary
    for key in record.keys():
        if key not in ["Source", "MemberOnly", "NameINStore", "CategoryInStore", "DescriptionInStore", "Downloads", "Favorites", "Reads", "Rates", "URL", "get_json_from_url", "multiple", "records", "shortcut"]:
            raise Exception(f"Additional: {key}, {record[key]}")

    if "URL" in next_record and URL == next_record["URL"]:
        if not cur_dict:
            cur_dict = {
                "Source": [Source],
                "MemberOnly": [MemberOnly],
                "NameINStore": [NameINStore],
                "CategoryInStore": [CategoryInStore],
                "DescriptionInStore": [DescriptionInStore],
                "Downloads": [Downloads],
                "Favorites": [Favorites],
                "Reads": [Reads],
                "Rates": [Rates],
                "URL": URL,
                "records": records,
                "shortcut": shortcut
            }
        else:
            cur_dict["Source"].append(Source)
            cur_dict["MemberOnly"].append(MemberOnly)
            cur_dict["NameINStore"].append(NameINStore)
            cur_dict["CategoryInStore"].append(CategoryInStore)
            cur_dict["DescriptionInStore"].append(DescriptionInStore)
            cur_dict["Downloads"].append(Downloads)
            cur_dict["Favorites"].append(Favorites)
            cur_dict["Reads"].append(Reads)
            cur_dict["Rates"].append(Rates)
    else:
        if not cur_dict:
            cur_dict = {
                "Source": [Source],
                "MemberOnly": [MemberOnly],
                "NameINStore": [NameINStore],
                "CategoryInStore": [CategoryInStore],
                "DescriptionInStore": [DescriptionInStore],
                "Downloads": [Downloads],
                "Favorites": [Favorites],
                "Reads": [Reads],
                "Rates": [Rates],
                "URL": URL,
                "records": records,
                "shortcut": shortcut
            }
        else:
            cur_dict["Source"].append(Source)
            cur_dict["MemberOnly"].append(MemberOnly)
            cur_dict["NameINStore"].append(NameINStore)
            cur_dict["CategoryInStore"].append(CategoryInStore)
            cur_dict["DescriptionInStore"].append(DescriptionInStore)
            cur_dict["Downloads"].append(Downloads)
            cur_dict["Favorites"].append(Favorites)
            cur_dict["Reads"].append(Reads)
            cur_dict["Rates"].append(Rates)

        cur_dict["Source"] = list(set(cur_dict["Source"]))
        cur_dict["MemberOnly"] = list(set(cur_dict["MemberOnly"]))
        cur_dict["NameINStore"] = list(set(cur_dict["NameINStore"]))
        cur_dict["CategoryInStore"] = list(set(cur_dict["CategoryInStore"]))
        cur_dict["DescriptionInStore"] = list(set(cur_dict["DescriptionInStore"]))
        cur_dict["Downloads"] = list(set(cur_dict["Downloads"]))
        cur_dict["Favorites"] = list(set(cur_dict["Favorites"]))
        cur_dict["Reads"] = list(set(cur_dict["Reads"]))
        cur_dict["Rates"] = list(set(cur_dict["Rates"]))
        cur_dicts.append(cur_dict)
        cur_dict = {}
        cnt += 1
        if cnt % 100 == 0:
            print(f"{cnt} records have been processed.")

# with open(dump_file_path, "w") as f:
#     json.dump(cur_dicts, f, indent=4)

print(f"The data contained {before_cnt} records before merging.")
print(f"The merged data is saved in {dump_file_path}, containing a total of {cnt} records.")