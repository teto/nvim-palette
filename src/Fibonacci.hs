{-# LANGUAGE TemplateHaskell #-}
module Fibonacci (plugin) where

import Neovim
-- import Fibonacci.Plugin (fibonacci)

-- | Neovim is not really good with big numbers, so we return a String here.
fibonacci :: Int -> Neovim env String
fibonacci n = return . show $ fibs !! n
  where
    fibs :: [Integer]
    fibs = 0:1:scanl1 (+) fibs

-- 
plugin :: Neovim () NeovimPlugin
plugin = wrapPlugin Plugin
    { environment = ()
    , exports     = [ $(function' 'fibonacci) Sync ]
    }

-- import qualified Fibonacci as Fibonacci

main :: IO ()
main = neovim defaultConfig
    { plugins = plugins defaultConfig ++ [ plugin ]
    }
