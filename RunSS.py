import smtplib
import os
import subprocess
import time

from pysvtools import status_scope
import pysvext.lunarlake_status_scope.post_processors.mdat.mdat_uy_post_process as mdat
from pysvext.lunarlake_status_scope.analyzers.xncu.ver1.xncu_plugin import XNcuPlugin
from pysvext.lunarlake_status_scope.analyzers.noc.ver1.noc_plugin import NocPlugin
from pysvext.lunarlake_status_scope.analyzers.hbo.ver1.hbo_plugin import HboPlugin
from pysvext.lunarlake_status_scope.analyzers.idib.ver1.idib_plugin import IdibPlugin
from pysvext.lunarlake_status_scope.analyzers.ccf.ver1.ccf_plugin import CcfPlugin
from pysvext.lunarlake_status_scope.analyzers.mempma.ver1.mempma_plugin import MempmaPlugin
from pysvext.lunarlake_status_scope.analyzers.ccfpma.ver1.ccfpma_plugin import CcfpmaPlugin


def mdt_env(path: str, output: str):
    plugin_idib = IdibPlugin()
    plugin_xncu = XNcuPlugin()
    plugin_noc = NocPlugin()
    plugin_hbo = HboPlugin()
    plugin_ccf = CcfPlugin()
    plugin_mempma = MempmaPlugin()
    plugin_ccfpma = CcfpmaPlugin()

    state_dump_file_path = path
    namednodes_file_path = r"C:\pythonsv\src\pysvext-lunarlake_status_scope\tests\test_input\MDAT\A0\snapshot.spkx"
    status_scope.run(
        analyzers=[plugin_ccf, plugin_hbo, plugin_noc, plugin_xncu, plugin_mempma, plugin_ccfpma, plugin_idib, mdat.MdatPostProcessor()],
        offline_dict={"state_dump": state_dump_file_path, "namednodes": namednodes_file_path},
        autoconfig=False,
        output_dir=output,
    )
    pass


def send_email(body: str, email: str):
    sender = 'alon.modin@intel.com'
    receivers = [email]
    SUBJECT = "Your status_scope run finished !"
    TEXT = body
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


    try:
        smtpObj = smtplib.SMTP('smtp.intel.com')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
    return


if __name__ == '__main__':
    #while true and sleep 30 min +-
    while True:
        main_folder = r"C:\SVSHARE\RunSS"
        all_folders = [name for name in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, name))] #all folders inside the main folder
        nf_folders = [] #not finished folders
        for file in all_folders:      #yuval_files
            if "finished" not in file and "output" not in file:
                nf_folders.append(file)
        while nf_folders:
            path = r"C:\pythonsv\src\pysvext-lunarlake_status_scope"
            command = 'git checkout main'
            command = command.split()
            branch = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path).stdout.read()
            command = 'git pull'
            command = command.split()
            branch = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path).stdout.read()
            for file_in in nf_folders:        # files_afeldma
                get_id = file_in.split("_")
                email = get_id[-1] + "@sc.intel.com"
                temp_path = main_folder + "\\" + file_in
                output_path = r"C:\SVSHARE\RunSS" + "\\" +file_in + "_output"
                files_to_run = [name for name in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, name))]
                for file in files_to_run:         #ww14
                    path_to_run = temp_path + "\\" + file + "\\" + "state_dump.zip"
                    spec_output = output_path + "\\" + file
                    mdt_env(path_to_run, spec_output)
                os.rename(temp_path, temp_path+"_finished")
                body = f"Hi,\n\nYour run finished !\n You can find your files here: C:\\SVSHARE\\RunSS\\{file_in}_output \nPlease note that in 1 week all files will be deleted ! \n\nThanks,\nAlon Modin."
                send_email(body, "alon.modin@intel.com")
                nf_folders.remove(file_in)
        time.sleep(15 * 60)
        print("woke up and check for new files")