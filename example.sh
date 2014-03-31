pwd=$(pwd)
for first in "A" "B" "C" "D" 
do
	for second in "A" "B" "C" "D"
	do
		find $pwd/$first/$second/*/*.json | awk '{print "python json2flat.py " $1}'
	done
done