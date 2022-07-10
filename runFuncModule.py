import os, time,glob
import configparser


def get_list_we_have():
    path = r'C:\SVSHARE\CompareFiles\test1'
    ids_list = []
    we_have_list = []
    for line in open(path, encoding="utf8"):
        if '"_id"' in line:
            new = line.split(':')
            ids_list.append(new[1])
    for i in range(len(ids_list)):
        ids_list[i] = ids_list[i].replace(' "', '')
        ids_list[i] = ids_list[i].replace('",\n', '')
    dir_to_get_files = r"C:\SVSHARE\CompareFiles\AllFiles"
    sub_dir_files = [x[0] for x in os.walk(dir_to_get_files)]
    for name in ids_list:
        for i in range(len(sub_dir_files)):
            if name in sub_dir_files[i]:
                if not (name in we_have_list):
                    we_have_list.append(name)
                    break
    return we_have_list


def get_list_to_download():
    path = r'C:\SVSHARE\CompareFiles\test1'
    ids_list = []
    to_download_list = []
    for line in open(path, encoding="utf8"):
        if '"_id"' in line:
            new = line.split(':')
            ids_list.append(new[1])
    for i in range(len(ids_list)):
        ids_list[i] = ids_list[i].replace(' "', '')
        ids_list[i] = ids_list[i].replace('",\n', '')
    dir_to_get_files = r"C:\SVSHARE\CompareFiles\AllFiles"
    sub_dir_files = [x[0] for x in os.walk(dir_to_get_files)]
    for name in ids_list:
        flag = False
        for i in range(len(sub_dir_files)):
            if name in sub_dir_files[i]:
                flag = True
        if not flag:
            to_download_list.append(name)

    return to_download_list


def file_birthtime(file):
    return time.ctime(os.path.getctime(file))


def check_ini_file_status(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    curr_conf_status = config[config.sections()[0]]['status']
    return curr_conf_status


def get_branch(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    branch = config[config.sections()[0]]['branch']
    return branch


def get_email(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    email = config[config.sections()[0]]['email']
    return email


def get_weeks_ago(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    weeks_ago = config[config.sections()[0]]['weeks_ago']
    return weeks_ago


def get_flow_type(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    flow_type = config[config.sections()[0]]['flow_type']
    return flow_type


def get_query(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    query = config[config.sections()[0]]['query']
    return query


def get_dir(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    dire = config[config.sections()[0]]['output_directory']
    return dire


def get_q_type(file):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    q_type = config[config.sections()[0]]['q_type']
    return q_type


def change_status(file, new_status):
    config = configparser.ConfigParser()
    config.read(file)
    config.sections()
    config.set(config.sections()[0], 'status', new_status)
    with open(file, 'w') as configfile:
        config.write(configfile)
