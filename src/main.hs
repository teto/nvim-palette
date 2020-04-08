{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE DeriveGeneric       #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE Trustworthy         #-}

module Main where

import Neovim
import qualified Fibonacci as Fibonacci
import Palette

-- import qualified Module.With.MyPlugin as MyPlugin
-- main :: IO ()
-- TODO pass a log
-- main = neovim defaultConfig { plugins = [Fibonacci.plugin] }
--

-- vim_command

main :: IO ()
main = do
  objects <- openMpack "/home/teto/nvim-palette/data/options_v2.mpack"
  putStrLn $ "Hello world" ++ (show objects)
