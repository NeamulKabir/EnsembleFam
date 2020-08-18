import sys

fname = sys.argv[1]
labelFile = (sys.argv[2]).split("/")

label = labelFile[-1].split(".")[0]

with open(fname) as f:
	content = f.readlines()

rowList = list()
colList = list()
for line in content:
	data = line.strip().split("\t")
	rowList.append(data)

row = len(rowList)
col = len(rowList[0])

fwName = sys.argv[3]

fw = open(fwName, 'w')

for i in range(col):
	for j in range(row):
		fw.write("%s\t" % rowList[j][i])
	fw.write("%s\n" % label)
fw.close()