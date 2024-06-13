# import os

# def insert_line():
#     for root, dirs, files in os.walk('.'):
#         for file in files:
#             if file == 'README.md':
#                 filepath = os.path.join(root, file)
#                 with open(filepath, 'r', encoding='utf-8') as f:
#                     lines = f.readlines()
#                 lines.insert(1, '\n## Read in [中文](README_ZH.md)\n')
#                 with open(filepath, 'w', encoding='utf-8') as f:
#                     f.writelines(lines)

# insert_line()
import os

def remove_duplicate_line():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'README.md':
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                duplicate_line = '## Read in [中文](README_ZH.md)\n'
                while lines.count(duplicate_line) > 1:
                    lines.remove(duplicate_line)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

remove_duplicate_line()