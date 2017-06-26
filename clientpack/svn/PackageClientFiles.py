#coding=gbk
import os
import time
import sys
import shutil
import threading

SVN_PATH = "f:/test3/"
#SVN_PATH = "F:/test3/"

TEMP_FOLDER = "temp/"

current_time_folder_name = str(int(time.time()))

parent_folder = TEMP_FOLDER + current_time_folder_name + "/"

OUT_PUT_PATH = "f:/test3/output/" + current_time_folder_name

#copy modified or add resource to target folder
def _add_new_resource_files():

    os.system("svn up " + SVN_PATH)

    start_time = int(time.time())

    old_dic = _get_old_version_data_to_dic()

    new_dic = _get_new_version_data()

    need_output_files = []

    for key in new_dic:
        if not (key in old_dic):
            need_output_files.append(key)
        else:
            if new_dic[key] != old_dic[key]:
                need_output_files.append(key)

    file_count = len(need_output_files)

    if file_count == 0:
        print("warnig: ----------------notice no new file found-----------------------")
        return

    finished_count = 0

    print("start _add_new_resource_files total " + str(file_count))

    start_copy_time = int(time.time())

    for relatvie_path in need_output_files:
        output_full_path = OUT_PUT_PATH + "/" + relatvie_path

        dst_path = os.path.dirname(output_full_path)

        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        source_file = SVN_PATH + relatvie_path

        if not os.path.isfile(source_file):
            continue

        shutil.copy(source_file, dst_path)

        finished_count = finished_count + 1

        if finished_count%1000 == 0:
            now_copy_time = int(time.time())
            print("finished " + str(finished_count) + " cost " + str(now_copy_time - start_copy_time) + " seconds")

    _submit_new_files()

    #write new version file
    _wrtie_new_version_data_to_file(new_dic)

    end = int(time.time())

def _submit_new_files():

    print("start commit new files")

    start_time = int(time.time())

    os.system("svn add " + OUT_PUT_PATH)

    os.system("svn commit -m " + " add_files " +  OUT_PUT_PATH)

    end_time = int(time.time())

    print("end commit new files cost " + str(int(end_time - start_time)) + " seconds")

def _get_old_version_data_to_dic():

    dic = {}

    if os.path.exists("version.txt"):
        old_file = open("version.txt")

        old_file_lines = old_file.readlines()

        for old_line in old_file_lines:
            temp = old_line.replace("\n", "").split(" ")

            if len(temp) == 2:
                dic[temp[0]] = temp[1]

    return dic


#write new version info to txt
def _wrtie_new_version_data_to_file(dic):
    ret_file = open("version.txt", "w")

    ret_dic = sorted(dic.items(), key=lambda d: d[0], reverse=False)

    temp_count = 0

    for t_path in ret_dic:
        temp_count = temp_count + 1

        if temp_count < len(ret_dic):
             ret_file.write(t_path[0] + " " + t_path[1] + "\n")
        else:
            ret_file.write(t_path[0] + " " + t_path[1])

    ret_file.close()


def _get_new_version_data():

    start_time = int(time.time())

    os.system("rd /s /q temp")

    recursive_folder = ["effect", "entity", "images", "loading","sound","ui", "map"]

    one_folder = ["map"]

    temp_time = int(time.time())

    last_time = 0

    ret_dic = {}

    function_start_time = int(time.time())

    for recursive_path in recursive_folder:

        recursive_start_time = int(time.time())

        print("_create_new_version_file start run folder " + recursive_path)

        file_name = parent_folder + recursive_path + ".txt"

        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        if not os.path.exists(file_name):
            create_file = open(file_name, "w")
            create_file.close()

        if recursive_path in one_folder:
            os.system("svn list " + SVN_PATH + recursive_path + " -v >> " + file_name)
        else:
            os.system("svn list " + SVN_PATH + recursive_path + " -v --recursive >> " + file_name)

        _write_new_revision_dic(file_name, recursive_path, ret_dic)

        recursive_end_time = int(time.time())

        print("_create_new_version_file end run folder " + recursive_path + " cost " + str(recursive_end_time - recursive_start_time) + " seconds")


    function_end_time = int(time.time())

    print("_get_new_version_data cost " + str(function_end_time - function_start_time) + " seconds")

    return ret_dic

def _write_new_revision_dic(file_path, recursive_path, dic):

    #load new outout revision file

    full_path = sys.path[0].replace("\\", "/") + "/" + file_path

    r_slash_index = full_path.rfind("/")

    if r_slash_index != -1:
        parent_folder_path  =  os.path.dirname(full_path)

        if not os.path.exists(parent_folder_path):
            os.makedirs(parent_folder_path)

    if not os.path.exists(full_path):
        file = open(full_path, 'w')
        file.close()

    file_object = open(file_path)

    #effect entity
    type_folder = recursive_path + "/"

    try:
        lines = file_object.readlines()

        for one_line in lines:
            line_data = one_line.strip().split(" ")

            revision = line_data[0]

            relative_path = line_data[len(line_data) - 1]

            if (relative_path == "./"):
                continue

            if recursive_path == "map":
                if (relative_path.find(".") != -1):
                    continue
            else:
                if (relative_path.find(".") == -1):
                    continue

            dic[type_folder + relative_path] = revision

    finally:
        file_object.close()

    return dic

start_run_time = int(time.time())

_add_new_resource_files()

end_run_time = int(time.time())

print("finish running cost " + str(end_run_time - start_run_time) + " seconds")
#_get_new_revision_dic()



