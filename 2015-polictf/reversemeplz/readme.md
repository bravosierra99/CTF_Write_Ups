# polictf: reversemeplz

----------
## Challenge details
| Contest        | Challenge     | Category  | Points |
|:---------------|:--------------|:----------|-------:|
| polictf | Reversemeplz | Reversing |    200 |

**Description:**
>*Last month I was trying to simplify an algorithm.. and I found how to mess up a source really really bad. And then this challenge is born. Maybe is really simple or maybe is so hard that all of you will give up. Good luck!*

----------

After extracting the file you see that it is a standard ELF file.  So I load it up into IDA PRO.

Looking at the main file it seems pretty straight forward.  You can see it allocates some space on the stack and pushes a pointer to that space on the stack to the function _gets.  Ok so what we type in is going to be on the stack.  You can additionally see that it pushes that pointer into $esp so that the top of the stack points to a pointer of our buffer.  OK, seems straight forward.

You can test this functionality by running the program in gdb.  Set a breakpoint on main (`0x08048390`, which you can get from IDA).  Step through until the _gets then step over it.  You'll have to type your flag into the prompt.  

Now let's go back and look at IDA again.  It looks like we then push `$esi` into the `$esp` again, which doesn't change anything because it's already there.  Then it calls a function.  Directly after the function it executes `test	eax,eax` which is usally a good sign it's testing if the function returned properly.  This is confirmed by the fact that we jump if the function returns 0 over the part that seems to be generating our flag.  

Looking at the flag generating portion (starting at `0x080483C1`) you can see it is concatenating to generate the flag.  However, it looks as if it's using what we entered, so you probably won't be able to pull the flag out of the program.  We are going to have to figure out what the function call above does.

OK, so let's take a peak at the function at `0x08048801`.  The first part moves `0xF` values onto the stack using the 'rep movsd' instruction.  We see that there is a loop. If you look at the bottom of the loop it loops `0xF` times (could this be the length of our key?).  The first two portions of the loop compare your input string against `0x60` and `0x7A`.  Which we can assume means it's checking that the values are lowercase.  So our flag needs to be lower case.  The third portion calls a function and that function looks very complicated.  let's skip that for a moment.

After we exit that loop, assuming we passed the tests, we enter a second loop at `0x8048880`.  This loops `0xE` or 15 times.  It loads a character from our key (strangly it goes to the second character in the string since eax was incremented to 1) and then loads the last byte of the previous character.  In this case the first character from our key (remember ascii is only one byte).  Then it subtracts that byte from our character value and compares it to the value of the first strange value it loaded into the stack earlier from memory.  If we take a look at the values that were put on we see they are all very low hex numbers of very low negative signed numbers.  Based off the fact that they are low, and we are comparing the difference between lowercase numbers, it looks like he's checking our key characters against the character before them, starting with the first one.

Ok now we are getting somewhere.  let's go back to gdb and see what that big complicated function in the first loop does.  If you run through some test values for your flag and check at the end of first loop, you'll see that it appears to simply be rotating your flag values 13 to the right.  excellent!  

while we are in gdb let's go ahead and look at those strange values on the stack.  type in `x/15d 0xffffd330` any point after the values are loaded onto the stack and you get the numbers.  

At this point I felt like I probably had the information to solve.  I wrote up a python script to iterate through all possible start letters and then calculate the second letter based off of their expected difference. If when doing an operation I escape the bounds of lowercase letters then I break out of the loop and check the next possible start letter.  Once I found the proper sequence I rotate the letters back 13.  

```python
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
```
bam, I get onetwotheflagyo.  Look like a flag to me so I give it a spin in the program and sure enough it works!
 

