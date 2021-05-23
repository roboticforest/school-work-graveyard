# Willamette University: Python 3 Class - Final Exam Project

![Gameplay Demo](https://github.com/roboticforest/school-work-graveyard/blob/main/wu-python-final-project/github-media/gameplay-demo-converted-by-ezgif.com-gif-maker.gif "Gameplay Demo")

---

## Assignment

We were given a list of 25 learning objectives that had been covered since the midterm exam. It was decided that we would *not* be doing a final exam and instead were allowed to work on whatever "mini-project" we wanted, so long as we hit about 18 of the learning objectives presented.

### My First Idea: Voronoi Cells

My original idea was to create a simple program to draw Voronoi cells given point data read from a text file. Writing the parser for the point file was fun, but I didn't think my design was going to be complex enough to hit enough objectives so I scrapped that work and decided to make a small game.

### My Second Idea: Click On The Shapes Game

I made a small game that someone described as an "Ant Squisher clone" (I've never played that game 🤷‍♂️). The goal of the game is to remove all of the moving shapes from the play area by clicking on them with your mouse.

The game only supports two shapes, and two styles of object movement, but there is room in the code for that to easily grow. It would have supported three shapes, but due to bugs in the graphics library I used this was not something I could get completely working in the time I had available to me so "wondering triangles" had to be scrapped.

The program is completely data-driven. The size, shape, color, speed, and point value of each object is read from a plain-text file. That same file also describes all of the levels in the game. Each level is a list of previously defined objects and a count of how many should be in play. Lastly, the game also loads its settings from a file.

I also implemented Python style comments and ensured that things like empty lines, missing data, and more wouldn't confuse the game file reader. Very little data is actually required (only names and kinds), and if anything vital is missing or incorrect the objects are ignored.

The names of objects are completely arbitrary, they just need to be unique so they can be referred to when defining levels.

#### Example game.data file:

```python
new object
name = racecar  # A fast red block.
kind = slider  # Slider is a falling block.
color = red  # Hex values should work too.
size = 25  # pixels wide/high.
speed = 3
points = 30

new object
name = ping pong ball  # A speedy, small white ball.
kind = bouncer  # Bouncer is a pong-like ball.
color = white
size = 10  # pixel radius.
speed = 3
points = 30

new level
1, ping pong ball
1, racecar

new level
3, ping pong ball
2, racecar
```

---

# Copyright

Portable Graphics Library (PGL) © Professor Eric Roberts

PGL was provided to students at Willamette University as an educational tool in the Computer Science Department and was required for many assignments and class projects.
