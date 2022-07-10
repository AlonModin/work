import subprocess
from compare_zip_files import *
from runFuncModule import *
from pysvtools import status_scope
from compare_zip_files import *
from svtools.pysv2axon import download
from datetime import datetime, timedelta
import string
import random
import smtplib


def generate_download_file(updated_query):
    global command_line
    path = r'C:\SVSHARE\CompareFiles'
    random_dir = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    with open(path + random_dir, 'w') as tmp:
        tmp.write(updated_query)
        q_name = '@' + tmp.name.replace("\\", "/")
        now = datetime.now()
        command_line = "c:/temp/axon-windows-x64.exe query --query " + q_name + " --token 6605dc21-decf-462b-8dfc-a9f6ca757196 > test1"
    return command_line


def run_by_cTime(first_created_file, command_line):
    global full_file_list
    full_file_list = []
    list_files_to_download = []
    list_files_we_have = []
    print("Started Running\n")
    os.chdir(r'C:\SVSHARE\CompareFiles')
    os.system(command_line)
    print("Getting Lists\n")
    change_status(first_created_file, "Running")
    list_files_we_have = get_list_we_have()
    list_files_to_download = get_list_to_download()
    print(list_files_we_have)
    print(list_files_to_download)
    if list_files_we_have:
        full_file_list.extend(list_files_we_have)
    if list_files_to_download:
        full_file_list.extend(x for x in list_files_to_download if x not in list_files_we_have)

    # download files we don't have
    print("Downloading missing files\n")
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
    os.mkdir('C:\\SVSHARE\\CompareFiles\\AllFiles\\'+dt_string)  # dir to download files to, timestamp name
    for item in list_files_to_download:
        os.mkdir('C:\\SVSHARE\\CompareFiles\\AllFiles\\'+dt_string+'\\'+item)
        os.chdir('C:\\SVSHARE\\CompareFiles\\AllFiles\\'+dt_string+'\\'+item)
        archive_path = download.save_status_scope_archive(item)
    change_file_name('C:\\SVSHARE\\CompareFiles\\AllFiles\\'+dt_string)  # change all file names to 'intel-status-scope-logs-v1'
    print("finished downloading\n")

    # search the files and then run them
    output_dir = get_dir(first_created_file)
    dir_to_get_files = "C:\\SVSHARE\\CompareFiles\\AllFiles"  # dir where all files are
    sub_dir_files = [x[0] for x in os.walk(dir_to_get_files)]
    print("starting to run files\n")
    for name in full_file_list:
        for i in range(len(sub_dir_files)):
            if name in sub_dir_files[i]:
                x = ''.join(glob.glob(sub_dir_files[i] + '\\*.zip'))
                status_scope.run(offline_path=x,
                                analyzers=["ccf", "idp", "ncu", "iop", "cmi", "mc", "pm"],
                                post_processors=["mdat_postprocessor"], output_dir=output_dir+'\\'+name)
                break
    print(first_created_file + " Done running")
    change_status(first_created_file, "Done")


def change_file_name(path):
    dir_name = path
    dir_files = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, name))]
    for name in dir_files:
        new_dir_name = dir_name + "\\" + name
        files = os.listdir(new_dir_name)
        file_path = new_dir_name + "\\" + files[0]
        file_dest = new_dir_name + "\\" + 'intel-status-scope-logs-v1.zip'
        os.rename(file_path, file_dest)


def set_branch(branch_name, path=None):
    if path is None:
        path = r"C:\pythonsv\src\status_scope_ext"
    command = 'git checkout '+branch_name
    command = command.split()
    branch = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path)
    return


def send_email(body: str, email_to_send):
    sender = 'alon.modin@intel.com'
    receivers = [email_to_send]
    message = """From: From HA01WVAW9132 <alon.modin@intel.com>

    """+body

    try:
        smtpObj = smtplib.SMTP('smtp.intel.com')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
    return


if __name__ == '__main__':
    global first_created_file
    while True:
        fileDir = r"C:\SVSHARE\CompareFiles\ConfigFiles"
        fileExt = r".ini"
        filenames = [os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)]
        dictionary = {}
        for file in filenames:
            file_time = file_birthtime(file)
            dictionary[file] = file_time
        first_created_file_value = min(dictionary.values())

        # list keys and values
        key_list = list(dictionary.keys())
        val_list = list(dictionary.values())

        # handle the config file
        position = val_list.index(first_created_file_value)
        for i in range(len(key_list)):
            if check_ini_file_status(key_list[position]) == 'Waiting':
                first_created_file = key_list[position]
                break
            else:
                del dictionary[first_created_file_value]
                first_created_file_value = min(dictionary.values())
                position = val_list.index(first_created_file_value)
        print(first_created_file)

        email_to_send = get_email(first_created_file)

        query = get_query(first_created_file)  # set query
        command_line = generate_download_file(query)

        branch_name = get_branch(first_created_file)  # switch branch
        set_branch(branch_name)

        run_by_cTime(first_created_file, command_line)  # start running

        change_file_name(get_dir(first_created_file))
        body = compare_zip_files(first_created_file)  # start comparing
        send_email(body, email_to_send)
