module Palette where
import Data.ByteString.Lazy (writeFile, readFile)
import Data.MessagePack

openMpack :: String -> IO [Entry]
openMpack filename = do
  filteredConnectionsStr <- Data.ByteString.Lazy.readFile filename
  -- getArray
  case Data.Aeson.eitherDecode filteredConnectionsStr of
      -- case Data.Aeson.eitherDecode "[]" of
      Left errMsg -> error ("Failed loading " ++ filename ++ ":\n" ++ errMsg)
      Right list -> return list

-- full_name='aleph', abbreviation='al',
-- short_desc=N_("ASCII code of the letter Aleph (Hebrew)"),
-- type='number', scope={'global'},
-- vi_def=true,
-- redraw={'curswant'},
-- varname='p_aleph',

data Scope = Global | Window | Buffer 
  deriving Enum

-- instance Enum Scope
--   toEnum "Global" = Global
--   fromEnum Global = "Global"

data Entry = Entry {
  entryFullname :: String
  , entryShortDesc :: String
  , entryScope :: [Scope]
  , entryVarname :: String

} derive Show;

-- loadEntry ::


