import MySQLdb
import csv
import re
import subprocess
import time

db = MySQLdb.connect("localhost","root","admin","test",charset = 'utf8')

cursor = db.cursor()

playerStats={}



"""s="CREATE TABLE IF NOT EXISTS matches (ID INT, stadium VARCHAR(50), year INT, type VARCHAR(10), tournament VARCHAR(20), matchNo INT, primary key(ID))"
cursor.execute(s)

s="CREATE TABLE IF NOT EXISTS teams(matchID INT, team1 varchar(30), team2 varchar(30), FOREIGN KEY(matchID) references matches(ID))"
cursor.execute(s)

s="CREATE TABLE IF NOT EXISTS tossResult(matchID INT, innings1 varchar(30), innings2 varchar(30), FOREIGN KEY(matchID) references matches(ID), primary key(matchID))"
cursor.execute(s)"""

s= """select column_name from information_schema.columns
where table_schema = 'test' and table_name='teamstats'
order by ordinal_position"""

cursor.execute(s)
data = cursor.fetchall()
columns = [i[0] for i in data]
#print(columns)

s='select ID from matches'
cursor.execute(s)
data = cursor.fetchall()
matchIDs = [i[0] for i in data]
#print(matchIDs)

f1=open("teams1.txt",'r')
teamA=[i.strip() for i in f1.read().split(',')]
f2=open("teams2.txt",'r')
teamB=[i.strip() for i in f2.read().split(',')]

#print(teamA,teamB)

"""for player in teamA[1:]:
    s="insert into players(name,team,matchID) values('"+player+"','"+teamA[0]+"',1)"
    cursor.execute(s)
for player in teamB[1:]:
    s="insert into players(name,team,matchID) values('"+player+"','"+teamB[0]+"',1)"
    cursor.execute(s)"""
bestBatsman=""
bestBowler=""

#getting playerstats
for ID in matchIDs:
    s="select name,team from players where matchID="+str(ID)
    cursor.execute(s)
    data=cursor.fetchall()
    players=[]
    for i in data:
        players.append([[j.strip() for j in i[0].split() if len(j.strip())>1],i[1]])
    s="select bowler,batsman,runs from ball where matchID="+str(ID)
    cursor.execute(s)
    data1=cursor.fetchall()
    #print(data1)
    #print(players)
    #data1=(('Albie','Kallis','6'),)
    for player in players:
        runsTaken=0
        runsGiven=0
        wickets=0
        p=player[0]
        #print(p)
        typeP=None
        ballsFaced=0
        ballsBowled=0
        for data in data1:
            #print("data:",data)
            for p1 in p:
                #print("p1:",p1)
                if re.search(p1,data[0],re.I)!=None:
                    #print("aaaa")
                    if typeP==None:
                        typeP="Bowler"
                    elif typeP=="Batsman":
                        typeP="All rounder"
                    if re.match('out',data[2],re.I)!=None:
                        wickets+=1
                    else:
                        runsGiven+=int(data[2])
                    ballsBowled+=1
                    break
                if re.search(p1,data[1],re.I)!=None:
                    if typeP==None:
                        typeP="Batsman"
                    elif typeP=="Bowler":
                        typeP="All Rounder"
                    if data[2].isnumeric():
                        runsTaken+=int(data[2])
                    ballsFaced+=1
                    break
        #print(player,wickets,runs,typeP)
        sentiment=""
        strikeRate=0
        economy=0

            
        if runsTaken!=0 and ballsFaced!=0:
            strikeRate=runsTaken/ballsFaced*100
        if ballsBowled!=0 and typeP=="Bowler" or typeP=="All Rounder":
            economy=runsGiven/ballsBowled*6.0
        if strikeRate>=100 or (economy<8 and ballsBowled!=0 and typeP=="Bowler" or typeP=="All Rounder") or wickets>=1:
            sentiment="positive"
        else:
            sentiment="negative"
        #args=(' '.join(p),typeP,runs,wickets,0,balls,strikeRate,economy,player[1],ID)
        
        s="insert into playerstats values('"+" ".join(p)+"','"+typeP+"',"+str(wickets)+","+str(0)+","+str(ballsFaced)+","+str(strikeRate)+","+str(economy)+",'"+player[1]+"',"+str(ID)+",'"+sentiment+"',"+str(runsTaken)+","+str(runsGiven)+","+str(ballsBowled)+")"
        #print(s)
        #cursor.execute(s)
print("PlayerStats:")
s="select * from playerstats"
cursor.execute(s)
data= cursor.fetchall()
for i in data:
    print(i)
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
#s="select economy,name from playerstats where ballsBowled>0 and economy>0 order by economy"
#cursor.execute(s)
#print(cursor.fetchall())


#getting teamstats
teamStatsData=[]
for ID in matchIDs:
    score1=0
    wickets1=0
    score2=0
    wickets2=0
    for innings in [1,2]:
        s="select runs from ball where innings="+str(innings)+" and matchID="+str(ID)
        #print(s)
        cursor.execute(s)
        data = cursor.fetchall()
        runs = [i[0] for i in data]
        score=0
        wickets=0
        
        s="select max(over) from ball where innings="+str(innings)+" and matchID="+str(ID)
        cursor.execute(s)
        overs=cursor.fetchone()[0]+1
        
        for i in runs:
            if i.isnumeric()==True:
                score+=int(i)
            elif re.match('OUT',i,re.I):
                wickets+=1
        #print(score,wickets)
        runrate=score/overs
        s="select innings"+str(innings)+" from tossResult where matchID="+str(ID)
        cursor.execute(s)
        team=cursor.fetchone()[0]
        teamStatsData.append(str(ID)+","+str(innings)+","+str(score)+","+str(wickets)+","+str(overs)+",'"+team+"',"+str(runrate))
        if runrate>=8:
            sentiment="positive"
        else:
            sentiment="negative"
        if team=='Chennai':
            b1=BestBatsmanC
            b2=BestBowlerC
            win=0
        elif team=='Bangalore':
            b1=BestBatsmanB
            b2=BestBowlerB
            win=1
        s="insert into teamstats(matchID, innings, score, wickets, overs, team,RunRate,sentiment,bestBowler,bestBatsman,win) values("+str(ID)+","+str(innings)+","+str(score)+","+str(wickets)+","+str(overs)+",'"+team+"',"+str(runrate)+",'"+str(sentiment)+"','"+str(b2)+"','"+str(b1)+"',"+str(win)+")"
        #print(s)
        #cursor.execute(s)
print("\nTeamStats")
s="select * from teamstats"
cursor.execute(s)
data=cursor.fetchall()
#for i in data:
#    print(i)

#add sentiments to ball




#getting good balls for players
p1="Morkel"
s1='positive'




from tkinter import *

s="select name from players where matchID=1"
cursor.execute(s)
data=cursor.fetchall()
players=[]
for i in data:
    #print(i[0])
    players.append(i[0])

#players=['aaaa','bbbb']

p1=""
s1=""
    

def play():
    global master,p1,s1
    print(p1,s1)
    master.destroy()
    s="select * from playerstats"
    cursor.execute(s)
    data=cursor.fetchall()
    for player in data:
        #print(player)
        p2=player[0].split()
        #print(p2)
        for name in p2:
            if re.search(p1,name,re.I)!=None:
                #print(player)
                break
            
        #print(player[9])


    s="select * from ball"
    cursor.execute(s)
    data=cursor.fetchall()
    p1=p1.split()
    l=0
    times=[]
    for ball in data:
        #print(ball)
        bowler=ball[3]
        batsman=ball[4]
        players=[ball[3],ball[4]]
        sentimentBat=ball[10]
        sentimentBowl=ball[11]

        #print("Batting\n")
        #for batsman
        
        for p in p1:
            #print(p,batsman,sentimentBat)
            if re.search(batsman,p,re.I)!=None and re.search(s1,sentimentBat,re.I)!=None:
                print("Batting:  ",ball,'\n')
                l=1
                times.append([ball[5],ball[6]])
                break

        #print("Bowling\n")
        #for bowler
        for p in p1:
            #print(p,batsman,sentimentBat)
            if re.search(bowler,p,re.I)!=None and re.search(s1,sentimentBowl,re.I)!=None:
                print("Bowling:  ",ball,'\n')
                times.append([ball[5],ball[6]])
                break
            
    for t in times:            
        p=subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe","C:\\Anju\\Summer Project Stuff\\DBSentimentAnalysis\\match.avi","--start-time="+str(t[0])+" --stop-time="+str(t[1])])
        time.sleep(t[1]-t[0]+3)
        p.terminate()

        
def func1(value):
    global s1
    s1=value
    b = Button(master, text="OK", command=play)
    b.pack()

def func(value):
    global p1
    p1=value
     # default value
    sentiment=('Positive','Negative')
    variable = StringVar(master)
    variable.set('Choose Sentiment')
    wq = OptionMenu(master, variable,*sentiment,command=func1)
    
    wq.pack()


    
master = Tk()
text=Text(master)
text.insert(INSERT, "IPL MATCH\n")
text.insert(INSERT, "Bye Bye.....")
text.pack()
variable1 = StringVar(master)
variable1.set('Choose Player') # default value

w = OptionMenu(master, variable1,*players,command=func)
w.pack()

mainloop()




        

db.commit()
db.close()
