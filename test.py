from neovim import attach
import sys
sys.path.append('/home/teto/nvim-palette/rplugin/python3')
# from palette import __init__ # noqa: E402
# from __init__ import * # noqa: E402
from palette import PalettePlugin  # noqa: E402

# echo serverlist() or v:servername in a running nvim
nvim = attach('socket', path=sys.argv[1])
p = PalettePlugin(nvim)
p.get_propositions([{ 'menus': 'toto'}])
