{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE DeriveGeneric       #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE Trustworthy         #-}

module Main where

import Neovim
import qualified Fibonacci as Fibonacci

-- import qualified Module.With.MyPlugin as MyPlugin
main :: IO ()
main = neovim defaultConfig { plugins = [Fibonacci.plugin] }
