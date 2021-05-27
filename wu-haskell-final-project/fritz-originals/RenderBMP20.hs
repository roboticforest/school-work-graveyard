
module RenderBMP20 where

import Data.List
import System.IO
import Data.Word (Word8)
import Foreign.Marshal.Array

---------------

gen file = -- write ("C:\\Users\\fruehr\\Desktop\\pics\\"++file++".bmp")	-- Windows
           write ("/Users/fruehr/Desktop/pics/"++file++".bmp")			-- Mac

write fn w h pix = do f <- openBinaryFile fn WriteMode
                      hPutBytes f (map fromIntegral (bmp w h pix))
                      hClose f

hPutBytes :: Handle -> [Word8] -> IO ()
hPutBytes h ws = withArray ws $ \p -> hPutBuf h p $ length ws

---------------

bmp w h pix = header w h ++ raster w h pix

header w h = magic ++ concatMap (bytes 4) 
			              [size+offset, 0, offset, 40, w, h, bitplanes, 0, size, res, res, 0, 0]
             where magic = [0x42, 0x4D]
                   size = h * nhm 4 (3 * w)
                   offset = 54
                   bitplanes = 1572865
                   res = 2835

raster w h pix = concat (reverse (bunch 4 w 3 0 (map (bytes 3) pix)))

bunch k w n p [] = []
bunch k w n p xs = (concat as ++ pad) : bunch k w n p bs
                   where (as, bs) = splitAt w xs
                         pad = replicate (k - ((w*n) `mod` k)) p

---------------

nhm k n = if n `mod` k == 0 then n else k * (1 + n `div` k)

numl b = unfoldr (\n -> if n > 0 then Just (n `mod` b, n `div` b) else Nothing)

bytes k n = take k (numl 256 n ++ repeat 0)

---------------

testbytes :: [Int]
testbytes = 
  [	0x42, 0x4D, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x36, 0x00, 0x00, 0x00, 0x28, 0x00,
	0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x18, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x13, 0x0B, 0x00, 0x00, 0x13, 0x0B, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00,
	0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00]