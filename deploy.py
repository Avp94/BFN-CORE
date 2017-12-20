import os
top = raw_input("Enter topology(star/chain)-")
if top=="star":
	x1 = raw_input("enter no. of nodes-")
	x=str(x1)
	s = open("star.py").read()
	s = s.replace("5",x)
	f = open("star.py", 'w')
	f.write(s)
	f.close()
	os.system("sudo /usr/bin/core-gui /home/ashwin/star.py")
	f1 = open("star.py",'w')
	f1.write('')
	f1.close()

	with open("star1.py") as f:
		with open("star.py", "a") as f1:
			for line in f:
				f1.write(line) 
else:
	x2 = raw_input("enter no. of nodes-")
	x3=str(x2)
	s1 = open("chain.py").read()
	s1 = s1.replace("5",x3)
	f1 = open("chain.py", 'w')
	f1.write(s1)
	f1.close()
	os.system("sudo /usr/bin/core-gui /home/ashwin/chain.py")
	f1 = open("chain.py",'w')
	f1.write('')
	f1.close()
	with open("chain1.py") as f:
		with open("chain.py", "a") as f1:
			for line in f:
				f1.write(line) 

