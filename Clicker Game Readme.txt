# Goals of the program

To be a simple game where you click on moving shapes to earn points. If you miss too many times, you lose. If you get all of the shapes, you move on to the next level. If you complete every level, you win. (I typoed win as wine. You can wine too if you wish.)

**NOTE:** This .txt is actually a Markdown file. Rename it to .md for a better view if your editor supports it.

# Learning Objectives Demonstrated (in this project)

## TL;DR:

- 01 DONE
- 02 DONE?
- 03 not done
- 04 DONE
- 05 DONE
- 06 DONE
- 07 DONE
- 08 not done
- 09 not done
- 10 DONE
- 11 not done
- 12 DONE
- 13 DONE
- 14 DONE
- 15 DONE
- 16 DONE
- 17 DONE
- 18 not done
- 19 DONE
- 20 DONE
- 21 not done
- 22 not done
- 23 not done
- 24 DONE
- 25 DONE

## 01

DONE.

Lines 527, 589, and 592.

I'm not sure if you wanted a hardcoded list or not. I manage many lists in this program, and all are filled with valid elements, but none are hardcoded.

## 02

DONE - mostly.

I can't recall anywhere where I concatenate any lists/strings, however, I do build tuples. Maybe it's a bit of a stretch, but they are technically an iterable type that's being concatenated together from a number of variables. :-D

As for removing elements, I do clear() a list on line 280 and remove characters from strings via slicing on lines 56, 57, 498, 499, 547, and 548.

I index on lines 469, 470, and 526 (and probably more).

I loop through lists on lines 284, 354, and others. I also have a HUGE chunk of code I commented out, but didn't delete where I looped through a list on line 306.

## 03

NOT done.

I found no use for it. All of my lists are things I'm loading from files and I'm not creating any lists from larger lists or other collections.

I know it doesn't count for this project, but I just want to note that I was using list comprehensions weeks before they were introduced to the class.

## 04

DONE - twice. Three times if you count the abandoned work in the "first idea" folder. I was going to make a program the drew a voronoi diagram, but then I realized that I couldn't think of enough for it to do that would meet enough objectives. I was going to brute for the generation of a picture, but I don't know the math well enough to build a voronoi data structure that I think could have met everything.

Lines 41 and 412.

## 05

DONE.

Every line with error_log.write().

Lines 271, 509, 511, 517, and more.

I was also going to make a tiny program to make the game.data text file, but I'm out of time.

## 06

DONE

Lines 40, 58, 412, 450, 501, and 549.

## 07

DONE

game_levels on line 569 is filled with other lists on line 557, which are themselves lists of tuples from line 552.

## 08

NOT done.

I would have done this if I had gone with my original idea to draw a voronoi graphic, or possibly if I had time to create graphics objects to bounce around the screen instead of just shapes.

## 09

NOT done. Because of 08.

## 10

Line 356 hits each object just once per update.

All of the file operations are very close too, but the go_back_one_line() function creates a tiny amount of redone work.

## 11

NOT done.

I didn't manually do any kind of data sorting/searching in this project.

## 12

DONE.

Lines 16 and 84.

## 13

DONE.

Lines 72, as well as lines 106, 114, 120, and more.

## 14

DONE.

Line 106.

## 15

DONE.

Lines 296, and 298.

## 16

DONE.

I've never heard the term "receiver syntax" before this class, and I can't find this term used anywhere online. I vaguely remember someone once saying it during a lab session. I think I found it in the slides.

This is just where you call a method on a particular instance of a class, right?

Line 362, and many, many others satisfy this.

## 17

DONE.

Lines 164 and 225.

## 18

NOT done, technically.

My GameObject class is a wrapper around GFillableObject, but that's not really the same thing. Inheritance just didn't work in this case. A wrapper made more sense.

## 19

DONE.

Line 533.

## 20

DONE.

Line 403.

## 21

NOT done.

I literally had zero project ideas that would involve doing this.

## 22

NOT done. But, damn it! I tried!

I was planning, and all sorts of ready to use sets to store my level data, but the problem was that when I was ready to save it I had a tuple and sets don't work with tuples.

I played around with things for a bit, but I couldn't force it. Tuples were the way to go with what I had set up and with how levels were being defined for this game it made sense to order them in a simple list.

I tried to find other uses for sets, like maybe for the game object, or their descriptions, since they all have unique names, but that didn't work out either as I would have needed to re-write big chunks of the program. So again, I had to give up on finding a use for sets. This project just didn't need them. :-/

## 23

NOT done.

Because of 22.

## 24

DONE.

Both game_levels and the GameObject classes are very data driven.

I'm not sure which lines you want me to highlight here. The definitions of the structures, or where some of their data gets used.

Lines 84, 164, 225, and 602 define the structures.

Lines 289, 295, and 297 show control flow.

Line 563 shows use.

## 25

DONE.

See load_next_level() on line 282, and load_game_from_file() on line 417.

# Additional Info

This project, unlike all of the others, had a .github directory. This caused a hard to find bug that actually had nothing to do with Python and everything to do with my dev tools.

I was getting FileNotFound exceptions when trying to open settings.txt, even though it was RIGHT THERE in the main project folder. I was also NOT getting any errors when creating files, writing to them, and then immediately re-opening them for reading, yet the files didn't seem to exist anywhere that I could see.

Searching my HDD via "find . -iname 'test_filename.txt'" showed that my project's working directory was not set to the main project directory, but instead the .github directory for some reason. I don't know if deleting that directory will have any effect on your end, but on mine it seems to be harmless.

Just an FYI.
