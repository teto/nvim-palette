module Palette where
import Data.ByteString.Lazy (writeFile, readFile)
import qualified Data.ByteString.Lazy.UTF8 as BLU
import Data.MessagePack
import Data.Either (fromRight)
import Data.Maybe (fromJust)
import Data.Serialize.Get (runGet)
import Data.Serialize (
    decodeLazy, Serialize, decode)
import qualified Data.Map as M

openMpack :: String -> IO [Entry]
openMpack filename = do
  optionsStr <- Data.ByteString.Lazy.readFile filename
  case (decodeLazy optionsStr) of
      Left errMsg -> error ("Failed loading " ++ filename ++ ":\n" ++ errMsg)
      -- entryLoadArray
      Right list -> case entryLoadArray list of
            Left errMsg -> error ("Failed loading " ++ filename ++ ":\n" ++ errMsg)
            Right ob -> return ob


-- to export a command
-- command :: String -> Name -> Q Exp

-- full_name='aleph', abbreviation='al',
-- short_desc=N_("ASCII code of the letter Aleph (Hebrew)"),
-- type='number', scope={'global'},
-- vi_def=true,
-- redraw={'curswant'},
-- varname='p_aleph',

data Scope = Global | Window | Buffer
  deriving (Read, Show)

-- instance Enum Scope
--   toEnum "Global" = Global
--   fromEnum Global = "Global"

data Entry = Entry {
  entryFullname :: String
  , entryShortDesc :: String
  , entryScope :: [Scope]
  , entryVarname :: String
} deriving (Show);

entryFromObject :: Object -> Either String Entry
entryFromObject _ = Left "wrong value"
entryFromObject (ObjectMap m) = let
    fullname = fromJust $ M.lookup (ObjectString (BLU.fromString "fullname")) m
  in
  -- Left "unimplemented"
  Right Entry {
    entryFullname = "toto"
    , entryShortDesc = "temp"
    , entryScope = [Global]
    , entryVarname = "p_temp"
  }
-- entryFromObject (ObjectArray m) = Right $ entryLoadArray m

entryLoadArray :: Object -> [Entry]
entryLoadArray _ = undefined
entryLoadArray (ObjectArray []) = []
entryLoadArray (ObjectArray (x:toto)) = case entryFromObject x of
    Left err -> undefined
    Right entry -> [entry] ++ entryLoadArray (ObjectArray toto)

-- calls menu_get('*')
-- getMenus :: 


-- instance Serialize Entry where
--   put = undefined
--   get = undefined
-- loadEntry ::


