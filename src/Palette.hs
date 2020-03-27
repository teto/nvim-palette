module Palette where
import Data.ByteString.Lazy (writeFile, readFile)
import Data.MessagePack
import Data.Serialize.Get (runGet)
import Data.Serialize (
    decodeLazy, Serialize, decode)
import qualified Data.Map as M

-- ObjectArray [
openMpack :: String -> IO Object
openMpack filename = do
  optionsStr <- Data.ByteString.Lazy.readFile filename
  -- getArray
  -- ObjectArray
  -- return $ runGet $ get optionsStr
  -- decode
  -- decodeLazy
  case (decodeLazy optionsStr) of
  -- case Data.Aeson.eitherDecode filteredConnectionsStr of
  --     -- case Data.Aeson.eitherDecode "[]" of
      Left errMsg -> error ("Failed loading " ++ filename ++ ":\n" ++ errMsg)
      Right list -> return list

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

-- Serialize
} deriving (Show);
-- P.pretty . UTF8.toString <$> fromObject o
--     put (ObjectMap m)      =
entryFromObject :: Object -> Either String Entry
-- entryFromObject ::  -> Either String Entry
entryFromObject _ = undefined
-- m of type (M.Map Object Object )
entryFromObject (ObjectMap m) = 
  -- Left "unimplemented"
  Left Entry {
    entryFullname = fromJust M.Lookup "fullname"



-- instance Serialize Entry where
--   put = undefined
--   get = undefined

-- loadEntry ::


