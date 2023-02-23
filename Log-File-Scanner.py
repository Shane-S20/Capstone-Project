import re

#Open log file
file = open('db-logfile.log', 'r')
read = file.readlines()

#Open ML data file to be fed to ML algorithm
file2 = open('ML-data.txt', 'r+')

modified_log = []
SQL_Injection_Commands = ["-- or #", "\' OR '1", "\' OR 1 -- -", "\" OR \"\" = \"", "\" OR 1 = 1 -- -", '\'=\'', "\'LIKE\'", "\'=0--+", "OR 1=1", "\' OR \'x\'=\'x", 
                          "\' AND id IS NULL; --", "%00", "/*..*/", "+", "||", "%", "@variable", "@@variable", "AND 1", "AND 0", "AND true", "AND false", 
                          "1-false", "1-true", "1*56", "-2", "1\' ORDER BY 1--+", "1\' ORDER BY 2--+", "1\' ORDER BY 3--+", "1\' ORDER BY 1,2--+", "1\' ORDER BY 1,2,3--+",
                          "1\' GROUP BY 1,2--+", "1\' GROUP BY 1,2,3--+", "\' GROUP BY names having 1=1 --", "-1 UNION SELECT 1,2,3--+", "\' UNION SELECT sum(names) from users --",
                          "-1 UNION SELECT 1 INTO @,@", "-1 UNION SELECT 1 INTO @,@,@", "1 AND (SELECT * FROM users) = 1", "\' and MID(VERSION(),1,1) = \'5\';"]
ML_Checkbox = []

#remove \n from log file
for line in read:
    modified_log.append(line.strip())

#SQL Commands are parsed from the log file 
modified_log = modified_log[14:len(modified_log)]

#Initialize ML array
for indexes in modified_log:
    ML_Checkbox.append("0")

#Initialize array of potential injections
Possible_Injections = []

#Initialize list of SQL commands detected to be used with the ML algorithm
Detected_Commands = []
for indexes in modified_log:
    Detected_Commands.append("0")

#Parse SQL logs to find queries that match SQL Injection queries
for line in modified_log:
    for phrase in SQL_Injection_Commands:
        if phrase in line:
            print("Found potential SQL Injection command: " + phrase)
            ML_Checkbox[modified_log.index(line)] = "1"
            Possible_Injections.append(line)
            Detected_Commands[modified_log.index(line)] = phrase

#Write ML data to file
file2.writelines(ML_Checkbox)
file2.writelines("\n")
file2.writelines(Detected_Commands)

print(Possible_Injections)
#print(Detected_Commands)

# line = file2.readline()
# print(line)
#print(modified)

# result = any(item in modified for item in SQL_Injection_Commands)
# # print(str(result))
