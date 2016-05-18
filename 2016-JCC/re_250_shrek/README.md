[main]: https://github.com/bravosierra99/CTF_Write_Ups/2016-JCC/
# JCC: re_250 aka shrek

--------------
## Challenge details
| Contest   | Challenge     | Category  | Points    |
|:---------|:---    | :---  | :---  |
| JCC   | re_250 aka shrek  | Reversing | 250   |

**Description:**
*A reversing challenge binary with layers.

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

