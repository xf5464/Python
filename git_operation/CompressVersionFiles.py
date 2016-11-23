import os
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import zlib
from xml.etree.ElementTree import SubElement


def _checkFilePathAndCreateDir(file_url):
    slash_index = file_url.rfind("/")

    if slash_index == -1:
        return
    else:
        pre_folder = file_url[:slash_index]

        if not os.path.exists(pre_folder):
            os.makedirs(pre_folder)

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
        new_element = SubElement(new_root, "f", {"n":output_key, "v":out_put_dic.get(output_key)})

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

target_files = ["1.txt","2.txt","bb/c/v.txt","bb/z/fff.txt"]

_update_version_txt(target_files,"1","f:/version.xml","f/version.dat")
