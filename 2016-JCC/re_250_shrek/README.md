[main]: https://github.com/bravosierra99/CTF_Write_Ups/blob/master/2016-JCC/re_250_shrek/imgs/main.png
[auth]: https://github.com/bravosierra99/CTF_Write_Ups/blob/master/2016-JCC/re_250_shrek/imgs/auth.png
[step1]: https://github.com/bravosierra99/CTF_Write_Ups/blob/master/2016-JCC/re_250_shrek/imgs/step1.png
[step2]: https://github.com/bravosierra99/CTF_Write_Ups/blob/master/2016-JCC/re_250_shrek/imgs/step2.png
[step3]: https://github.com/bravosierra99/CTF_Write_Ups/blob/master/2016-JCC/re_250_shrek/imgs/step3.png
# JCC: re_250 aka shrek

--------------
## Challenge details
| Contest   | Challenge     | Category  | Points    |
|:---------|:---    | :---  | :---  |
| JCC   | re_250 aka shrek  | Reversing | 250   |

**Description:**
* A reversing challenge binary with layers.

Shrek: Ogres are like onions.
Donkey: They stink?
Shrek: Yes. No.
Donkey: Oh, they make you cry.
Shrek: No.
Donkey: Oh, you leave em out in the sun, they get all brown, start sproutin' little white hairs.
Shrek: NO. Layers. Onions have layers. Ogres have layers. Onions have layers. You get it? We both have layers.
Donkey: Oh, you both have layers. Oh. You know, not everybody like onions.*

First thing I like to do is run the program.  Running the program with an argument nets you a string letting you know that you don't have the correct flag

So I pop into IDA to take a look at what's going on.  Fortunately, it seems very straight forward.

![alt text][main]

There isn't too much to main.  We can see that it checks to make sure you have one argument and then calls two functions before either telling you that you win or lose.  The prep_the_objective function just calls mprotect on an area in memory that contains the code.  If you want to see just take a look at it yourself.  From this we can tell thats adding *write* privileges to that section of memory.  This means the code is going to modifying itself as it goes.  This could mean several things but it's usually a type of packing.  Let's take a look at auth know since it seems this will determine if we win or lose.

![alt text][auth]

OK so some things stand out.  IDA won't give us a graph view because it can't determine function boundaries.  We also see some *db* markers which means IDA thinks those sections are data.  These should not be in the code section...  at `0x08048461` we see it loads `eax` with `loc_804847F` which is just a section of code we can see right there on the screen.  Then it heads down into a loop which does some xoring on the location in `eax`.  So it definitely seems to be doing some unpacking.

Our team spent some time going forward from here.  The less intelligent members of the team (me) forgot how breakpoints work and tried to set a break point in the area of code that is being unpacked.  This causes the program to crash because, well, breakpoints (lookup how a debugger executes breakpoints if you don't understand why I'm dumb).  Smart people executed the loop a few a times until it had stopped unpacking the next section of code and then set a break point to see what the code is doing.  We continued this way until we discovered the first comparison with our flag.

The program had taken the first character of our argument and loaded it into `eax` and was comparing it against an ascii byte for *f*.  

At this point we had an idea of how the program would run.  It seemed as if it would continue to unpacke itself as it went along and do comparisons until it checked your whole flag.  A nice thing to notice is that it did not check the length of the flag.  At this point there are a lot of ways you can solve this program.  Mine is definitely not the best, but it does **WORK**.  Please explore other methods such as the approved write up from JCC.  However, let's show how I did it.

I made several assumptions.  One being that the *f* was a part of *flag{* and the second being that it would continue to check your flag using the same method.  Therefore, I could use conditional breakpoints to find when a comparison was being made.  I did that by using a test flag of *flag{zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz* and setting a breakpoint to check if `0x7A` was in `eax`.  I then set `eax` to the proper value of the comparison and continued on to the next comparison.  Voila, flag.  Slow and painful, but very flaggy.  Observe what that looks like.  


![alt text][step1]
![alt text][step2]
![alt text][step3]

Keep going and you get your flag which you then painstakingly convert from hex to ascii.  

A couple of notes
Don't set your watchpoint before starting the program.  You'll end up stopping in all sorts of initialization library calls.  So I stepped over the prep_the_battlefield and then set the watch point.
The up arrow is super handy for doing repetative work like this
Use GDB-PEDA, it's better in every possible way
Check out the python script I wrote based off of @ohai's pin script that will solve this automatically using intel's pin tool.  It's a way more automated way of doing this.
