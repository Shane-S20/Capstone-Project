import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB 
from sklearn.feature_extraction.text import TfidfVectorizer

#Open log file
file = open('db-logfile.log', 'r')
read = file.readlines()

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
            #print("Found potential SQL Injection command: " + phrase)
            ML_Checkbox[modified_log.index(line)] = "1"
            Possible_Injections.append(line)
            Detected_Commands[modified_log.index(line)] = phrase

        
print(ML_Checkbox)

df_x = modified_log
df_y = ML_Checkbox
cv = CountVectorizer()
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.7, random_state=4)
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
print("Correct Predictions: " + str(count))
print("Total Predictions: " + str(len(pred)))
print("Accuracy of Prediction: " + str(count / len(pred)))