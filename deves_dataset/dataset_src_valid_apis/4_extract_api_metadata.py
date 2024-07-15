import os
import json
from collections import defaultdict
import xml.etree.ElementTree as ET

SHORTCUT_PROJECT = os.getenv("SHORTCUT_PROJECT", "")
if SHORTCUT_PROJECT == "":
    raise Exception("The SHORTCUT_PROJECT environment variable is not set.")
SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
if SHORTCUT_DATA == "":
    raise Exception("The SHORTCUT_DATA environment variable is not set.")

succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_api_json_filter.json")
# succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_succ_api_json_filter.json")
# succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_fail_api_json_filter.json")

app_dir_path = os.path.join(SHORTCUT_DATA, "ToGetAPIs", "ios-free-apps")
# app_dir_path = os.path.join(SHORTCUT_DATA, "ToGetAPIs", "mac-free-apps")
# app_dir_path = os.path.join(SHORTCUT_DATA, "ToGetAPIs", "mac-system-apps")
# app_dir_path = os.path.join(SHORTCUT_DATA, "ToGetAPIs", "tmp")

def sort_dict(obj):
    if isinstance(obj, dict):
        # Filter out key-value pairs where the value is None, and convert keys of type NoneType to empty strings.
        filtered_items = [(key if key is not None else "", value) for key, value in obj.items() if value is not None]
        sorted_obj = {key: sort_dict(value) for key, value in sorted(filtered_items)}
        return sorted_obj
    elif isinstance(obj, list):
        sorted_list = [sort_dict(item) for item in obj if item is not None]
        return sorted_list
    else:
        return obj
    
def parse_element(element):
    """Recursively parse XML elements, returning dictionaries and lists.
    """
    if element.tag == 'dict':
        return {element[i].text: parse_element(element[i+1]) for i in range(0, len(element), 2)}
    elif element.tag == 'array':
        return [parse_element(child) for child in element]
    elif element.tag == 'true':
        return True
    elif element.tag == 'false':
        return False 
    elif element.tag == 'integer':
        return int(element.text)
    elif element.tag == 'string':
        return element.text
    elif element.tag == 'real':
        return float(element.text)
    else:
        raise ValueError("Unsupported tag: " + element.tag)
    
    
def process_actionsdata(folder_path, data_dict, apidata_cnt):
    # Traverse the directory.
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.actionsdata'):
                file_path = os.path.join(root, file)
                # Determine the identifier based on the keywords in the path.
                identifier = get_identifier(root, file)
                # Handle files with the same name.
                if identifier in data_dict:
                    apidata_cnt[identifier] += 1
                    identifier += f'.{apidata_cnt[identifier]}'
                # Extract file information.
                with open(file_path, 'r') as f:
                    data = json.load(f)
                # Sort the data in lexicographical order by keys.
                sorted_data = sort_dict(data)
                # Store information
                data_dict[identifier] = sorted_data
                
                
def process_intentdata(folder_path, data_dict, apidata_cnt):
    # Traverse the directory.
    for root, dirs, files in os.walk(folder_path):
        for file in files:

            if file.endswith('.intentdefinition'):
                file_path = os.path.join(root, file)
                # Identify based on keywords in the path.
                identifier = get_identifier(root, file)
                # Handle files with identical names.
                if identifier in data_dict:
                    apidata_cnt[identifier] += 1
                    identifier += f'.{apidata_cnt[identifier]}'
                try:
                    # Parse XML files.
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()
                    parsed_data = parse_element(root_element[0])
                    data = parsed_data
                    sorted_data = sort_dict(data)
                    # Store data.
                    data_dict[identifier] = sorted_data
                except ET.ParseError as e:
                    raise ValueError(f"Failed to parse XML {file_path}: {str(e)}")
                except Exception as e:
                    raise ValueError(f"Failed to convert {file_path}: {str(e)}")


def get_identifier(root, file):
    if ('.app/Watch') in root and ('PlugIns' in root):
        return f"Watch.PlugIns.{file}"
    if '.app/PlugIns' in root:
        return f"PlugIns.{file}"
    elif '.app/Watch' in root:
        return f"Watch.{file}"
    elif '.app' in root:
        return file
    else:
        print(root)
        raise ValueError("Unexpected actionsdata file found in a non-standard directory.")

def main():

    with open(succ_api_json_path, 'r', encoding='utf-8') as file:
        succ_api_json = json.load(file)

    folder_path = app_dir_path

    # Retrieve all entries in the directory.
    entries = os.listdir(folder_path)
    # Filter out the subdirectories.
    subfolders = [entry for entry in entries if (os.path.isdir(os.path.join(folder_path, entry)))]
    # print(subfolders)
    for subfolder in subfolders:
            # Construct subdirectory paths with 'subfolder' as the app name.
            subfolder_path = os.path.join(folder_path, subfolder)
            # Process the directory
            # Initialize data structures
            actionsdata_dict = defaultdict(dict)
            apidata_cnt = defaultdict(int)
            process_actionsdata(subfolder_path, actionsdata_dict, apidata_cnt)
            intentdata_dict = defaultdict(dict)
            intentdata_count = defaultdict(int)
            process_intentdata(subfolder_path, intentdata_dict, intentdata_count)

            # Store in a JSON file.
            for app in succ_api_json:
                if app["AppName"]== subfolder:
                    app.update(actionsdata_dict)
                    app.update(intentdata_dict)

    # Write the data to a file.
    with open(succ_api_json_path, 'w') as f:
        json.dump(succ_api_json, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()