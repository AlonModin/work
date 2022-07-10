import io
import os
from io import StringIO
import zipfile
from zipfile import ZipFile
import pandas as pd
from os import listdir
from os.path import isfile, join
import json
from collections import Counter
import numpy as np
from prettytable import PrettyTable
from main import *
from runFuncModule import *


def compare_zip_files(first_created_file):
    display_pie_chart = False  ##--boolean to know if we want to display pie chart or not--##
    comparing_files = True  ##--boolean to know if we want to compare directories or not--##

    sub_dic_files = []
    files_we_have = get_list_we_have()
    files_to_download = get_list_to_download()
    if files_we_have:
        sub_dic_files.extend(files_we_have)
    if files_to_download:
        sub_dic_files.extend(x for x in files_to_download if x not in files_we_have)

    dir_name = get_dir(first_created_file)
    first_dic_path = []  ##--dir 1 to compare--##
    second_dic_path = dir_name  ##--dir 2 to compare--##

    all_files_dir = "C:\\SVSHARE\\CompareFiles\\AllFiles"
    inside_files = [x[0] for x in os.walk(all_files_dir)]
    for name in sub_dic_files:
        for i in range(len(inside_files)):
            if name in inside_files[i]:
                first_dic_path.append(inside_files[i])
                break

    if_created = False
    finall = {}
    all_flows = []
    good_files = 0
    list_bad_files = []
    second_flows = []
    bad_files = 0
    for name in sub_dic_files:
        # print(sub_dic_files)
        # print(name)
        temp_file_path = ""
        for i in range(len(first_dic_path)):
            if name in first_dic_path[i]:
                temp_file_path = first_dic_path[i]
                break
        if comparing_files:
            flow_only1 = ''
            flow_list1 = []
            arch_flows1 = []
            paths1 = []
            flows1 = []
            discovered1 = []
        temp = []
        flow_only = ''
        flow_list = []
        arch_flows = []
        paths = []
        flows = []
        discovered = []
        # open and read the log
        with zipfile.ZipFile(temp_file_path + "\\" + "intel-status-scope-logs-v1.zip") as zf:
            with io.TextIOWrapper(zf.open("post_processors/mdat_postprocessor/mdat_postprocessor.log"),
                                  encoding="utf-8") as f:
                log_file = f.readlines()
        if comparing_files:
            with zipfile.ZipFile(second_dic_path + "\\" + name + "\\" + "intel-status-scope-logs-v1.zip") as zf1:
                with io.TextIOWrapper(zf1.open("post_processors/mdat_postprocessor/mdat_postprocessor.log"),
                                      encoding="utf-8") as f1:
                    log_file1 = f1.readlines()
                # -----------------------------------------------------------------------
                # read only flows summary
                # file in first dir :
                for x in log_file:
                    if (not ("Table" in x)):
                        flow_only = flow_only + x
                    else:
                        break
                # file in second dir :
                if comparing_files:
                    for x in log_file1:
                        if (not ("Table" in x)):
                            flow_only1 = flow_only1 + x
                        else:
                            break
        # -----------------------------------------------------------------------
        # split each line we need
        # file in first dir :
        flow_list = flow_only.split("|")
        for i in range(len(flow_list)):
            if "Flow Name:" in flow_list[i]:
                while flow_list[i] != "\n":
                    j = 1
                    flows.append(flow_list[i + j])
                    j += 1
                    i += 1
            if "Arch Flow" in flow_list[i]:
                while flow_list[i] != "\n":
                    j = 1
                    arch_flows.append(flow_list[i + j])
                    j += 1
                    i += 1
            if "Path" in flow_list[i]:
                while flow_list[i] != "\n":
                    j = 1
                    paths.append(flow_list[i + j])
                    j += 1
                    i += 1
        # file in second dir :
        if comparing_files:
            flow_list1 = flow_only1.split("|")
            for i in range(len(flow_list1)):
                if "Flow Name:" in flow_list1[i]:
                    while flow_list1[i] != "\n":
                        j = 1
                        flows1.append(flow_list1[i + j])
                        j += 1
                        i += 1
                if "Arch Flow" in flow_list1[i]:
                    while flow_list1[i] != "\n":
                        j = 1
                        arch_flows1.append(flow_list1[i + j])
                        j += 1
                        i += 1
                if "Path" in flow_list1[i]:
                    while flow_list1[i] != "\n":
                        j = 1
                        paths1.append(flow_list1[i + j])
                        j += 1
                        i += 1
        # -----------------------------------------------------------------------
        # split the col and check not discovered
        # file in first dir
        data = flow_only
        df = pd.DataFrame([x.split('|') for x in data.split('\n')])

        new_df = df[6:]
        for i in range(len(flows) - 1):
            temp_info = new_df[i + 2].values.tolist()
            if "not discovered" in temp_info:
                discovered.append("no")
            else:
                discovered.append("yes")
        # file in second dir :
        if comparing_files:
            data1 = flow_only1
            df1 = pd.DataFrame([x.split('|') for x in data1.split('\n')])

            new_df1 = df1[6:]
            for i in range(len(flows1) - 1):
                temp_info1 = new_df1[i + 2].values.tolist()
                if "not discovered" in temp_info1:
                    discovered1.append("no")
                else:
                    discovered1.append("yes")
        # -----------------------------------------------------------------------
        flows_stripped = [x.strip() for x in flows]
        arch_flows_stripped = [x.strip() for x in arch_flows]
        paths_stripped = [x.strip() for x in paths]
        # -----------------------------------------------------------------------
        # check if col data is in both files but maybe different col number
        if comparing_files:
            count = 1
            count_new = 1
            file_name = "changes_"+get_branch(first_created_file)+".log"
            if if_created:
                log_f = open("C:\\SVSHARE\\amodin\\"+file_name, "a") #where the comparing file will be
            else:
                log_f = open("C:\\SVSHARE\\amodin\\"+file_name, "w")  ##--log file created--##
                if_created = True
            if len(flows) == len(flows1) == 2:
                curr_flow = new_df[2].values.tolist()
                curr_flow1 = new_df1[2].values.tolist()
                if curr_flow != curr_flow1:
                    bad_files += 1
                    list_bad_files.append(name)
                    print("flow " + arch_flows_stripped[0] + " have a mismatch problem")
                    log_f.write("In file name: " + name + " there is a change at the flow!\n")
                    x = PrettyTable()
                    x.padding_width = 1
                    curr_flow_without_none = []
                    for val in curr_flow:
                        if val != None:
                            curr_flow_without_none.append(val)
                    x.add_column("Old Flow", curr_flow_without_none)
                    curr_flow1_without_none = []
                    for val in curr_flow1:
                        if val != None:
                            curr_flow1_without_none.append(val)
                    x.add_column("New Flow", curr_flow1_without_none)
                    log_f.write(str(x))
                    log_f.write("\n\n\n")
                    log_f.write("---+---" * 50)
                    log_f.write("\n\n\n")
                else:
                    good_files = good_files + 1
            if len(flows) != len(flows1):
                bad_files += 1
                list_bad_files.append(name)
                print("file " + name + " has more or less flows")
                log_f.write("In file name: " + name + " there is a change at the flows count!\n")
                log_f.write("we had " + str(len(flows) - 1) + " flows and at the new file we have " + str(
                    len(flows1) - 1) + " flows! \n")
                if len(flows) > len(flows1):  # flows is now less than before and we need to print what is lost
                    flag_to_write = True
                    x = PrettyTable()
                    x.padding_width = 1
                    for i in range(len(flows1) - 1):
                        temp_second_file = new_df1[i + 2].values.tolist()
                        second_file_without_none = []
                        for val in temp_second_file:
                            if val != None:
                                second_file_without_none.append(val)
                        second_flows.append(new_df1[i + 2].values.tolist())
                        x.add_column("New Flow " + str(count), second_file_without_none)
                        count += 1
                    for j in range(len(flows) - 1):
                        temp_first_file = new_df[j + 2].values.tolist()
                        first_file_without_none =[]
                        for val in temp_first_file:
                            if val != None:
                                first_file_without_none.append(val)
                        if not (first_file_without_none in second_flows):
                            flag_to_write = True
                            list_bad_files.append(name)
                            log_f.write("flow " + first_file_without_none[0].strip() + " is removed/updated from the second file! \n")
                            column_lists = []
                            x.add_column("Old Flow " + str(count_new), first_file_without_none)
                            count_new += 1
                    if (flag_to_write):
                        log_f.write(str(x))
                        log_f.write("\n\n\n")
                        log_f.write("---+---" * 50)
                        log_f.write("\n\n\n")
                if len(flows) < len(flows1):  # flows is now more than before and we need to print whats added
                    first_flows = []
                    flag_to_write = False
                    x = PrettyTable()
                    x.padding_width = 1
                    for i in range(len(flows) - 1):
                        temp_first_file = new_df[i + 2].values.tolist()
                        first_flows.append(new_df[i + 2].values.tolist())
                        x.add_column("Old Flow " + str(count), temp_first_file)
                        count += 1
                    for j in range(len(flows1) - 1):
                        temp_second_file = new_df1[j + 2].values.tolist()
                        if not (temp_second_file in first_flows):
                            flag_to_write = True
                            list_bad_files.append(name)
                            log_f.write("flow " + temp_second_file[0].strip() + " is added/updated to the second file! \n")
                            x.add_column("New Flow " + str(count_new), temp_second_file)
                            count_new += 1
                    if (flag_to_write):
                        log_f.write(str(x))
                        log_f.write("\n\n\n")
                        log_f.write("---+---" * 50)
                        log_f.write("\n\n\n")
            if len(flows) == len(flows1) and len(flows) > 2:
                x = PrettyTable()
                x.padding_width = 1
                file_is_good = True
                for i in range(len(flows1) - 1):
                    temp_second_file = new_df1[i + 2].values.tolist()
                    second_flows.append(new_df1[i + 2].values.tolist())
                    x.add_column("New Flow " + str(count), temp_second_file)
                    count += 1
                for j in range(len(flows) - 1):
                    temp_first_file = new_df[j + 2].values.tolist()
                    if not (temp_first_file in second_flows):
                        file_is_good = False
                        bad_files += 1
                        list_bad_files.append(name)
                        print("flow " + temp_first_file[0].strip() + " from zip: " + name + " from first dir is not in second dir")
                        log_f.write("In file name: " + name + " there is a change at the flow!\n")
                        x.add_column("Old Flow " + str(count_new), temp_first_file)
                        count_new += 1
                if (file_is_good):
                    good_files = good_files + 1
                else:
                    log_f.write(str(x))
                    log_f.write("\n\n\n")
                    log_f.write("---+---" * 50)
                    log_f.write("\n\n\n")
        # -----------------------------------------------------------------------
        for i in range(len(flows) - 1):
            temp.append(arch_flows_stripped[i] + " discovered = " + discovered[i] + " : flow_path = " + paths_stripped[i])
            all_flows.append(arch_flows_stripped[i] + " discovered = " + discovered[i] + " : flow_path = " + paths_stripped[i])
        finall[name] = temp
        # -----------------------------------------------------------------------
    f.close()
    zf.close()
    body = f"There are Total {len(sub_dic_files)} files and {bad_files} of them have changed\n you can check more about the changes here: C:\\SVSHARE\\amodin" \
           f"\n Make sure you enter as host to see the file!"
    if (comparing_files):
        f1.close()
        zf1.close()
        log_f.close()
    perc_list = []
    my_dict = {i: all_flows.count(i) for i in all_flows}
    for item in all_flows:
        item_cnt = all_flows.count(item)
        perc = (item_cnt / len(all_flows) * 100)
        perc = round(perc, 2)
        perc_list.append(f"{item} ; {perc}")
    perc_list = list(dict.fromkeys(perc_list))
    to_display = []
    j = 0
    for i in my_dict.keys():
        to_display.append(perc_list[j] + " ; " + str(my_dict.get(i)))
        j += 1
    # -----------------------------------------------------------------------
    # display pie chart
    if (display_pie_chart):
        pie_list = []
        pie_items = []
        pie_perc = []
        for i in range(len(to_display)):
            pie_list.append(to_display[i].split(";"))
        for j in range(len(pie_list)):
            pie_items.append(pie_list[j][0])
            pie_perc.append(pie_list[j][1])

    ##    fig = px.pie(values=pie_perc, names=pie_items)
    ##    fig.update_traces(textposition='inside', textinfo='percent+label')
    ##    plotly.offline.plot(fig, filename='piechart.html')
    return body
# -----------------------------------------------------------------------
# export report to json file
# new_file = open("C:\\SVSHARE\\amodin\\status_scope_allFiles.json" , "w")
# json.dump(to_display, new_file)
# new_file.close()
# ---------------------------END-----------------------------------------