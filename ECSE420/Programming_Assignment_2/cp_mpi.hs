module Main	where

import Data.List (find)

main = putStrLn "Hi there"

--rref :: Fractional a => [[a]] -> [[a]]
--rref m = f m 0 [0 .. rows - 1]
--	where rows = length m
--		  cols = length (head m)

replace :: Int -> a -> [a] -> [a]
replace n e l = a ++ e : b
	where (a, _ : b) = splitAt n l

