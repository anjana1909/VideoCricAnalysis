f1=open("MatchSeg1.anvil",'r')
f2=open("MatchSeg1_new.anvil",'w')
f3=open("OnlyCommentary1.txt",'r')
Lines=f1.readlines()
Over_ball="    <track name=\"Over_Ball\" type=\"primary\">\n"
Com_head="    <track name=\"Commentary\" type=\"primary\">\n"
i=0

while(i<len(Lines)):
	print(Lines[i])
	if(Lines[i]==Over_ball):
		print("aaa")
		j=i+1
	if(Lines[i]!=Com_head):
		f2.write(Lines[i])
	else:
		f2.write(Com_head)
		break
	i+=1
print j
i=j
Comm=f3.readlines()
j=0
end="    </track>\n"
com_start="        <attribute name=\"token\">"
com_end="</attribute>"
while(i<len(Lines)):
	f2.write(Lines[i])
	i+=2
	com_body=com_start
	while(Comm[j]!="\n"):
		com_body+=Comm[j]
		com_body=com_body[:len(com_body)-1]
		j+=1
	j+=1
	com_body+=com_end
	f2.write(com_body)
	print(i)
	f2.write("\n")
	print(Lines[i])
	f2.write(Lines[i])
	i+=1
	if(Lines[i]==end):
		break
f2.write(Lines[len(Lines)-3])
f2.write(Lines[len(Lines)-2])
f2.write(Lines[len(Lines)-1])
f1.close()
f2.close()
f3.close()
