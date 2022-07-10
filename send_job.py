from __future__ import print_function
from pysvtools import status_scope
from pysvext.lunarlake_status_scope.base_classes.lnl_ip_plugin_base_test import LnlIpPluginBaseTest
import pysvext.lunarlake_status_scope.post_processors.mdat.mdat_uy_post_process as mdat
from pysvext.lunarlake_status_scope.analyzers.ccf.ver1.ccf_plugin import CcfPlugin
from pysvext.lunarlake_status_scope.analyzers.pm.ver1.pm_plugin import PmPlugin
import glob
import smtplib
from datetime import datetime
from configparser import ConfigParser
import subprocess
import argparse
from os.path import isfile, join
from os import listdir
import os
from pysvtools import status_scope


def generate_q_config(branch_name, query, email, q_type):
    path = r"\\HA01WVAW9132\c$\SVSHARE\CompareFiles\ConfigFiles\config"+branch_name+".ini" #dir to save the config file
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
    config = ConfigParser()
    config.add_section(branch_name)
    config.set(branch_name, 'Branch', branch_name)
    config.set(branch_name, 'Email', email)
    config.set(branch_name, 'Query', query)
    config.set(branch_name, 'Output_Directory', r"C:\SVSHARE\QueryCompFiles\qFilesAfterRun\files_for_" + dt_string) #dir to save the downloaded files
    config.set(branch_name, 'Status', 'Waiting')
    config.set(branch_name, 'q_type', q_type)


    with open(path, 'w') as configfile:
        config.write(configfile)


def generate_config(branch_name, weeks_ago, flow_type, email, q_type):
    path = r"\\HA01WVAW9132\c$\SVSHARE\CompareFiles\ConfigFiles\config" + branch_name + ".ini"  # dir to save the config file
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
    config = ConfigParser()
    config.add_section(branch_name)
    config.set(branch_name, 'Branch', branch_name)
    config.set(branch_name, 'Weeks_ago', str(weeks_ago))
    config.set(branch_name, 'Flow_type', flow_type)
    config.set(branch_name, 'Email', email)
    config.set(branch_name, 'Output_Directory',
               r"C:\SVSHARE\CompareFiles\FilesAfterRun\files_for_" + dt_string)  # dir to save the downloaded files
    config.set(branch_name, 'Status', 'Waiting')
    config.set(branch_name, 'q_type', q_type)


    with open(path, 'w') as configfile:
        config.write(configfile)


def get_git_branch(path=None):
    if path is None:
        path = os.path.curdir
    command = 'git rev-parse --abbrev-ref HEAD'.split()
    branch = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path).stdout.read()
    return branch.strip().decode('utf-8')


def run_by_path_ADL(path: str):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
    output = "C:\\SVSHARE\\adlPathCompFiles\\" + dt_string
    all_files = [x[0] for x in os.walk(path)]
    for i in range(len(all_files)):
        x = ''.join(glob.glob(all_files[i] + '\\*.zip'))
        status_scope.run(offline_path=x,
                         analyzers=["ccf", "idp", "ncu", "iop", "cmi", "mc", "pm"],
                         post_processors=["mdat_postprocessor"], output_dir=output + '\\' + all_files[i])

    body = f"your run finished! you can check more about the changes here: C:\\SVSHARE\\adlPathCompFiles\\{dt_string}\n " \
           f"Make sure you enter as host to see the files! "
    return body


def run_by_path_LNL(path: str):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
    output = "C:\\Temp\\WeeklyRun\\AfterRun\\" + dt_string
    plugin = CcfPlugin()
    all_files = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    for dir in all_files:
        x = ''.join(glob.glob(path + "\\" + dir + '\\state_dump.zip'))
        status_scope.run(analyzers=[plugin, mdat.MdatPostProcessor()],
            offline_dict={"state_dump": x,
            "namednodes": r"C:\pythonsv\src\pysvext-lunarlake_status_scope\tests\test_input\MDAT\A0\snapshot.spkx"},
            autoconfig=False, output_dir=output+ "\\" + dir, )
    body = f"your run finished! you can check more about the changes here: \\HA01WVAW9132\\c$\\SVSHARE\\lnlPathCompFiles\\{dt_string}\n " \
           f"Make sure you enter as host to see the files! "
    return body


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


def send_branch(branch_name, path=None):
    if path is None:
        path = os.path.curdir
    command = 'git remote add ' + branch_name + ' //HA01WVAW9132/c$/pythonsv/src/status_scope_ext'
    command = command.split()
    branch = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path).stdout.read()
    command = 'git push ' + branch_name + ' ' + branch_name
    command = command.split()
    branch = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path).stdout.read()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional description')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-pathADL', type=str, help='path to folder that you want to run all ADL files inside')
    group.add_argument('-query', type=str, help='path to query you would like to use')
    group.add_argument('-duration', type=int, help='the number of weeks ago you would like to choose for your job')
    group.add_argument('-pathLNL', type=str, help='path to folder that you want to run all LNL files inside')

    parser.add_argument('-email', type=str, required=True,
                        help='the email you would like to get details to, at the end of the job run')
    parser.add_argument('-flow', type=str, help='flow type for query: discovered / not discovered')
    parser.add_argument('-branch', type=str, default="current",
                        help='branch to run your job, default is current branch')
    args = parser.parse_args()

    if args.pathADL is not None:
        mail_msg = run_by_path_ADL(args.pathADL)
        send_email(mail_msg, args.email)
        exit(1)

    if args.pathLNL is not None:
        mail_msg = run_by_path_LNL(args.pathLNL)
        send_email(mail_msg, args.email)
        exit(1)

    if args.branch == "current":
        branch_name = get_git_branch()
    else:
        branch_name = args.branch

    q_type = ""
    if args.query is not None:
        q_type = "modified"
        generate_q_config(branch_name, args.query, args.email, q_type)
        #send_branch(branch_name) // DO WE NEED THIS ?!

    if args.duration is not None and args.flow is not None:
        q_type = "regular"
        generate_config(branch_name, args.duration, args.flow, args.email, q_type)
        #send_branch(branch_name) // DO WE NEED THIS ?!

### templates :
###     send_job.py -path c:/... -email moshe@intel.com  # run the files in the path
###     send_job.py -query c:/... -email moshe@intel.com  # send config file with path to modified query
###     send_job.py -duration 1 -flow discovered -email moshe@intel.com  # send config file with details to generate query
