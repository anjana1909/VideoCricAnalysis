import html2text
html = open("Commentary.html").read()
f=open("Commentary_output.txt",'w')
f.write(html2text.html2text(html))
f.close()
