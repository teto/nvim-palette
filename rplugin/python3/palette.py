"""
Description: Easy toggling ON/OFF of options
License: MIT
"""

import neovim
import msgpack
import logging
import gettext as g
import pandas as pd
import os
import json
from . import menus

logger = logging.getLogger('palette')

locale_dir = "/home/teto/neovim2/build/locale"


@neovim.plugin
class PalettePlugin(object):
    """
    Gather entries to fuzzy search
    """

    def __init__(self, nvim):
        """
        to ease testing (for instance in jupyter-console):
        from neovim import attach
        import sys
        # echo serverlist() or v:servername in a running nvim
        nvim = attach('socket', path='/tmp/nvimJHSJGG/0')
        sys.path.append('~/nvim-palette/rplugin/python3/palette')
        import palette as p

        """
        self.nvim = nvim

        if nvim.vars['palette_debug']:
            # logger.addHandler(NeoVimLoggerHandler(nvim))
            handler = logging.FileHandler("nvimpalette.log", delay=True)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
            handler.setFormatter(formatter)

        self.sources = []
        self.add_source( menus.PaletteMenus())

    @neovim.function('PaletteAddSource', sync=True)
    def add_source(self, src):
        """
        look at deoplete "find_rplugins"; it searches in
        runtime/rplugin/python3/deoplete for source files.
        it is called by deoplete.py:load_sources
        """
        self._sources[name] = 


    # @neovim.function('PaletteGetMenu', sync=True)
    # def get_menus(self, args):
    #     entries = self.retrieve_menus()
    #     keys = list(entries.keys())
    #     res = self.nvim.call('PaletteFzf', keys)

    @neovim.function('PaletteSelect', sync=True)
    def get_propositions(self, opts=[{'options': True}]):
        """
        Accept a dictionary:
            { name: filter }
        with filter being source-specific
        """
        entries = []
        logger.debug("options %r" % opts)
        opts = opts[0] # hack because vimL dict seems encapsulated into a list
        for name, match in opts.items():
            src = self._sources.get(name)
            entries.append(src.entries())

        logger.debug("Choosing between %s" % entries[:10])
        # res = self.nvim.call('PaletteFzf', entries)
        return entries

    @neovim.function('PalettePostprocessChoice', sync=True)
    def map_to_command(self, line):
        """
        Need to convert description back to its command

        Dispatch entry to the correct source so that it can act on it
        """
        line = line[0]
        logger.info("Trying to map '%s' (type %s)" % (line, type(line)))
        mark = line[0]



        return ":echom 'Nothing found for \"" + stripped + "\"'"



# class NeoVimLoggerHandler(logging.Handler):
#     def __init__(self, nvim):
#         super().__init__()
#         self.nvim = nvim

#     def emit(self, record):
#         msg = self.format(record).replace('"', '`')
