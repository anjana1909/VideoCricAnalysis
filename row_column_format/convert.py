import re
import os
import codecs
import csv



def getOver_Ball(f,x):
    #add batsman name in the column (both the batsmen, hightlight the one
                #that is batting in that ball
    #add bowlers name in respective column
    #get the runs - no run, number run, leg byes, FOUR, SIX
    #other context --> text has to be parsed!!
    global inn
    while(f.tell()<int(os.path.getsize('.\MatchSeg'+str(x)+'.anvil'))):
        l=f.readline()
        pattern="[ ]*\<track name=\"Over_Ball\""
        res=re.match(pattern,l)
        while(res!=None):
            l=f.readline()
            res1=re.match("[ ]*<el",l)
            if(res1!=None):
                l2=l.split()
                l1=[]
                l3=[l2[2].split('=')[1].split('"')[1],l2[3].split('=')[1].split('"')[1]]
                start.append(l3[0])
                end.append(l3[1])
            res1=re.match("[ ]*<attribute",l)
            if(res1!=None):
                l1=l.split('>')
                l1=l1[1].split('<')[0].split('.')
                if (l1[0]=='0'and l1[1]=='1'):
                    inn+=1
                over.append(l1[0])
                ball.append(l1[1])
                innings.append(str(inn))
                
            res2=re.match("[ ]*</track",l)
            if(res2!=None):
                break
        pattern="[ ]*\<track name=\"Commentary\""
        res=re.match(pattern,l)
        while(res!=None):
            l=f.readline()
            res1=re.match("[ ]*<attribute",l)
            if(res1!=None):
                newl=""
                res2=None
                while(res2==None):
                    l+=newl
                    newl=f.readline()
                    res2=re.match("[ ]*</attribute",newl)
                l1=l.split('>')
                l1=l1[1].split('<')[0]
                l2=l1.split()
                #till to is encountered
                l0=""
                n=0
                for k in l2:
                    if(k!="to"):
                        l0+=k
                        n+=1
                    else:
                        break
                bowler.append(l0)
                batsman.append(l2[n+1].split(',')[0])
                run=l2[n+2].split(',')[0]
                p=0
                if(run=='FOUR'):
                    runs.append('4')
                elif(run=='SIX'):
                    runs.append('6')
                elif(run=='no'):
                    runs.append('0')
                    p=1
                else:
                    runs.append(run)
                    p=1
                if p==1:
                    comment.append(" ".join(l2[5:]))
                else:
                    comment.append(" ".join(l2[4:]))
            res2=re.match("[ ]*</track",l)
            if(res2!=None):
                break
        
            
            

inn=0

innings=["Innings"]
over=["Over"]
ball=["Ball"]
start=["Start time"]
end=["End time"]
bowler=["Bowler"]
batsman=["Batsman"]
runs=["Runs"]
comment=["Comment"]
for i in range(1,16):
    f=codecs.open('.\MatchSeg'+str(i)+'.anvil',encoding='utf-16',mode='r')
    getOver_Ball(f,i)

lists=[[1,2,3,4],[5,6,7,8]]
with open('data.csv','w') as csvfile:
    writer=csv.writer(csvfile)
    for val in zip(innings,over,ball,start,end,bowler,batsman,runs,comment):
        writer.writerow(val)

        

