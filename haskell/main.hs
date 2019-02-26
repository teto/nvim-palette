{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE DeriveGeneric       #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE Trustworthy         #-}
-- module Data.MessagePackSpec 

data Record = Record
  { recordField1 :: Int
  , recordField2 :: Double
  , recordField3 :: String
  }
  deriving (Eq, Show, Generic)

instance MessagePack Record



fields = ["full_name", "short_desc", "abbreviation", "scope"]
