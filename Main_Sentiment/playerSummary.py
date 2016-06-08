import MySQLdb
import csv
import re
import subprocess
import time


db = MySQLdb.connect("localhost","root","admin","test",charset = 'utf8')

cursor = db.cursor()


print("\n")
print("Chennai:")
s="select name,type,strikeRate,economy,wickets,ballsFaced,sentiment from playerstats where matchID=1 and ballsFaced>0 and team='Chennai' order by strikeRate DESC"
cursor.execute(s)
BestBatsmanC=cursor.fetchone()[0]
print("BestBatsman:",BestBatsmanC)
s="select name,type,strikeRate,economy,wickets,ballsFaced,sentiment from playerstats team where matchID=1 and ballsBowled>0 and economy>0 and team='Chennai' order by economy"
cursor.execute(s)
BestBowlerC=cursor.fetchone()[0]
print("BestBowler:",BestBowlerC)

print("Bangalore:")
s="select name,type,strikeRate,economy,wickets,ballsFaced,sentiment from playerstats where matchID=1 and ballsFaced>0 and team='Bangalore' order by strikeRate DESC"
cursor.execute(s)
BestBatsmanB=cursor.fetchone()[0]
print("BestBatsman:",BestBatsmanB)
s="select name,type,strikeRate,economy,wickets,ballsFaced,sentiment from playerstats team where matchID=1 and ballsBowled>0 and economy>0 and team='Bangalore' order by economy"
cursor.execute(s)
BestBowlerB=cursor.fetchone()[0]
print("BestBowler:",BestBowlerB)




from tkinter import *


s="select name from players where matchID=1"
cursor.execute(s)
data=cursor.fetchall()
players=[]
for i in data:

    players.append(i[0])


p1=""
s1=""
process=subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe","C:\\Anju\\Summer Project Stuff\\DBSentimentAnalysis\\match.avi"]).terminate()


def play():
    global master,p1,s1
    print(p1,s1)
    master.destroy()
    s="select * from playerstats"
    cursor.execute(s)
    data=cursor.fetchall()
    found=0
    for player in data:
        p2=player[0].split()

        for name in p2:
            if re.search(p1,name,re.I)!=None:
                found=1
                break

    #if found!=1:
    #messagebox.showinfo("Not found", "Player not found")
    s="select * from ball"
    cursor.execute(s)
    data=cursor.fetchall()
    p1=p1.split()
    l=0
    times=[]
    for ball in data:
        bowler=ball[3]
        batsman=ball[4]
        players=[ball[3],ball[4]]
        sentimentBat=ball[10]
        sentimentBowl=ball[11]

        #batting
        for p in p1:
            if re.search(batsman,p,re.I)!=None and re.search(s1,sentimentBat,re.I)!=None:
                l=1
                times.append([ball[5],ball[6]])
                break
        #bowling
        for p in p1:
            if re.search(bowler,p,re.I)!=None and re.search(s1,sentimentBowl,re.I)!=None:
                times.append([ball[5],ball[6]])
                break
            
    for t in times:
        global process
        process=subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe","C:\\Anju\\Summer Project Stuff\\DBSentimentAnalysis\\match.avi","--start-time="+str(t[0])+" --stop-time="+str(t[1])])
        time.sleep(t[1]-t[0]+3)
        process.terminate()

def stop():
    master.destroy()
    global process
    if process:
        process.terminate()
    exit()
        
def func1(value):
    global s1
    s1=value
    b = Button(master, text="OK", command=play)
    b.pack()
    b1=Button(master,text="Cancel",command=stop)
    b1.pack()

def func(value):
    global p1
    p1=value
    sentiment=('Positive','Negative')
    variable = StringVar(master)
    variable.set('Choose Sentiment')
    wq = OptionMenu(master, variable,*sentiment,command=func1)
    wq.pack()


    
master = Tk()
text=Label(master,text="Player summary for IPL match 2010 Bangalore vs Chennai",font="Arial 15")
text.pack()
variable1 = StringVar(master)
variable1.set('Choose Player')

w = OptionMenu(master, variable1,*players,command=func)
w.pack()

mainloop()

db.commit()
db.close()
