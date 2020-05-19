# defcon-quals-2020-whoooo-are-u
My work on the whooo-are-u ctf challenge

### Background 
This was very rushed code but it got the job done, as this was a two day CTF. My team and I mostly focused on this challenge. We didn't spend the whole weekend on it but a decent amount of hours. I was happy with the headway our small team accomplished. By the end of the CTF I think we were at around 300 subflags. 

The problem required you to connect to a port on a server and then solve a proof of work challenge. Once you spent a few cpu cycles on some math it would drop you into the nobody account on a shell. They provided you with a linux docker image that replicated the backend server, to allow you to test offline, and likely to give their servers a break. This docker image was .. something. Tons and tons of setuid binaries, seemly randomly tossed into an image (here:zardus/dc2020q-whooo-are-you) and posted online to annoy all of us. 

### My team's approach

We first worked to identify all of the setuid binaries and then started to see how we could trick them into reading flags. Each setuid binary could read a single flag file in /flags/<uid of binary>. After a lot of trial and error we managed to start grabbing flags but at this rate of manual flag collection I knew we would never hit the thousands of flags we needed to get any points. I figured out that gnu binaries often use the @/file/location format for files. I then automated the entire login and command scripting required to connect to the server: wru.py. I then grep'd all of the 'gnu' named setuid binaries from the list and then tried to bruteforce our way to some flags. Lucky enough we got about 100 this way. My teammate tried the same trick earlier on with simply binary /flag/<uid> and also grabbed a fair number of flags.
  
We spend more time doing manual flag collection, snagging a few one by one. The admins of the game switched up the format of the server output, which broke my script. I spent more time fixing it and making the code handle more variations from the server, and finished just a few moments before the CTF was over. 

## Closing thoughts

Overall this has been one of the most fun ctf challenges I've ever encountered. Hats off to oooverflow for putting this one together. 

### How to use this code

You can modify the testparam variable to fuzz command line options in order to get subflags from all of the setuid binaries. " -f " and " @" were both fruitful. We didn't have time to try this, but we assumed " -v ", " -d ", and other debug and verbose command line options would be fruitful. cmd.sh contains all of the setuid binaries that you want to test. I'd also watch out for the apps in the list that go interactive, without closing right away. Those can be tested manually as they will break automation unless you add a feature to timeout and exit your tests.
