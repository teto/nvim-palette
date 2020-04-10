{-# LANGUAGE TemplateHaskell #-}
module Palette (plugin) where

import Neovim
-- import Palette.Menu ()

-- call fzf with menus
plugin :: Neovim () NeovimPlugin
plugin = wrapPlugin Plugin
    { environment = ()
    , exports     = [ 
        -- $(function' 'fibonacci) Sync 
        -- to export a command
        -- command :: String -> Name -> Q Exp
        --PaletteSelect({

      ]
    }


-- main :: IO ()
-- main = neovim defaultConfig
--     { plugins = plugins defaultConfig ++ [ plugin ]
--     }

