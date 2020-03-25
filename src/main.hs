{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE DeriveGeneric       #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE Trustworthy         #-}
-- module Data.MessagePackSpec
--import Data.MessagePack

---- https://hackage.haskell.org/package/data-msgpack-0.0.12/docs/Data-MessagePack.html
----
---- http://tanakh.hatenablog.com/entries/2009/12/09
--data Record = Record
--  { recordField1 :: Int
--  , recordField2 :: Double
--  , recordField3 :: String
--  }
--  deriving (Eq, Show, Generic)

--instance MessagePack Record

---- unpack

---- copied from
---- fields = ["full_name", "short_desc", "abbreviation", "scope"]
----
----
----
--main = do
--  sb <- newSimpleBuffer -- Packerが使うバッファ作成
--  pc <- newPacker sb -- Packer作成

--  packArray  pc 3     -- 三要素の配列をパックしますよ
--  packS32    pc 12345 -- 整数
--  packDouble pc 3.14  -- 浮動小数
--  packTrue   pc       -- Bool

--  bs <- simpleBufferData sb -- バッファにたまったデータを取り出す

--  print bs -- > "\147\205\&09\203@\t\RS\184Q\235\133\US\195"

--  up <- newUnpacker defaultInitialBufferSize -- Unpacker作成
--  unpackerFeed up bs -- Unpackerにデータを食わせる

--  resp <- unpackerExecute up -- デシリアライズ実行
--  guard $ resp==1 -- 成功すると1が返る
--  obj <- unpackerData up -- デシリアライズされたデータを取り出す

--  print obj -- > ObjectArray [ObjectInteger 12345,ObjectDouble 3.14,ObjectBool True]

module Main where

  import Neovim
  import qualified Fibonacci as Fibonacci

  -- import qualified Module.With.MyPlugin as MyPlugin
  main :: IO ()
  main = neovim defaultConfig { plugins = [Fibonacci.plugin] }
