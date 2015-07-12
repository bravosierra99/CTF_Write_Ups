#!/usr/bin/python
list = [-1, 17,-11,3,-8,5,14,-3,1,6,-11,6,-8,-10];
answer = [];
answerconverted = [];
next = 0;
for x in range(0,25):
	answer = [];
	answer.append(x);
	next = x
	for y in list:
		next = next + y;
		if (next < 0 or next >25):
			break;
		answer.append(next);
	if len(answer) == 15:
		break;
print answer;
output = "";
for x in answer:
	answerconverted.append((x-13)%26);
	output = output + chr(x+ord('a'));
print answerconverted;
print output
output = ""
for x in answerconverted:
	output = output + chr(x+ord('a'));
print output;

		
			
			

	
	
