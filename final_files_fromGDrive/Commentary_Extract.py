f1 = open('Innings2_Commentary_output.txt')
f2 = open('OnlyCommentary2.txt', 'w')
Lines=f1.readlines()
i=0
string=""
o=0
b=1
inn=1
while i < len(Lines):
	string=str(o)+"."+str(b)+"\n"
	#print(string)
	text=Lines[i]
	#print(text)
	#print(i)
	if string in text:
		#print(string)
		i+=2
		f2.write(string)
		while(Lines[i]!="\n"):
			f2.write(Lines[i])
			i+=1
		f2.write("\n")
		b+=1
		if(b==7):
			b=1
			o+=1
		if(o>20):
			inn+=1
			o=0
			b=1
			if(inn==3):
				break
	else:
		i+=1
f1.close()
f2.close()





		
		




