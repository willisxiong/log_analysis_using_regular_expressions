#!/usr/bin/env python3

import re
import sys
import csv
import subprocess
import pandas as pd

filename = sys.argv[1]

#get all the username and store in a list
def get_user_msg(filename):
    pattern = r"\(([a-z.]+)\)"
    user_list = []
    with open(filename) as file:     
        for line in file:
            usr_line = re.search(pattern, line)
            if not usr_line[1] in user_list:
                user_list.append(usr_line[1])
    return user_list
user_list = get_user_msg(filename)

#count INFO and ERROR for each user
#put all the count data into list dict format
def count_msg(userlist):
    user_dict = []
    each_user = {}
    for user in userlist:
        each_user["USERNAME"] = user
        each_user["INFO"] = 0
        each_user["ERROR"] = 0
        with open(filename) as file:
            for line in file:
                if user in line and "INFO" in line:
                    each_user["INFO"] += 1
                elif user in line and "ERROR" in line:
                    each_user["ERROR"] += 1
                continue
            user_dict.append(each_user.copy())
    return user_dict
csv_data = count_msg(user_list)

keys = ["USERNAME", "INFO", "ERROR"]

with open("user_report.csv", "w") as user:
    writer = csv.DictWriter(user, fieldnames=keys)
    writer.writeheader()
    writer.writerows(csv_data)

subprocess.run(['cat', 'user_report.csv'])

df = pd.read_csv("user_report.csv")
html = df.to_html("user_report.html")