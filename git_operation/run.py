import os
import shutil

version_txt = "e:/version_digit.txt"

b = os.path.exists(version_txt)
if not os.path.exists(version_txt):
    new_file = open(version_txt, "w")
    new_file.write("0")
    new_file.close()

text_file = open(version_txt, "r", encoding='utf-8', errors='ignore')
lines = text_file.read()

current_version = "0"

if len(lines) > 0:
    current_version = lines[0]

print(str(current_version))

resource_repository = "E:/test_resource/source1/flashWithJenkinsResource4/"

file_url = "aaa/ddd/c.txt"

resource_destination = "E:/package_output/"

targer_files = ["1.txt", "2.txt", "bb/c/v.txt","bb/z/fff.txt"]

for file_url in targer_files:

    slash_index = file_url.rfind("/")

    copy_to_folder = ""

    full_url = resource_repository + file_url

    if not os.path.exists(full_url):
        continue

    if slash_index == -1:
        copy_to_folder = resource_destination
    else:
        pre_folder = file_url[:slash_index]

        copy_to_folder = resource_destination + pre_folder

    if not os.path.exists(copy_to_folder):
        os.makedirs(copy_to_folder)

    shutil.copy(full_url, copy_to_folder)