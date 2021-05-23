# Willamette University: Python 3 Class - Final Project

![Gameplay Demo](https://github.com/roboticforest/school-work-graveyard/blob/main/wu-python-project-5/github-media/gameplay-demo.gif "Gameplay Demo")

---

## Assignment

Recreate the classic game Adventure.

We were supplied:

- A similar, simpler program called TeachingMachine.
- A minimal, empty skeleton program.
- Data files for the game.
- A small token scanner utility (which I didn't use).

This project was a huge exercise in refactoring, code porting, and (primarily) data parsing. A couple memorable moments include (a) an undocumented feature and (b) an easter egg I hid.

(a) The project instructions didn't mention anything about needing to implement a "catch all" player movement instruction. This was needed in order to make the "Darkness" room (see SmallRooms.txt or CrowtherRooms.txt) work correctly, moving the player to the "Pit" room and ending the game if they attempted to move through it without holding a lamp.

(b) For those of you reading this that are fans of [homestarrunner.com](homestarrunner.com) cartoons, I implemented an extension to how movement commands were interpreted simply to accommodate a [StrongBad](https://homestarrunner.com/sbemails) easter egg. Have fun. 😊