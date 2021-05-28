import sys
import math

hmmfile = sys.argv[1]
posfile = sys.argv[2]
flag = sys.argv[3]


with open(hmmfile) as f:
	content = f.readlines()

sz = len(content)

with open(posfile) as f:
	positions = f.readlines()


## to identify the start of features in the output file
flagStr = "E-value  score  bias"


evalList = list()
bitsList = list()


for pos in positions:
	val = int(pos.strip())
	line1 = content[val + 4].strip()
	line2 = content[val + 5].strip()
	e_val = 0.0;	bit_sc = 0.0

	if(len(line1) > 1 and line1[0].isdigit()):
		line = line1
	elif(len(line2) > 1 and line2[0].isdigit()):
		line = line2
	else:
		line = "null"

	if line != "null":
		data = line.split()
		temp_val = float(data[3])
		if temp_val == 0.0:
			e_val = -999
		else:
			e_val = math.log(temp_val)
		bit_sc = float(data[4])
	
	
	evalList.append(e_val)
	bitsList.append(bit_sc)

fwName = sys.argv[4]

if flag == '1':
	fw = open(fwName, 'w')
else:
	fw = open(fwName, 'a')


for feature in evalList:
	fw.write("%.3f\t" % feature)
fw.write("\n")

for feature in bitsList:
	fw.write("%.3f\t" % feature)
fw.write("\n")

fw.close()
#print("extracted features %d" % len(evalList))