module Main	where

import Data.List (find)
import Control.Parallel.MPI.Simple (mpiWorld, commWorld, unitTag, send, recv)

main :: IO ()

{- what if I read the first line to process 0 every time, and use the size of that to compute the total
	size of the array...?-}

main = mpiWorld $ \size rank ->
	if size < 1
		then putStrLn "At least one process is needed here..."
		else case rank of
			0 -> gatherSend commWorld y unitTag $ initial $ openFile [getArgs] ReadMode
			where y = 1 in 

			x -> do (msg, _status) <- recv commWorld 0 unitTag
				process msg
			_ -> return ()


initial f = 
--rref :: Fractional a => [[a]] -> [[a]]
--rref m = f m 0 [0 .. rows - 1]
--	where rows = length m
--		  cols = length (head m)

replace :: Int -> a -> [a] -> [a]
replace n e l = a ++ e : b
	where (a, _ : b) = splitAt n l

