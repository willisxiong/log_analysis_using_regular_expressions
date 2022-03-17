#!/usr/bin/env python3

import re
import sys
import csv
import subprocess
import pandas as pd

filename = sys.argv[1]

#find all the error message
def get_error_msg(filename):
    pattern = r"ERROR([a-zA-Z' ]+)"
    error_msg = []
    with open(filename) as f:
        for line in f:
            if "ERROR" in line:
                error_line = re.search(pattern, line)
                new_error_line = error_line[1].strip()
                error_msg.append(new_error_line)
            continue
    return error_msg        
all_error_msg = get_error_msg(filename)

#count for each error
def count_msg(lmsg):
    msg_list = []
    msg_dict = {}
    for msg in lmsg:
        if not msg in msg_list:
            msg_list.append(msg)
            msg_dict[msg] = 1
        else:
            msg_dict[msg] += 1
    return msg_dict
error_msg_result = count_msg(all_error_msg)

#convert the error dict to a lisf of dict format
#in order to create data for write into csv
def convt_data(orig_data):
    msg_data = {}
    csv_data = []
    for k, v in orig_data.items():
        msg_data["ERROR"] = k
        msg_data["COUNT"] = v
        csv_data.append(msg_data.copy())
    return csv_data 
error_report_data = convt_data(error_msg_result)
sorted_report = sorted(error_report_data, key=lambda error_report: error_report["COUNT"], reverse=True)

keys = ["ERROR", "COUNT"]

with open('error_report.csv', 'w') as report:
    writer = csv.DictWriter(report, fieldnames = keys)
    writer.writeheader()
    writer.writerows(sorted_report)

subprocess.run(['cat', 'error_report.csv'])

df = pd.read_csv("error_report.csv")
html = df.to_html("error_report.html")