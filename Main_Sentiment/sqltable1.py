import MySQLdb
import csv
import re

db = MySQLdb.connect("localhost","root","admin","test",charset = 'utf8')

cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print("Database version : %s " % data)

cursor.execute("show tables")

data = cursor.fetchone()

s="select * from information_schema.columns where table_schema = test and table_name = " + data[0]

s= """select column_name from information_schema.columns
where table_schema = 'test' and table_name='ball'
order by ordinal_position"""

cursor.execute(s)
data = cursor.fetchall()
columns = [i[0] for i in data]
print(columns)

with open('data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    num=1
    count=0
    for row in reader:
        count+=1
        if count%2!=0:
            continue
        values=[]
        sentimentBat=""
        sentimentBowl=""
        #print(row[7])
        if re.search("OUT",row['runs'])!=None or int(row['runs'])==0:
            sentimentBowl="positive"
            sentimentBat="negative"
        elif int(row['runs'])>=3 or re.search("dropped",row['comment'],re.I)!=None:
            sentimentBat="positive"
            sentimentBowl="negative"
        
        for i in columns:
            if row.get(i)!=None:
                values.append(row[i])
            
        s="insert into ball("+",".join(columns)+")"\
       "values("+str(int(values[0]))+","+str(int(values[1]))+","+str(int(values[2]))+",'"+str(values[3])+"','"+str(values[4])+"',"+str(float(values[5]))+","+str(float(values[6]))+",'"+str(values[7])+'\',"'+str(values[8][0:250])+'"'+",1,'"+sentimentBat+"','"+sentimentBowl+"')"
        print(s)
        cursor.execute(s)
        
#db.commit() #---> be careful, don't use 

# disconnect from server
db.close()


