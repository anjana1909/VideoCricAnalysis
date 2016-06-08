import os
import re

os.chdir('C:\Anju\Summer project stuff\Cricket_Anu\CricInfo')
f=open('Commentary_output1.txt','r')
f1=open('onlyballs.txt','w')
f2=open('endofover.txt','w')
while(f.tell()<int(os.path.getsize('.\Commentary_output1.txt'))):
    l=f.readline()
    pattern="^((([1][0-9]|[0-9])[\.][0-6])[ ]*[\n])$"
    p=re.compile(pattern)
    res=p.match(l)
    l2=""
    if(res!=None):
        f1.write(l)
        c=0
        while(f.tell()<int(os.path.getsize('.\Commentary_output1.txt'))):
            t=f.tell()
            l1=f.readline()
            res=p.match(l1)
            if(res==None):
                l1.strip()
                pat="^End of over"
                p1=re.compile(pat)
                if(p1.match(l1)):
                    f2.write(l1)
                    for i in range(5):
                        f2.write(f.readline())
                    f2.write('\n\n')
                    l2+='\n'
                    break
                else:
                    pat1="\n"
                    p2=re.compile(pat1)
                    if(p2.match(l1)):
                        c+=1
                    if(c<2):
                        l2+=l1
            else:
                f.seek(t,0)
                l2+='\n'
                break
    #l2+="\n"
    f1.write(l2)
f.close()
f1.close()
f2.close()
            
