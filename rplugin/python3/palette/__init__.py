#!/usr/bin/env python
"""
Description: Easy toggling ON/OFF of options
License: GPLv3
"""

import neovim
import logging
import gettext as g
import pandas as pd
import os
import json
import re
from abc import abstractmethod
from palette.menus import PaletteMenus
from palette.settings import SettingsSource

logger = logging.getLogger(__name__)
handler = logging.FileHandler("nvimpalette.log", delay=True)
formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
handler.setFormatter(formatter)

debug_level = logging.DEBUG


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
            logger.addHandler(handler)
            logger.setLevel(debug_level)

        """ { mark: src } dict """
        self.sources = {}
        # TODO should be done from vim side ?
        if nvim.eval("exists('*menu_get')"):
            m = PaletteMenus(nvim)
        # print("test", m.name)
            self.add_source(m)

        # need to import first
        m = SettingsSource(nvim)
        self.add_source(m)

    @neovim.function('PaletteAddSource', sync=True)
    def add_source(self, src):
        """
        look at deoplete "find_rplugins"; it searches in
        runtime/rplugin/python3/deoplete for source files.
        it is called by deoplete.py:load_sources
        """
        if self.sources.get(src.mark):
            raise Exception("A source is already registered with mark %s " % src.name)

        self.sources[src.mark] = src


    # @neovim.function('PaletteGetMenu', sync=True)
    # def get_menus(self, args):
    #     entries = self.retrieve_menus()
    #     keys = list(entries.keys())
    #     res = self.nvim.call('PaletteFzf', keys)

    @neovim.function('PaletteGetEntries', sync=True)
    def get_propositions(self, opts=[{'options': True}]):
        """
        Accept a dictionary:
            { name: filter }
        with filter being source-specific
        """
        entries = []
        logger.debug("options %r" % opts)
        opts = opts[0] # hack because vimL dict seems encapsulated into a list
        for _, src in self.sources.items():
            filter_cmd = opts.get(src.name)
            if filter_cmd:
                temp = src.serialize(filter_cmd)
                temp2 = map(lambda x: "[" + src.mark + "]" + x, temp )
                entries.append(list(temp2))
            else:
                logger.debug('No filter for source %s' % src.name)

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

        # for now mark = first character, could be the last
        # mark = line[0]
        pattern = re.compile("\[(?P<mark>.+)](.*)")
        res = pattern.match(line)
        if not res:
            # raise Exception ("No mark in the selected entry")
            logger.error("No mark in the selected entry")
            return None

        logger.info("match=%s" % res)
        mark = res.group(1)
        logger.info("Looking for mark  '%s'" % mark)

        # look at the mark
        cmd = None
        src = self.sources.get(mark)
        logger.info("module %s" % __name__)
        # for src in self.sources:
        #     if src.mark == mark:
        if src is not None:
                logger.info("Mark mapped to src %s" % src.name)
                cmd = src.map2command(res.group(2))
                # break

        if cmd is None:
            # todo use echomsg instead
            logger.error("No mark in the selected entry")
            raise Exception ("Could not generate an appropriate cmd")

        return cmd

        # return ":echom 'Nothing found for \"" + line[0] + "\"'"



# class NeoVimLoggerHandler(logging.Handler):
#     def __init__(self, nvim):
#         super().__init__()
#         self.nvim = nvim

#     def emit(self, record):
#         msg = self.format(record).replace('"', '`')

