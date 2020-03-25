{-# LANGUAGE TemplateHaskell #-}
module Fibonacci (plugin) where

import Neovim
import Fibonacci.Plugin (fibonacci)

plugin :: Neovim () NeovimPlugin
plugin = wrapPlugin Plugin
    { environment = ()
    , exports     = [ $(function' 'fibonacci) Sync ]
    }


main :: IO ()
main = neovim defaultConfig
    { plugins = plugins defaultConfig ++ [ plugin ]
    }
