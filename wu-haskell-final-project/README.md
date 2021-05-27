# Willamette University: Functional Programming with Haskell Class - Final Project

This was my final project from CS-354: Functional Programming with Haskell.

# The Assignment

Study and use a small graphics library our professor, Fritz Ruehr, created and generate a few image files. Specifically, we needed to:

1. Define at least one new type of figure or pattern.
2. Define at least two new kinds of transformations.

I did that, but I also re-wrote the entire library. 🤦‍♂️

Professor Fritz admitted that he wasn't much of a graphics guy, so his library ended up being a little awkward to use. There were a couple of magnitude and scaling variables that needed played with to get an image the right size, plus some type definitions that didn't seem to be used anywhere.

I rebuilt and improved his library. All drawing is now done in a square space with coordinates going from -1 to 1. This space is automatically scaled to fit within the drawing area. I also implemented anti-aliasing, improved shape masking, and instead of outputting Windows Bitmap (BMP) files I generate Portable Pixmap (PPM) files.
