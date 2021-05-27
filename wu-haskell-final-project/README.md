# Willamette University: Haskell Class - Final Project

This was my final project for CS-354: Functional Programming with Haskell.

# The Assignment

Study and use a small graphics library our professor, Fritz Ruehr, created and generate a few image files. Specifically, we needed to:

1. Define at least one new type of figure or pattern.
2. Define at least two new kinds of transformations.

I did that, but I also re-wrote the entire library. 🤦‍♂️

Professor Fritz admitted that he wasn't very experienced with graphics programming, so his library ended up being a little awkward to use. There were a couple of magnitude and scaling variables that needed to be manually played with to get an image the right size, plus some type definitions that didn't seem to be used anywhere, and one or two other things.

I decided to rebuild and improved his library. All drawing is now done in a square space with coordinates going from -1 to 1. This space is automatically scaled to fit within the drawing area, meaning the aspect ratio and pixel resolution of the final image are independent of the drawing space. I also implemented anti-aliasing, improved shape masking, and instead of outputting Windows Bitmap (BMP) files I generate [Portable Pixmap](https://en.wikipedia.org/wiki/Netpbm) (PPM) files.

