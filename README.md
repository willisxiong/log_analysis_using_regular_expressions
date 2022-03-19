# Log Analysis using Regular Expressions
## The target of the scripts:
- use regex to find all error message and count for each error;
- write the result to a csv file and order by count number in descending;
- convert the csv to html;
- count the error for each user, the username is in parenthesis in syslog.log, just like below:
```
Jan 31 17:51:52 ubuntu.local ticky: INFO Closed ticket [#8604] (mcintosh)
```
- write the result to a csv file;
- convert the csv to html.
