import csv
from itertools import islice
from threading import Thread

def getData(x,y):
    with open('Dictionary.csv') as csvreader:
        with open('MDictionary.csv','a',newline='') as csvwriter:
            write = csv.writer(csvwriter)
            senti = csv.reader(csvreader)
            for s in islice(senti,x,y):
                if(int(s[2])>0 or int(s[1])>0):
                    #print(s)
                    write.writerow(s)

with open('Dictionary.csv') as csvreader:
    senti = csv.reader(csvreader)
    num=len(list(senti))
with open('Dictionary.csv') as csvreader:
    with open('MDictionary.csv','w',newline='') as csvwriter:
        write = csv.writer(csvwriter)
        senti = csv.reader(csvreader)
        for s in islice(senti,0,1):
            print(s)
            write.writerow(s)

x=1
y=8000
number_of_threads=(num-1)//8000
threads=[]
for i in range(0,number_of_threads):
    t=Thread(target=getData,args=(x,y))
    threads+=[t]
    t.start()
    x+=8000
    y+=8000
    #print(x,y)
t=Thread(target=getData,args=(x,num-1))
threads+=[t]
t.start()

for x in threads:
    #pass
    x.join()
