import numpy as np
import pandas as pd
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB 
from sklearn.feature_extraction.text import TfidfVectorizer


#Open log file
file = open('Demo-Queries3.log', 'r')
read = file.readlines()

current_time = time.ctime()

#Open results file
Results_File = open('Scan-Results.txt', 'w')
Results_File.write('Machine Learning Scan Results: \n'
                    "Scan Start Time: " + current_time + "\n\n")

modified_log = []
#SQL_Injection_Indicators = ["-- or #", "\' OR '1", "\' OR 1 -- -", "\" OR \"\" = \"", "\" OR 1 = 1 -- -", '\'=\'', "\'LIKE\'", "\'=0--+", "OR 1=1", "\' OR \'x\'=\'x", 
#                          "\' AND id IS NULL; --", "%00", "/*..*/", "+", "||", "%", "@variable", "@@variable", "AND 1", "AND 0", "AND true", "AND false", 
#                          "1-false", "1-true", "1*56", "-2", "1\' ORDER BY 1--+", "1\' ORDER BY 2--+", "1\' ORDER BY 3--+", "1\' ORDER BY 1,2--+", "1\' ORDER BY 1,2,3--+",
#                          "1\' GROUP BY 1,2--+", "1\' GROUP BY 1,2,3--+", "\' GROUP BY names having 1=1 --", "-1 UNION SELECT 1,2,3--+", "\' UNION SELECT sum(names) from users --",
#                          "-1 UNION SELECT 1 INTO @,@", "-1 UNION SELECT 1 INTO @,@,@", "1 AND (SELECT * FROM users) = 1", "\' and MID(VERSION(),1,1) = \'5\';"]

# SQL_Injection_Indicators = ["OR 1=1", "OR 1=0", "OR x=x", "OR x=y", "OR 1=1#", "OR 1=0#", "OR x=x#", "OR x=y#", "OR 1=1-- " , "OR 1=0-- ", "OR x=x-- ", "OR x=y-- ", 
# "OR 3409=3409 AND ('pytW' LIKE 'pytW", "OR 3409=3409 AND ('pytW' LIKE 'pytY", "HAVING 1=1", "HAVING 1=0",
# "HAVING 1=1#", "HAVING 1=0#", "HAVING 1=1-- ", "HAVING 1=0-- ", "AND 1=1", "AND 1=0", "AND 1=1-- ", "AND 1=0-- ", "AND 1=1#", "AND 1=0#", "AND 1=1 AND '%'='", "AND 1=0 AND '%'='", 
# "AND 1083=1083 AND (1427=1427", "AND 7506=9091 AND (5913=5913","AND 1083=1083 AND ('1427=1427", "AND 7506=9091 AND ('5913=5913", "AND 7300=7300 AND 'pKlZ'='pKlZ", 
# "AND 7300=7300 AND 'pKlZ'='pKlY", "AND 7300=7300 AND ('pKlZ'='pKlZ", "AND 7300=7300 AND ('pKlZ'='pKlY", "AS INJECTX WHERE 1=1 AND 1=1", "AS INJECTX WHERE 1=1 AND 1=0", 
# "AS INJECTX WHERE 1=1 AND 1=1#", "AS INJECTX WHERE 1=1 AND 1=0#", "AS INJECTX WHERE 1=1 AND 1=1--", "AS INJECTX WHERE 1=1 AND 1=0--", "WHERE 1=1 AND 1=1", "WHERE 1=1 AND 1=0", 
# "WHERE 1=1 AND 1=1#", " WHERE 1=1 AND 1=0#", "WHERE 1=1 AND 1=1--", "WHERE 1=1 AND 1=0--", "ORDER BY 1-- ", "ORDER BY 2-- ", "ORDER BY 3-- " "ORDER BY 4-- ", "ORDER BY 5-- ", 
# "ORDER BY 31337-- ", "ORDER BY 1# ", "ORDER BY 2# ", "ORDER BY 3# ", "ORDER BY 4# ", "ORDER BY 5# ", "ORDER BY 31337#", "ORDER BY 1 ", "ORDER BY 2 ", "ORDER BY 3 ", 
# "ORDER BY 4 ", "ORDER BY 5 ", "ORDER BY 31337 ", "RLIKE (SELECT (CASE WHEN (4346=4346) THEN 0x61646d696e ELSE 0x28 END)) AND 'Txws'='",
# "RLIKE (SELECT (CASE WHEN (4346=4347) THEN 0x61646d696e ELSE 0x28 END)) AND 'Txws'='", "IF(7423=7424) SELECT 7423 ELSE DROP FUNCTION xcjl--", 
# "IF(7423=7423) SELECT 7423 ELSE DROP FUNCTION xcjl--", "%' AND 8310=8310 AND '%'='", "%' AND 8310=8311 AND '%'='", "and (select substring(@@version,1,1))='X'", 
# "and (select substring(@@version,1,1))='M'", "and (select substring(@@version,2,1))='i'", "and (select substring(@@version,2,1))='y'", "and (select substring(@@version,3,1))='c'", 
# "and (select substring(@@version,3,1))='S'", "and (select substring(@@version,3,1))='X'"]

SQL_Injection_Indicators = ["ORDER BY SLEEP(5)","ORDER BY 1,SLEEP(5)", "ORDER BY 1,SLEEP(5),BENCHMARK(1000000,MD5('A'))", 
"ORDER BY 1,SLEEP(5),BENCHMARK(1000000,MD5('A')),4", "ORDER BY 1,SLEEP(5),BENCHMARK(1000000,MD5('A')),4,5", 
"ORDER BY SLEEP(5)#", "ORDER BY 1,SLEEP(5)#", "ORDER BY 1,SLEEP(5),3#", "ORDER BY 1,SLEEP(5),BENCHMARK(1000000,MD5('A')),4,5#", 
"ORDER BY SLEEP(5)--", "ORDER BY 1,SLEEP(5)--", "ORDER BY 1,SLEEP(5),3--", "ORDER BY 1,SLEEP(5),3,4--"
"ORDER BY 1,SLEEP(5),BENCHMARK(1000000,MD5('A')),4,5--", "UNION ALL SELECT 1", "UNION ALL SELECT 1,2", "UNION ALL SELECT 1,2,3", "UNION ALL SELECT 1#"
"UNION ALL SELECT 1,2#", "UNION ALL SELECT 1,2,3#", "UNION ALL SELECT 1--", "UNION ALL SELECT 1,2--",  "UNION ALL SELECT 1,2,3--", 
"UNION SELECT @@VERSION,SLEEP(5),3", "UNION SELECT @@VERSION,SLEEP(5),USER(),4", "UNION SELECT @@VERSION,SLEEP(5),USER(),BENCHMARK(1000000,MD5('A')),5"]


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
    for phrase in SQL_Injection_Indicators:
        if phrase in line:
            Results_File.write("Found potential SQL Injection command: " + phrase + "\n")
            ML_Checkbox[modified_log.index(line)] = "1"
            Possible_Injections.append(line)
            Detected_Commands[modified_log.index(line)] = phrase
       
#print(ML_Checkbox)

df_x = modified_log
df_y = ML_Checkbox
cv = CountVectorizer()
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.85, random_state=4)
x_traincv=cv.fit_transform(x_train)
a=x_traincv.toarray()
#print(cv.inverse_transform(a))

mnb = MultinomialNB()
#y_train=y_train.astype('int')
mnb.fit(x_traincv,y_train)
x_testcv = cv.transform(x_test)
pred=mnb.predict(x_testcv)
#print(np.array(y_test))
actual=np.array(y_test)

count = 0
for i in range (len(pred)):
    if pred[i]==actual[i]:
        count = count+1
# print("Correct Predictions: " + str(count))
# print("Total Predictions: " + str(len(pred)))
# print("Accuracy of Prediction: " + str(count / len(pred)))
current_time = time.ctime()

Results_File.write("\nCorrect Predictions: " + str(count) + "\n")
Results_File.write("Total Predictions: " + str(len(pred)) + "\n")
Results_File.write("Accuracy of Prediction: " + str(count / len(pred) * 100) + "%" + "\n")
Results_File.write("Scan Ended At: " + current_time)
Results_File.close()