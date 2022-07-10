import zipfile
import io
import os
import difflib


logs = ["ccf", "idp", "ncu", "iop", "cmi", "mc", "pm"]
dir1 = "C:\\Temp\\WeeklyRun\\MainFolder"
dir2 = "C:\\Temp\\WeeklyRun\\AfterRun\\24.04.2022_11.02.58"
all_files = [name for name in os.listdir(dir1) if os.path.isdir(os.path.join(dir1, name))]
output = open("C:\\Temp\\WeeklyRun\\log_changes.log", "w")
for name in all_files:
    output.write(f'\n+----------------+ {name} +----------------+\n')
    for log in logs:
        log_s = True
        zf = zipfile.ZipFile(dir1 + "\\" + name + "\\" + "intel-status-scope-logs-v1.zip")
        f = io.TextIOWrapper(zf.open(f"ip_plugins/{log}/{log}.log"), encoding="utf-8")

        zf1 = zipfile.ZipFile(dir2 + "\\" + name + "\\" + "intel-status-scope-logs-v1.zip")
        f1 = io.TextIOWrapper(zf1.open(f"ip_plugins/{log}/{log}.log"), encoding="utf-8")
    ##############################################################
    # first_file_lines = f.readlines()
    # second_file_lines = f1.readlines()
    # difference = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines, f, f1)
    # difference_report = open("C:\\Temp\\WeeklyRun\\log_changes.html", "w")
    # difference_report.write(difference)
    # difference_report.close()
    ##############################################################
    old_lines = f.read().split('\n')
    new_lines = f1.read().split('\n')

    old_lines_set = set(old_lines)
    new_lines_set = set(new_lines)

    old_added = old_lines_set - new_lines_set
    old_removed = new_lines_set - old_lines_set

    for line in old_lines:
        if line in old_added:
            if log_s:
                output.write(f'\n+----------------+ {log} +----------------+\n')
                log_s = False
            output.write('- '+line.strip()+'\n')
        elif line in old_removed:
            if log_s:
                output.write(f'\n+----------------+ {log} +----------------+\n')
                log_s = False
            output.write('+ '+line.strip()+'\n')

    for line in new_lines:
        if line in old_added:
            if log_s:
                output.write(f'\n+----------------+ {log} +----------------+\n')
                log_s = False
            output.write('- '+line.strip()+'\n')
        elif line in old_removed:
            if log_s:
                output.write(f'\n+----------------+ {log} +----------------+\n')
                log_s = False
            output.write('+ '+line.strip()+'\n')