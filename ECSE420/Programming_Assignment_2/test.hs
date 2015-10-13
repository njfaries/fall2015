module Main where

import Control.Parallel.MPI.Simple (mpiWorld, commWorld, unitTag, send, recv)

main :: IO ()
main = mpiWorld $ \size rank ->
   if size < 2
      then putStrLn "At least two processes are needed"
      else case rank of
         0 -> do (msg, _status) <- recv commWorld 1 unitTag
                 putStrLn msg
         1 -> send commWorld 0 unitTag "Hello World"
         _ -> return ()
