import re
import os
f1=open("OnlyCommentary1.txt","r")
f2=open("OnlyCommentary2.txt","r")
f3=open("AllNamedLines.txt","w")

team=open("Team_Members.txt","r")
teams=team.readlines()
rcb=[" ".join(i.split()[1:]) for i in teams[1:12]]
csk=[" ".join(i.split()[1:]) for i in teams[14:25]]

pat1="[0-9]"


#get player names, 'players' contains all player names for matching
players=[]
for player in rcb:
    player=player.split()
    for i in player:
        if len(i)>1:
            players.append(i)
for player in csk:
    player=player.split()
    for i in player:
        if len(i)>1:
            players.append(i)

files=[f1,f2]
for file in files:
    file.seek(0,0)
    output=open('RegEx_Ouput_'+file.name,'w')
    while(file.tell()<int(os.path.getsize(file.name))):
        l=file.readline()
        if re.match(l,'\n')!=None:
            continue
        res=re.match(pat1,l)
        num=l
        com=''
        if(res!=None):
            while(file.tell()<int(os.path.getsize(file.name))):
                l=file.readline()
                res=re.match(pat1,l)
                if res==None:
                    com+=l
                else:
                    #set to number of bytes before
                    file.seek(file.tell()-len(num)-1)
                    break
        #num has over number + ball number
        output.write(num)
        
        #process com1 - commentary for each ball
        com1=re.split('\.|!',com)
        for line in com1:
            for player in players:
                res=re.search(player,line,re.I|re.M)
                #if line has player name
                if(res!=None):
                    output.write(line.strip())
                    output.write('. ')
                    break
        output.write('\n\n')
    output.close()
        
        
    
