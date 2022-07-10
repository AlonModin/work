import argparse
import pandas as pd


def RTL_to_dictionary(path: str):
    output_dict = {}
    spreadsheet_file = pd.ExcelFile(path)
    worksheets = spreadsheet_file.sheet_names
    for name in worksheets:
        if not (name == 'Final Tables look and feel'):
            temp = []
            read_file = pd.read_excel(path, sheet_name=name,usecols="D")
            read_file = read_file.dropna(axis=0)
            RTL = read_file.values.tolist()
            for i in range(1,len(RTL)):
                splitted = RTL[i][0].split("[")
                temp_split = splitted[1].split(":")
                left_num = temp_split[0]
                right_num = temp_split[1].split("]")
                if left_num < right_num[0]:
                    i = int(right_num[0])
                    j = int(left_num)
                else:
                    i = int(left_num)
                    j = int(right_num[0])
                for x in range(j , i+1):
                    temp.append(splitted[0] + "[" + str(x) + "]")
            output_dict[name] = temp
    return output_dict


def dictionary_to_txt(dict):
    # path to rc file creation
    output = open(r"C:\SVSHARE\excel_file\RTL_path.rc", "w")
    output.write("Magic 271485\nRevision Verdi_Q-2020.03-SP2\n")
    for key in dict.keys():
        output.write('addGroup "'+key+'"' + "\n")
        for i in range(len(dict[key])):
            output.write("addSignal -h 15 /" + dict[key][i].replace(".","/") + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('-path', type=str, help='path to excel file')
    args = parser.parse_args()
    data_dict = RTL_to_dictionary(args.path)
    dictionary_to_txt(data_dict)
    # data_dict = RTL_to_dictionary(r"C:\SVSHARE\excel_file\LNLM Santa interface table.xlsx")
    # dictionary_to_txt(data_dict)
