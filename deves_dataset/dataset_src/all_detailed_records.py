"""Based on the "URL" field in all_wo_repeat.json and others.json, request "https://www.icloud.com/shortcuts/api/records/aa2b4bbbd4bb44ad8d8eb4f7d530ea61" to obtain the shortcut source file.

1. Request https://www.icloud.com/shortcuts/aa2b4bbbd4bb44ad8d8eb4f7d530ea61
2. Request https://www.icloud.com/shortcuts/api/records/aa2b4bbbd4bb44ad8d8eb4f7d530ea61
3. Request the downloadURL from https://www.icloud.com/shortcuts/api/records/aa2b4bbbd4bb44ad8d8eb4f7d530ea61
4. The file obtained from the downloadURL in https://www.icloud.com/shortcuts/api/records/aa2b4bbbd4bb44ad8d8eb4f7d530ea61 is a binary file. Convert it to JSON format using the biplist package.
5. Save the result to 1_all_detailed_records.json

Each final saved shortcut appears as follows:
{
    "Source": "https://matthewcassinelli.com/sirishortcuts/library/free",
    "MemberOnly": false,
    "NameINStore": "Show my Regal Unlimited Card",
    "CategoryInStore": null,
    "DescriptionInStore": "Opens the Regal website to your Unlimited account page so you can tap to reveal the QR code for your card number.",
    "Downloads": null,
    "Favorites": null,
    "Reads": null,
    "Rates": null,
    "URL": "https://www.icloud.com/shortcuts/e6fa8dd9e012484bb85c9967f0b83f02",
    "multiple": false,
    "records": {
        "created": {
        "userRecordName": "_bc43d2662d27d57a905202643637d01c",
        "timestamp": 1711823013767,
        "deviceID": "3CEEFEE1-EC52-4D27-9F59-81BF91700072"
        },
        "pluginFields": {},
        "recordType": "SharedShortcut",
        "deleted": false,
        "fields": {
        "icon": {
            "type": "ASSETID",
            "value": {
            "size": 26792,
            "fileChecksum": "AX7iZnwtB1nkHdl8/NcCfL7/TMRO",
            "downloadURL": "https://cvws.icloud-content.com/B/AX7iZnwtB1nkHdl8_NcCfL7_TMRO/${f}?o=AtV3k77520JIx_69n6o_KPTyWjYcJPW3vDK79OUwfxzckVVZq_DteQ3-jPyfWkrc7A&v=1&x=3&a=CAogKLlYNtaRkhnffr49it5GqPqwvyi20EIoWS_hIpLIH-sSexC8yv_26TEYvKfb-OkxIgEAUgT_TMROajBYuseqYl_CqXaI3xCi2mcqdnKe5zJHt2lu1koV7JZ8ehbvYuUS1kgjyGAObRrQ-oVyMGy6JwJflX9Y3KLrTh8S_dZL7ilVAjtXb3P0rzR4cu2FMEa92sOCWHmy-NX-uKa5wA&e=1712066057&fl=&r=7502267e-0357-481b-81b1-11c8ce54fd06-1&k=_&ckc=com.apple.shortcuts&ckz=_defaultZone&p=33&s=lBetKLn09o2ku8UamjLKPlsexgE"
            }
        },
        "signedShortcut": {
            "type": "ASSETID",
            "value": {
            "size": 22231,
            "downloadURL": "https://cvws.icloud-content.com/B/AV6xEPkQTR0twKp9EZNO0megzZxI/${f}?o=Aqt39yBqXb2-_xkrAC-dPNhvFGhcCAhUlIVd2yHArVNOY4EXbEhh1Ala5_0O4GbImA&v=1&x=3&a=CAog86QcagKTZ1vY8wjHeObZJSHBpvRv5baGcAyixzcGD5cSexC7yv_26TEYu6fb-OkxIgEAUgSgzZxIajBvoRULiAIQUlHDzhAwqnUxVY2LluvUelnruq6WK_DJEVdmuKND-cSSw8h3WGbzMphyML0JQ3jKc592SYOmhUbsqCvsdcFVipEaTSeitc5D6hXSE4apx9H2FpOj_TmRg0iomw&e=1712066057&fl=&r=7502267e-0357-481b-81b1-11c8ce54fd06-1&k=_&ckc=com.apple.shortcuts&ckz=_defaultZone&p=33&s=dZmVNNnym4L_wgMg1FKV1x9RyoQ",
            "fileChecksum": "AV6xEPkQTR0twKp9EZNO0megzZxI"
            }
        },
        "name": {
            "type": "STRING",
            "value": "Show my Regal Unlimited Card"
        },
        "icon_color": {
            "type": "NUMBER_INT64",
            "value": 4251333119
        },
        "shortcut": {
            "value": {
            "fileChecksum": "AZRGlbXV+PlrIHLh+fKjasSlq2KV",
            "downloadURL": "https://cvws.icloud-content.com/B/AZRGlbXV-PlrIHLh-fKjasSlq2KV/${f}?o=AgOT8iwitE4XXRIW4E6MD0xOiUaiQpGnkq2AVWGhCF3aIPvDZ1DWm0Wdpmn-G4EPZQ&v=1&x=3&a=CAogftFt4fIuUqDXyN7ePvPM_JL_fL1WmHwV2zbM5_H7DvYSexC8yv_26TEYvKfb-OkxIgEAUgSlq2KVajBjxWDhVgzeTEN4oOxkW_Sa3uOGYEnTd1SuA-cZtrMfaqAtBD_ClhJ1kaMfpg5UwN1yMHTb9CZ1FNVFC4aU6ZTV-PkoQsYa3JXmC2KgYLsORfMqqDmY7AR-n1ng_Cv9wx9s8Q&e=1712066057&fl=&r=7502267e-0357-481b-81b1-11c8ce54fd06-1&k=_&ckc=com.apple.shortcuts&ckz=_defaultZone&p=33&s=kpWKre48Kc61DCWwcgwxJy9zLxA",
            "size": 1704
            },
            "type": "ASSETID"
        },
        "maliciousScanningContentVersion": {
            "type": "NUMBER_INT64",
            "value": 1
        },
        "signingStatus": {
            "type": "STRING",
            "value": "APPROVED"
        },
        "icon_glyph": {
            "type": "NUMBER_INT64",
            "value": 59819
        },
        "signingCertificateExpirationDate": {
            "value": 1746060769000,
            "type": "TIMESTAMP"
        }
        },
        "recordChangeTag": "luef82uk",
        "modified": {
        "userRecordName": "_a702d02db102341342355d5ae64b8e07",
        "timestamp": 1711933371665,
        "deviceID": "2"
        },
        "recordName": "E6FA8DD9-E012-484B-B85C-9967F0B83F02"
    },
    "shortcut": {
      "WFWorkflowMinimumClientVersionString": "900",
      "WFWorkflowMinimumClientVersion": 900,
      "WFWorkflowIcon": {
        "WFWorkflowIconStartColor": 4251333119,
        "WFWorkflowIconGlyphNumber": 59819
      },
      "WFWorkflowClientVersion": "2510.0.2.1.3",
      "WFWorkflowOutputContentItemClasses": [],
      "WFWorkflowHasOutputFallback": false,
      "WFWorkflowActions": [
        {
          "WFWorkflowActionIdentifier": "is.workflow.actions.comment",
          "WFWorkflowActionParameters": {
            "WFCommentActionText": "Opens the Regal website to your Unlimited account page so you can tap to reveal the QR code for your card number."
          }
        },
        {
          "WFWorkflowActionIdentifier": "is.workflow.actions.url",
          "WFWorkflowActionParameters": {
            "WFURLActionURL": "https://experience.regmovies.com/unlimited",
            "UUID": "BD1FD9AE-BDDD-4FA5-994D-747D9AD1EFEC"
          }
        },
        {
          "WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
          "WFWorkflowActionParameters": {
            "WFInput": {
              "Value": {
                "OutputUUID": "BD1FD9AE-BDDD-4FA5-994D-747D9AD1EFEC",
                "Type": "ActionOutput",
                "OutputName": "URL"
              },
              "WFSerializationType": "WFTextTokenAttachment"
            },
            "UUID": "40614FA6-3618-4C4C-97E3-07757D9C1B1E"
          }
        }
      ],
      "WFWorkflowInputContentItemClasses": [
        "WFAppContentItem",
        "WFAppStoreAppContentItem",
        "WFArticleContentItem",
        "WFContactContentItem",
        "WFDateContentItem",
        "WFEmailAddressContentItem",
        "WFFolderContentItem",
        "WFGenericFileContentItem",
        "WFImageContentItem",
        "WFiTunesProductContentItem",
        "WFLocationContentItem",
        "WFDCMapsLinkContentItem",
        "WFAVAssetContentItem",
        "WFPDFContentItem",
        "WFPhoneNumberContentItem",
        "WFRichTextContentItem",
        "WFSafariWebPageContentItem",
        "WFStringContentItem",
        "WFURLContentItem"
      ],
      "WFWorkflowImportQuestions": [],
      "WFQuickActionSurfaces": [],
      "WFWorkflowTypes": [],
      "WFWorkflowHasShortcutInputVariables": false
    }
}
"""

import json
import requests
import random
import time
import os
import re
import biplist

SHORTCUT_PROJECT = os.getenv("SHORTCUT_PROJECT", "")
if SHORTCUT_PROJECT == "":
    raise Exception("The SHORTCUT_PROJECT environment variable is not set.")
SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
if SHORTCUT_DATA == "":
    raise Exception("The SHORTCUT_DATA environment variable is not set.")
src_1_path = os.path.join(SHORTCUT_DATA)

def merge():
    """Merge data from all_wo_repeat.json and others.json, removing duplicates based on the URL, with priority given to data from all_wo_repeat.json."""

    all_wo_repeat_path = os.path.join(src_1_path, "all_wo_repeat.json")
    with open(all_wo_repeat_path, "r", encoding="utf-8") as f:
        all_wo_repeat = json.load(f)

    others_path = os.path.join(src_1_path, "others.json")
    with open(others_path, "r", encoding="utf-8") as f:
        others = json.load(f)

    # Remove duplicates based on the URL, prioritizing data from all_wo_repeat.json.
    URL_set = set()
    for cur_dict in all_wo_repeat:
        URL_set.add(cur_dict["URL"])
    for cur_dict in others:
        if cur_dict["URL"] not in URL_set:
            all_wo_repeat.append(cur_dict)

    # Standardize URLs, and remove any that do not meet the criteria.
    for i in range(len(all_wo_repeat)):
        cur_dict = all_wo_repeat[i]
        URL = cur_dict["URL"]
        if URL.startswith("https://www.icloud.com/shortcuts/"):
            id = URL[33:]
            unique_id = re.match(r"^[a-zA-Z0-9]+", URL[33:]).group()
            cur_dict["URL"] = f"https://www.icloud.com/shortcuts/{unique_id}"
        else:
            del all_wo_repeat[i]

    all_detailed_records_path = os.path.join(src_1_path, "1_all_detailed_records.json")
    # with open(all_detailed_records_path, "w", encoding="utf-8") as f:
    #     json.dump(all_wo_repeat, f, ensure_ascii=False, indent=2)

def my_default(obj):
    return str(obj)

def send_request():
    """In all_wo_repeat.json, there are entries with the same URL but different names and descriptions. When sending a request, keep only one entry per URL, then duplicate the retrieved data for each corresponding URL.

    all_wo_repeat.json is sorted, with entries marked as multiple set to true grouped together.
    """

    # Read the successfully retrieved file.
    all_detailed_records_path = os.path.join(src_1_path, "1_all_detailed_records.json")
    if os.path.exists(all_detailed_records_path):
        with open(all_detailed_records_path, "r", encoding="utf-8") as f:
            all_detailed_records = json.load(f)
    else:
        print(all_detailed_records_path)
        raise Exception("The 1_all_detailed_records.json file does not exist. Please run the merge function first.")

    fail_urls = []
    store_num = 0
    cur_num = 0
    while cur_num < len(all_detailed_records):
        cur_dict = all_detailed_records[cur_num]
        print(f"Currently requesting URL number {cur_num+1} (starting from 1), with {store_num} files processed so far.")
        if cur_dict.get("records") != None and cur_dict.get("shortcut") != None:
            cur_num += 1
            continue

        url = cur_dict["URL"].strip()
        if url == None:
            cur_num += 1
            continue
        if url[-1] == "/":
            url = url[:-1]
        if url.startswith("https://www.icloud.com/shortcuts/"):
            unique_id = url.split("/")[-1]
            # Use a regular expression to extract the longest alphanumeric string from the start.
            unique_id = re.match(r"^[a-zA-Z0-9]+", unique_id).group()
            try:
                response = requests.get(f"https://www.icloud.com/shortcuts/api/records/{unique_id}")
            except:
                print(f"Currently requesting URL number {cur_num+1} (starting from 1). Request to {url} failed.")
                fail_urls.append(url)
                cur_num += 1
                continue
            if response.status_code != 200:
                print(f"Currently requesting URL number {cur_num+1} (starting from 1). Request to {url} failed.")
                fail_urls.append(url)
                cur_num += 1
                continue
            cur_dict["records"] = response.json()
            downloadURL = cur_dict["records"]["fields"]["shortcut"]["value"]["downloadURL"]
            new_response = requests.get(downloadURL)
            time.sleep(1.5 + random.random())
            if new_response.status_code != 200:
                print(f"Currently requesting URL number {cur_num+1} (starting from 1). Request to {url} failed.")
                fail_urls.append(url)
                cur_num += 1
                continue
            try:
                # Convert to JSON using the plist package and store in response_json.
                response_json = biplist.readPlistFromString(new_response.content)
                cur_dict["shortcut"] = response_json
            except:
                cur_num += 1
                fail_urls.append(url)
                continue

            multiple = cur_dict["multiple"]
            store_num += 1
            if multiple == False:
                cur_dict["get_json_from_url"] = True
                cur_num += 1
            else:
                cur_dict["get_json_from_url"] = False
                cur_num += 1
                while cur_num < len(all_detailed_records) and all_detailed_records[cur_num]["multiple"] == True and all_detailed_records[cur_num]["URL"] == url:
                    all_detailed_records[cur_num]["records"] = response.json()
                    all_detailed_records[cur_num]["shortcut"] = response_json
                    all_detailed_records[cur_num]["get_json_from_url"] = False
                    cur_num += 1
            if store_num % 100 == 0:
                print("Saving file, please do not interrupt.")
                all_detailed_records_path = os.path.join(src_1_path, "1_all_detailed_records.json")
                # with open(all_detailed_records_path, "w", encoding="utf-8") as f:
                #     json.dump(all_detailed_records, f, ensure_ascii=False, indent=2, default=my_default)
                print("File saved successfully.")
        else:
            cur_num += 1
            continue

    all_detailed_records_path = os.path.join(src_1_path, "1_all_detailed_records.json")
    # with open(all_detailed_records_path, "w", encoding="utf-8") as f:
    #     json.dump(all_detailed_records, f, ensure_ascii=False, indent=2, default=my_default)

    fail_url_path = os.path.join(src_1_path, "fail_urls.txt")
    # with open(fail_url_path, "w", encoding="utf-8") as f:
    #     for url in fail_urls:
    #         f.write(url + "\n")

if __name__=="__main__":
    # merge() # Running this will clear all files in 1_all_detailed_records.json. Proceed with caution.
    send_request()