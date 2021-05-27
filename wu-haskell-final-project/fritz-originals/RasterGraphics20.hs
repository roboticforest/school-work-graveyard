
{- A concise implementation of 2D graphics in Haskell,
   by Fritz Ruehr, following ideas of Conal Elliott 

   New version: Spring 2020 (uses RenderBMP20.hs  -}

module RasterGraphics20 where

import RenderBMP20


---------------
-- Basic type definitions, plus hex-coded colors


{-
ALL FOUR OF THESE ARE NOT USED BY FRITZ!!!
-}
type Space  = (Double,Double)

type Color  = Int

type Pict   = Space -> Color

type Figure = Space -> Maybe Color              -- Nothing == <transparency>

[black, white, red, orange, yellow, green, blue, purple] = 
	[0x000000, 0xffffff, 0xff0000, 0xff9900, 0xffff00, 0x00ff00, 0x0000ff, 0x6600cc] :: [Int]


---------------
-- Blank canvas and "compositing" (layering)

blank = \(x,y) -> Nothing                       -- an empty (transparent) "slide"

-- `on` places Figure f on top of Figure g, resulting in a Figure

f `on`  g = \p -> case f p of Nothing -> g p ; Just c -> Just c

layer figs = foldl on blank figs

-- `orr` places a Figure against background color b to get a complete Picture
-- [ think: point p = (x,y) ]

f `orr` b = \p -> case f p of Nothing -> b   ; Just c -> c


---------------
-- Rendering and overall graphic sizing parameters (see also RenderBMP20.hs)

range n = [-m..m] where m = (n-1) / 2

space w h = map (\y -> (map (\x -> (x,y)) (range w))) (reverse (range h))

render fig w h = map (map (scale mag mag (fig `orr` white))) (space w h)

paint pic file = gen file (round x) (round y) (concat (render pic x y))
                 where size = base*mag
                       x = 2*size-1
                       y =   size-1
base = 30.0
mag  =  3.0		-- use (30,3) for Hugs, (50,8) for GHCi (on my Mac)


---------------
-- Basic geometric notions and transformations

dist  x y   = sqrt (x^2 + y^2)

shift n m f = \(x,y) -> f (x-n, y-m)
scale n m f = \(x,y) -> f (x/n, y/m)
skew  n m f = \(x,y) -> f (x-(n*y/m), y)

swap (x,y) = (y,x)
diag f = f . swap

flipv f = \(x,y) -> f (x,-y)
fliph f = \(x,y) -> f (-x,y)


---------------
-- Simple geometric figures and patterns

within x n = -m<=x && x<=m where m = (n-1)/2

rect w h c = \(x,y) -> when (x `within` w && y `within` h) c

when   b c = if b then Just c else Nothing

circ   r c = \(x,y) -> when (dist x y < r) c
square r c = rect (2*r) (2*r) c

radial   c = \(x,y) -> when (p x y) c
             where p x y = if y==0 then True else even (round (x / y))

stripe k c = skew k k (\(x,y) -> when (round x `mod` round k == 0) c)

checker  c = \(x,y) -> when (even (round x + round y)) c


---------------
-- Example graphics

squirc n = circ n yellow `on` square n blue

simple = (circ 5 red `on` shift 4 0 (rect 10 20 blue)) `on` radial yellow

--

tree   = shift 0 3 (circ 9 green) `on` shift 0 (-8) (rect 5 11 black)

wagon  = layer [shift 0 5 (rect 25 5 red), shift (-6) 0 wheel, shift 6 0 wheel]
         where wheel = circ 4 black

scene  = tree `on` sun `on` field
         where sun   = shift 17 10   (circ 5 yellow)
               field = shift 0 (-13) (\(x,y) -> when (y `within` 3) green)

scene2 = shift (-18) (-10) (scale 0.75 0.75 wagon) `on` scene

-- https://willamette.edu/~fruehr/354/figs/images/scene2.png


target = layer (zipWith circ [1,3..13] (cycle [red,white]))

galaxy = skew 3 3 (target `on` scale 2 2 (checker green))

stripy = scale 2 1 (stripe 4 blue)

messy  = skew 2 3 (layer [scale (-2) 2 (stripe 5 purple), target, stripy])

-- https://willamette.edu/~fruehr/354/figs/images/messy.png


mickey = layer [circ 9 black, shift 8 8 ear, shift (-8) 8 ear]
         where ear = circ 5 black

dizzy  = skew 2 3 (mickey `on` radial orange `on` checker yellow)

-- https://willamette.edu/~fruehr/354/figs/images/dizzy.png
