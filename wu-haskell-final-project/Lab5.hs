-- module Lab5(main) where
-- Not sure why I needed to comment out the module line in order
-- to get ghc to compile and link the file, but that was the only
-- solution I could find online.

import Prelude
import System.IO

{-
import RasterGraphics20
This import is not needed. This Lab5 file is based off of (and
extends) the code found in RasterGraphics and RenderBMP.

This code generates images as a full color, ASCII, Portable Pixmap.
-}


--------------------------------------------------
-- UTILITY FUNCTIONS
--------------------------------------------------

-- Distance from points A to B. Standard sqrt(a^2 + b^2) formula.
distance :: Point2D -> Point2D -> Double
distance (x1,y1) (x2,y2) = sqrt( (x2-x1)^2 + (y2-y1)^2 )

-- For boxes centered on the origin.
insideBox w h = \(x,y) ->
    if x <= w/2 && x >= (-w/2) && y <= h/2 && y >= (-h/2)
        then True
        else False


--------------------------------------------------
-- COMMON VECTOR TRANSFORMS APPLIED TO FIGURES
--------------------------------------------------

shift x y fig = \(startX, startY) -> fig (startX-x, startY-y)
scale x y fig = \(startX, startY) -> fig (startX/x, startY/y)

-- What do n and m mean/represent in this function!?
skew n m fig = \(x,y) -> fig (x - (n * (y/m) ), y)

-- Angle is in degrees: 1° * pi / 180 = 1rad
rotate degrees fig = \(startX, startY) ->
    let angle = degrees * pi/180 in
        fig (((cos angle) * startX) - ((sin angle) * startY),
             ((sin angle) * startX) + ((cos angle) * startY))


--------------------------------------------------
-- DATA REPRESENTATION
--------------------------------------------------

type Point1D = Double
type Point2D = (Double, Double)
type Color = (Double, Double, Double, Double) -- RGBA
type Figure = Point2D -> Color
type Space2D = [[Point2D]]
type ColorLayer = [[Color]]

-- Some basic predefined colors.
[black, white, red, orange,
 yellow, green, cyan, blue,
 magenta, brown,
 clear] =
    [(0,0,0,1), (1,1,1,1), (1,0,0,1), (1,0.5,0,1),
     (1,1,0,1), (0,1,0,1), (0,1,1,1), (0,0,1,1),
     (1,0,1,1), ((160/255),(90/255),(60/255),1.0),
     (0,0,0,0)] :: [Color]

capColor :: Color -> Color
capColor (r,g,b,a) = (capValue r,
                      capValue g,
                      capValue b,
                      capValue a)

capValue :: Double -> Double
capValue c =
    if c < 0.0
        then 0.0
        else if c > 1.0
                 then 1.0
                 else c

colorToRGBStr :: Color -> String
colorToRGBStr (r,g,b,_) =
    show red  ++ " " ++
    show green ++ " " ++
    show blue where
        step = (1/255)
        red = round (capValue(r)/step)
        green = round (capValue(g)/step)
        blue = round (capValue(b)/step)


--------------------------------------------------
-- FILE HANDLING
--------------------------------------------------

makeImgFile :: FilePath -> Int -> Int -> ColorLayer -> IO ()
makeImgFile fileName w h layer = do
    imgFile <- openFile fileName WriteMode

    -- P3 is a Portable PixMap magic number that specifies:
    -- - Full color, and
    -- - ASCII mode
    hPutStrLn imgFile ("P3")

    -- Write out width, height, and max color value:
    hPutStrLn imgFile (show w ++ " " ++ show h ++ " 255")
    
    -- Write out the raw pixel data:        
    -- map colorToRGBStr [color]
    -- mapM_ (\c -> putStr (c ++ " ")) rowOfLayer
    let rgbLayer = (map (map colorToRGBStr) layer)
    mapM_ (outputRow imgFile) rgbLayer where
        outputRow file (color1:color2:strings) = do hPutStr file (color1 ++ " "); outputRow file (color2:strings)
        outputRow file (color:[])              = hPutStr file (color ++ "\n")
        outputRow file []                      = hPutStr file "\n"


--------------------------------------------------
-- RENDERING
--------------------------------------------------

{-
Creates a list of n sampling points from the range [-1,1].

Effectively, the samples function overlays a grid of n cells on
the real line from -1 to 1 (both inclusive) and selects points
centered on each cell. This makes the range actually be from
-(1 - 1/n) to 1 - 1/n, with a step size between cell centers of
2/n.
-}
samples :: Int -> [Point1D]
samples n =
    case n of
        0 -> []
        _ -> [((1/ fromIntegral n)-1),((3/ fromIntegral n)-1)..(1-(1/ fromIntegral n))]
-- The above line is a simplified version of:
-- [-(1-(1/n)),((2/n)-(1-(1/n)))..(1-(1/n))]
-- ... which cuts down on precision errors.


{-
Creates a space for sampling colors from shapes. The space
created is automatically scaled so that a square [-1,1] space
remains squared and centered within the the given width and height.
The edges of the [-1,1] space will be flush with the smaller of the
width or height.
-}
sampleSpace :: Int -> Int -> Space2D
sampleSpace width height =
    let w = fromIntegral width
        h = fromIntegral height in
        if w >= h
            then map (\y -> (map (\x -> (x*(w/h), y)) (samples width))) (samples height)
            else map (\y -> (map (\x -> (x, y*(h/w))) (samples width))) (samples height)


{-
Runs a figure drawing function through a pixel sampling space and
produces a color sample layer. Note that a color layer is NOT a
pixel layer.
-}
renderFigure :: Figure -> Space2D -> ColorLayer
renderFigure fig space = map (map fig) space

{-
There's probably a much better way to do this. Currently I'm taking
a sample point, then splitting evenly into 4 subsamples based off
of the step size calculation used in samples. However, for this to
work I need to know the resolution of the original sample space
(the image width and height) in order to step the right amount away
from the center of the pixel that's being averaged.
-}

subSample :: Point1D -> Int -> [Point1D]
subSample point res = [point - step, point + step] where step = 1/(2 * fromIntegral res)

subSamples :: Int -> Int -> Point2D -> [Point2D]
subSamples renderSpaceWidth renderSpaceHeight = \(x,y) -> [(x,y) | x <- subSample x renderSpaceWidth, y <- subSample y renderSpaceHeight]

antiAlias :: Int -> Int -> Figure -> Point2D -> Color
antiAlias w h fig = \(x,y) -> avgListOfColors (map fig (subSamples w h (x,y))) where
    avgListOfColors (c:[]) = c
    avgListOfColors (c:colors) = averageColors c (avgListOfColors colors)

renderAAFigure :: Int -> Int -> Figure -> Space2D -> ColorLayer
renderAAFigure w h fig space = map (map (antiAlias w h fig)) space


{- WORK IN PROGRESS.
scaleDown :: ColorLayer -> ColorLayer
scaleDown [[],[]] = [[],[]]
scaleDown ((c1:c2:[]) : (c3:c4:[]) : rows) = (averageColors (averageColors c1 c2) (averageColors c3 c4)) : scaleDown (rows)
scaleDown ((c1:c2:row1) : (c3:c4:row2) : rows) = (averageColors (averageColors c1 c2) (averageColors c3 c4)) : scaleDown (row1:row2:rows)
-}


--------------------------------------------------
-- COMPOSITING
--------------------------------------------------

-- A simple average of each color component.
averageColors :: Color -> Color -> Color
averageColors (r1,g1,b1,a1) (r2,g2,b2,a2) =
    ((r1+r2)/2,(g1+g2)/2,(b1+b2)/2,(a1+a2)/2)

-- Alpha Blend formula for a color component:
-- C_a * A_a  +  C_b * A_b * (1 - A_a)
-- -----------------------------------
--       A_a  +  A_b * (1 - A_a)
alphaBlend :: Double -> Double -> Double -> Double -> Double
alphaBlend cA cB aA aB =
    if aA == 0 && aB == 0
        then 0.0
        else ((cA * aA) + (cB * aB * (1 - aA))) / (aA + (aB * (1 - aA)))

blendColor :: Color -> Color -> Color
blendColor (r1,g1,b1,a1) (r2,g2,b2,a2) = (rOut, gOut, bOut, aOut) where
    rOut = alphaBlend r1 r2 a1 a2
    gOut = alphaBlend g1 g2 a1 a2
    bOut = alphaBlend b1 b2 a1 a2
    aOut = a1 + a2 - (a1 * a2)

-- An empty figure/shape that draws nothing.
blank :: Figure
blank = \(x, y) -> clear


colorFill color = \(x, y) -> color

on :: Figure -> Figure -> Point2D -> Color
fig1 `on` fig2 = \samplePoint -> blendColor (fig1 samplePoint) (fig2 samplePoint)

masks :: Figure -> Figure -> Point2D -> Color
{-
fig1 `masks` fig2 = \samplePoint ->
    if fig1 samplePoint /= clear
        then fig2 samplePoint
        else clear
-}

fig1 `masks` fig2 = \samplePoint ->
    let (_, _, _, a1) = fig1 samplePoint
        (r2,g2,b2,a2) = fig2 samplePoint in
            (r2, g2, b2, (a1*a2))


-- Collapses a list of figures into one figure.
combine :: Foldable t => t Figure -> Point2D -> Color
combine figures = foldl on blank figures


--------------------------------------------------
-- FIGURES AND SHAPES
--------------------------------------------------

circle :: Double -> Color -> Point2D -> Color
circle radius color = \(x,y) ->
    if distance (0,0) (x,y) <= radius
        then color
        else clear

rectangle w h color = \(x,y) ->
    if insideBox w h (x,y) then color else clear

square diameter color = rectangle diameter diameter color

boxOutline w h thickness color = \(x,y) ->
    if (insideBox (w+(thickness/2)) (h+(thickness/2)) (x,y)) &&
       (not (insideBox (w-(thickness/2)) (h-(thickness/2)) (x,y)))
        then color
        else clear

gradientCircle radius (r,g,b,a) = \(x,y) ->
    let dist = distance (0,0) (x,y) in
        if dist <= radius
            then (r, g, b, a*((radius - dist)/radius))
            else clear

-----
-----
-----

mickey color = combine [shift 0 (1/4) (circle (3/4) color),
                        shift (-2/3) (-1/2) (circle 0.5 color),
                        shift  (2/3) (-1/2) (circle 0.5 color)]

boxTunnel w h thickness rot dist sizeStep rotStep distStep color = combine (makeBoxTunnelList w h thickness rot dist color) where
    (r,g,b,a) = color
    makeBoxTunnelList w h thickness rot dist color =
        if dist >= 1.0
            then []
            else (rotate rot (boxOutline w h thickness (r,g,b, a*(1-dist)))) :
                 (makeBoxTunnelList (w*sizeStep) (h*sizeStep) (thickness*sizeStep) (rot+rotStep) (dist+distStep) color)

grid color1 color2 = \(x,y) -> if odd (round x) && odd (round y) then color1 else color2

checker color1 color2 = \(x,y) -> if ((floor x) + (floor y)) `mod` 2 == 0 then color1 else color2

--------------------------------------------------
-- MAIN PROGRAM
--------------------------------------------------

--    (combine [mickey white, gradientCircle 1 white]) `masks` (square 1.5 red),
--    (mickey red) `masks` (gradientCircle 1 yellow),
--    skew 1 3 (mickey red),
--    skew 1 1 (rectangle 0.5 2 orange),
--    shift (-0.125) (-0.125) (circle 0.25 (0,0,0,0.5)),
--    shift 0.125 0.125 (circle 0.25 blue),
--    scale 1.5 0.5 (circle 1.0 red),
--    rotate 15 (square 2 yellow),
--    square 2 white,
--    boxOutline 2 2 0.1 green,

figures =
    [
    (mickey white `masks` gradientCircle 0.9 (1,1,1,2)) `masks` rectangle 1.75 1.5 yellow,
    scale 2 2 (checker black white),
    colorFill black
    ]

---- Green Swirling Tunnel
{-
figures =
    [
    boxTunnel 3 3 0.05 45 0 0.975 5 0.01 green,
    colorFill black
    ]
-}

---- Planets
{-
figures =
    [
    -- Big brown planet.
    shift 0.75 0.5 (circle 0.75 white) `masks` shift 0.85 0.55 (gradientCircle 0.85 (0,0,0,9)),
    shift 0.75 0.5 (circle 0.75 brown),

    -- Sun.
    circle 0.1 white,
    gradientCircle (1/3) yellow,
    gradientCircle 1 (1,1,0,(1/3)),
    gradientCircle 2 (0.5, 0, 0, 1),

    -- Cyan planet.
    shift (-1.5) 0.05 (circle 0.05 white) `masks` shift (-1.48) 0.05 (gradientCircle 0.05 (0,1,1,2)),
    shift (-1.5) 0.05 (circle 0.05 black),

    -- Tiny rear planet.
    shift (-0.75) (-0.01) (circle 0.005 white),
    
    colorFill black -- (0.125,0.125,0.125,1)
    ]
-}

renderWidth  = 1600
renderHeight = 900

main = do
    let fileName = "output.ppm"
    putStrLn("===== Lab 5 =====")
    putStrLn("Creating sample space...")
    let space = sampleSpace renderWidth renderHeight
    putStrLn("Rendering figures on the sample space...")
    let rendering = renderAAFigure renderWidth renderHeight (combine figures) space
    putStrLn("Saving rendering to file: " ++ fileName)
    makeImgFile fileName renderWidth renderHeight rendering
    putStrLn("Save complete!")




