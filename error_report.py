#!/usr/bin/env python3

import re
import os
import csv
import subprocess
import pandas as pd
 
class ErrorReport:
    def __init__(self,filename):
        self.filename = filename

    def get_error_msg(self):
        """find the error message in syslog.log and return a error message list"""
        pattern = r"ERROR([a-zA-Z' ]+)"
        error_msg = []
        with open(self.filename) as f:
            for line in f:
                if "ERROR" in line:
                    error_line = re.search(pattern, line)
                    new_error_line = error_line[1].strip()
                    error_msg.append(new_error_line)
                continue
        return error_msg

    def count_msg(self):
        """count for each error and return a dict"""
        msg_list = []
        msg_dict = {}
        lmsg = self.get_error_msg()
        for msg in lmsg:
            if not msg in msg_list:
                msg_list.append(msg)
                msg_dict[msg] = 1
            else:
                msg_dict[msg] += 1
        return msg_dict    

    def convt_data(self):
        """change the msg dict to a desired format for write into csv"""
        msg_data = {}
        csv_data = []
        orig_data = self.count_msg()
        for k, v in orig_data.items():
            msg_data["ERROR"] = k
            msg_data["COUNT"] = v
            csv_data.append(msg_data.copy())
        return csv_data

    def create_report(self):
        """
        order the csv data by descending and create the csv file,
        print out the csv content
        """
        error_report_data = self.convt_data()
        sorted_data = sorted(error_report_data, key=lambda error_report: error_report["COUNT"], reverse=True)

        keys = ["ERROR", "COUNT"]

        with open('error_report.csv', 'w') as report:
            writer = csv.DictWriter(report, fieldnames = keys)
            writer.writeheader()
            writer.writerows(sorted_data)

        subprocess.run(['cat', 'error_report.csv'])

    def create_html(self):
        if os.path.exists("error_report.csv"):
            df = pd.read_csv("error_report.csv")
            df.to_html("error_report.html")
        else:
            print("Please generate the csv file first")


report = ErrorReport("syslog.log")
report.create_report()
report.create_html()