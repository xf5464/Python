import os
import shutil
import sys
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import zlib
import svn
import svn.local
from xml.etree.ElementTree import SubElement


from git import Repo

DEBUG_MODE = 2

'''if DEBUG_MODE == 1:
    git_path = "C:/Program Files/Git/bin/git.exe"
else:
    git_path = sys.argv[2]

os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path'''

_start_version_num = "0"

if DEBUG_MODE == 1:
    _flash_repository = "E:/flashWithJenkinsDemo"

    _version_xml_path = "e:/version/version.xml"

    _version_data_path = "E:/package_output/version.data"

    _version_txt = "e:/version_digit.txt"

    _resource_repository = "E:/test_resource/source2/flashWithJenkinsResource/"

    _resource_destination = "E:/package_output"

else:

    _flash_repository = sys.argv[1]

    _version_xml_path = sys.argv[3]

    _version_data_path = sys.argv[4]

    _version_txt = sys.argv[5]

    _resource_repository = sys.argv[6]

    _resource_destination = sys.argv[7]

print("---------------------start init variables------------------------")

print(" _flash_repository:" + _flash_repository + "\n"
      + " _version_xml_path:" + _version_xml_path + "\n"
      + " _version_data_path:" + _version_data_path + "\n"
      + " _version_txt:" + _version_txt + "\n"
      + " _resource_repository:" + _resource_repository + "\n"
      + " _resource_destination:" + _resource_destination + "\n")

print("---------------------end init variables------------------------")


# flash_repository = "E:/flashWithJenkinsDemo"


def _check_file_path_and_create_dir(file_url):
    slash_index = file_url.rfind("/")

    if slash_index == -1:
        return
    else:
        pre_folder = file_url[:slash_index]

        if not os.path.exists(pre_folder):
            os.makedirs(pre_folder)

def _fetch_new_svn_files(svn_resource_repository):
    local_client = svn.local.LocalClient(svn_resource_repository)
    info = local_client.info()
    old_revision = info.get("entry_revision")

    local_client.update()

    new_info = local_client.info()
    new_rivision = new_info.get("entry_revision")

    svn_diff_files = local_client.diff_summary(old_revision, new_rivision)

    ret = []

    for obj in svn_diff_files:
        if obj.get("kind") == "dir":
            continue
        # .replace(svn_resource_repository, "")
        if obj.get("item") == "modified" or obj.get("item") == "added":
            relative_url = obj.get("path").replace("\\", "/")
            relative_url = relative_url.replace(svn_resource_repository, "")
            ret.append(relative_url)
            print(relative_url)

    return ret

def _fetch_new_files(resource_repository):
    repo = Repo(resource_repository)

    if len(repo.heads) > 0:
        old_head_sha = repo.git.rev_parse("HEAD")

        repo.remotes.origin.pull()

        new_head_sha = repo.git.rev_parse("HEAD")

        diff_files = repo.git.diff(old_head_sha + ".." + new_head_sha, name_only=True, diff_filter="ACMRT")

        if diff_files != "":
            targer_files = diff_files.split("\n")
        else:
            targer_files = []

    else:
        repo.remotes.origin.pull()

        new_head_sha = repo.git.rev_parse("HEAD")

        diff_files2 = repo.git.whatchanged(new_head_sha, no_notes=True, pretty="oneline",
                                           name_only=True, diff_filter="ACMRT")

        targer_files = diff_files2.split("\n")

        del targer_files[0]

    return targer_files


def _copy_files(targer_files, resource_repository, resource_destination):
    # copy files to destination
    for file_url in targer_files:

        slash_index = file_url.rfind("/")

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

        try:
            shutil.copy(full_url, copy_to_folder)
        except PermissionError as e:
            print("PermissionError _copy_files:" + "url:" + full_url + " copy_to_folder:" + copy_to_folder)


def _get_current_version_num(version_txt):
    # get current version
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
    # get current version

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

    current_version += 1

    write_file = open(version_txt, "w", encoding='utf-8', errors='ignore')
    write_file.write(str(current_version))
    write_file.close()


def _update_version_txt(target_files, version_num, version_xml_path, version_data_path):

    new_file_dic = {}

    old_file_dic = {}

    for file_url in target_files:
        new_file_dic[file_url] = version_num


    if os.path.exists(version_xml_path):

        old_file =  open(version_xml_path, "r", encoding='utf-8', errors='ignore')
        old_lines = old_file.read()

        if len(old_lines) > 0:
            tree = xml.etree.ElementTree.parse(version_xml_path)

            # root = tree.getroot()

            file_elements = tree.findall('f')

            for atype in file_elements:
                file_path = atype.get('n')

                old_file_dic[file_path] = atype.get("v")

    out_put_dic = {}

    for old_key in old_file_dic:
        if new_file_dic.get(old_key) is None:
            out_put_dic[old_key] = old_file_dic.get(old_key)
        else:
            if "Scene/" not in old_key:
                out_put_dic[old_key] = new_file_dic.get(old_key)

    for new_key in new_file_dic:
        if "Scene/" not in new_key:
            out_put_dic[new_key] = new_file_dic.get(new_key)

    new_root = ET.Element('root')

    for output_key in out_put_dic:
        new_element = SubElement(new_root, "f", {"n":output_key, "v":out_put_dic.get(output_key)})

    _check_file_path_and_create_dir(version_xml_path)

    new_tree = ET.ElementTree(new_root)
    new_tree.write(version_xml_path)

    # write to dat file
    data_xml_file = open(version_xml_path, "r", encoding='utf-8', errors='ignore')
    lines = data_xml_file.read()
    data_xml_file.close()

    compressed_string = zlib.compress(lines.encode("utf-8"), 9)

    _check_file_path_and_create_dir(version_data_path)

    target_dat_file = open(version_data_path, "wb")
    target_dat_file.write(compressed_string)
    target_dat_file.close()

print("start _fetch_new_svn_files")

_targer_files = _fetch_new_svn_files(_resource_repository)

print("changed files num:" + str(len(_targer_files)))

if (len(_targer_files)) > 0:
    _copy_files(_targer_files, _resource_repository, _resource_destination)

    _new_version_num = _get_current_version_num(_version_txt)

    _update_version_txt(_targer_files, _new_version_num, _version_xml_path, _version_data_path)

    _add_current_version_num(_version_txt)

'''old_head_sha = "7d0719749badc11276a830deceaabdf0071a0547"
new_head_sha = "45eed597a063221297899e9c128f2be49db95368"

repo = Repo(_resource_repository)
diff1 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="A")
diff2 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="D")
diff3 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="M")
diff4 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="ACMRT")
diff5 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="R")'''
