import os
import shutil
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

import winreg
import sys
import zlib

git_path = "C:/Program Files/Git/bin/git.exe"
#git_path = sys.argv[2]

os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path

'''r = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
k = winreg.OpenKey(r, r'SOFTWARE\GitForWindows')
install_path = winreg.QueryValueEx(k, 'InstallPath')[0]
git_path = os.path.join(install_path, 'bin/git.exe')
assert os.path.exists(git_path), "Git path not found"
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path'''


from git import Repo
#https://pypi.python.org/pypi/GitPython

import git
# rorepo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with

_flash_repository = "E:/flashWithJenkinsDemo"

_version_txt = "e:/version_digit.txt"

_resource_destination = "E:/package_output"

_version_xml_path = "e:/version/version.xml"

_version_data_path = "E:/package_output/version.data"

_resource_repository = "E:/test_resource/source1/flashWithJenkinsResource4/"#sys.argv[6]

_start_version_num = "0"

'''flash_repository = sys.argv[1]  #"E:/flashWithJenkinsDemo"

version_txt = sys.argv[5]

resource_repository = "E:/test_resource/source1/flashWithJenkinsResource2"#sys.argv[6]

resource_destination = sys.argv[7]'''

print("resource_repository:" + _flash_repository)

#flash_repository = "E:/flashWithJenkinsDemo"

def _checkFilePathAndCreateDir(file_url):
    slash_index = file_url.rfind("/")

    if slash_index == -1:
        return
    else:
        pre_folder = file_url[:slash_index]

        if not os.path.exists(pre_folder):
            os.makedirs(pre_folder)

def _fetch_new_files(resource_repository):
    repo = Repo(resource_repository)

    targer_files = []

    if len(repo.heads) > 0:
        old_head_sha = repo.git.rev_parse("HEAD")

        repo.remotes.origin.pull()

        new_head_sha = repo.git.rev_parse("HEAD")

        diff_files = repo.git.diff(old_head_sha + ".." + new_head_sha, name_only=True, diff_filter="AD")

        targer_files = diff_files.split("\n")

    else:
        repo.remotes.origin.pull()

        new_head_sha = repo.git.rev_parse("HEAD")

        diff_files2 = repo.git.whatchanged(new_head_sha, no_notes=True, pretty="oneline", name_only=True,diff_filter="AD")

        targer_files = diff_files2.split("\n")

        del targer_files[0]

    return targer_files

def _copy_files(targer_files, resource_repository, resource_destination):
    #copy files to destination
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

def _get_current_version_num(version_txt):
    #get current version
    b = os.path.exists(version_txt)

    if not os.path.exists(version_txt):
        new_file = open(version_txt, "w")
        new_file.write(_start_version_num)
        new_file.close()

    text_file = open(version_txt, "r", encoding='utf-8', errors='ignore')
    lines = text_file.read()

    current_version = _start_version_num

    if len(lines) > 0:
        current_version = lines[0]

    return current_version

def _add_current_version_num(version_txt):
    #get current version
    b = os.path.exists(version_txt)

    if not os.path.exists(version_txt):
        new_file = open(version_txt, "w")
        new_file.write(_start_version_num)
        new_file.close()

    text_file = open(version_txt, "r", encoding='utf-8', errors='ignore')
    lines = text_file.read()
    text_file.close()

    current_version = int(_start_version_num)

    if len(lines) > 0:
        current_version = int(lines[0])

    current_version = current_version + 1

    write_file = open(version_txt, "w", encoding='utf-8', errors='ignore')
    write_file.write(current_version)
    write_file.close()

def _update_version_txt(target_files,version_num,version_xml_path, version_data_path):

    new_file_dic = {}

    old_file_dic = {}

    for file_url in target_files:
        new_file_dic[file_url] = version_num

    if os.path.exists(version_xml_path):
        tree = xml.etree.ElementTree.parse(version_xml_path)

        root = tree.getroot()

        file_elements = tree.findall('f')

        for atype in file_elements:
            file_path = atype.get('n')

            old_file_dic[file_path] = atype.get("v")

    out_put_dic = {}

    for old_key in old_file_dic:
        if new_file_dic[old_key] is None:
            out_put_dic[old_key] = old_file_dic.get(old_key)
        else:
            if  not "Scene/" in old_key:
                 out_put_dic[old_key] = new_file_dic.get(old_key)

    for new_key in new_file_dic:
        if not "Scene/" in new_key:
            out_put_dic[new_key] = new_file_dic.get(new_key)

    new_root = ET.Element('root')

    for output_key in out_put_dic:
        new_element = SubElement(new_root, {"f":output_key, "v":out_put_dic.get(output_key)})

    _checkFilePathAndCreateDir(version_xml_path)

    new_tree = ET.ElementTree(new_root)
    new_tree.write(version_xml_path)

    #write to dat file
    data_xml_file = open(version_xml_path, "r", encoding='utf-8', errors='ignore')
    lines = data_xml_file.read()
    data_xml_file.close()

    compressed_string = zlib.compress(lines.encode("utf-8"), 9)

    _checkFilePathAndCreateDir(version_data_path)

    target_dat_file = open(version_data_path, "wb")
    target_dat_file.write(compressed_string)
    target_dat_file.close()

_targer_files = _fetch_new_files(_resource_repository)

_copy_files(_targer_files, _resource_repository, _resource_destination)

_new_version_num = _get_current_version_num(_version_txt)

_update_version_txt(_targer_files, _new_version_num, _version_txt, _version_data_path)

_add_current_version_num(_version_txt)

'''diff1 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="A")
diff2 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="D")
diff3 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="M")
diff4 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="AD")
diff5 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="R")'''
