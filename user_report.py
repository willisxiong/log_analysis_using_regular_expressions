#!/usr/bin/env python3

import re
import os
import csv
import subprocess
import pandas as pd

class UserReport:
    def __init__(self, filename):
        self.filename = filename

    def get_user_msg(self):
        """find all the username in syslog.log and store them in a list"""
        pattern = r"\(([a-z.]+)\)"
        user_list = []
        with open(self.filename) as file:     
            for line in file:
                usr_line = re.search(pattern, line)
                if not usr_line[1] in user_list:
                    user_list.append(usr_line[1])
        return user_list

    def count_msg(self):
        """
        count INFO and ERROR for each user in syslog.log,
        put all the count data into a list dict format
        """
        user_dict = []
        each_user = {}
        userlist = self.get_user_msg()
        for user in userlist:
            each_user["USERNAME"] = user
            each_user["INFO"] = 0
            each_user["ERROR"] = 0
            with open(self.filename) as file:
                for line in file:
                    if user in line and "INFO" in line:
                        each_user["INFO"] += 1
                    elif user in line and "ERROR" in line:
                        each_user["ERROR"] += 1
                    continue
                user_dict.append(each_user.copy())
        return user_dict
    
    def create_report(self):
        """create the csv file and print it out"""
        keys = ["USERNAME", "INFO", "ERROR"]
        csv_data = self.count_msg()

        with open("user_report.csv", "w") as user:
            writer = csv.DictWriter(user, fieldnames=keys)
            writer.writeheader()
            writer.writerows(csv_data)

        subprocess.run(['cat', 'user_report.csv'])

    def create_html(self):
        if os.path.exists("user_report.csv"):
            df = pd.read_csv("user_report.csv")
            df.to_html("user_report.html")
        else:
            print("Please generate the csv file first")

def main():
    report = UserReport("syslog.log")
    report.create_report()
    report.create_html()

if __name__ == "__main__":
    main()