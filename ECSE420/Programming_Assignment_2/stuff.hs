module Main where

import System.Environment
import Data.List
import System.IO

main = print $ x : [3] 
		where x = [4, 5]


readDouble :: String -> Double
readDouble = read