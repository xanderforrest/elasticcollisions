# elasticcollisions
A fun way to spend a Saturday.

In an effort to learn Pygame I decided to model balls. Bouncing a ball off a wall was very easy, and then I spent another four hours making the balls themselves bounce against each other. 

http://www.vobarian.com/collisions/2dcollisions2.pdf

This paper was very helpful, and was the algorithm implemented.

Turns out, my math/implementation wasn't the issue (well...) - The collision boxes meant the collisions were immediately revertising themselves, so the two balls just continued on their course. In the end, I implemented a small jump apart (1.5x the new velocity vector) so they don't continue to collide and can move apart from each other. 

It's a bit (understatement) janky, but my friends and family are worried about my excitement over balls bouncing so I must stop for now. 

Known bugs:
-Ball glitching into wall and moving horizontally/vertically
-Normalised vector of ball A --> B in a collision can, in rare cases, be 0, which breaks the algorithm causing the collision to be skipped
-Generally very ugly program
