import pandas as pd
import logging
from palette.source import Source
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class PaletteKeymaps(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keymaps = None

    @Source.name.getter
    def name(self):
        """ (temporary) rename to ease testing"""
        return "keymaps"

    def serialize(self, filter_cmd):
        return self.keymaps

    @property
    def keymaps(self,):
        if self._keymaps is None:
            self._keymaps = self.load_keymaps()
        return self._keymaps

    def map2command(self, line):

        logger.debug("Looking for keymap %s" % line)
        pattern = re.compile("(?P<name>.*)->(?P<rhs>.*)")
        res = pattern.match(line)
        if not res:
            # raise Exception ("No mark in the selected entry")
            logger.error("No rhs in the selected entry")
            return None
        mark = res.group(1)

        logger.info("Found group %s" % mark)
        # logger.info("Found command %s" % cmd)
        cmd = "toto"
        return cmd

    def load_keymaps(self, ):
        """
        rhs
        """
        entries : List  = []
        logger.debug('Loading keymaps...')
        # :h nvim_get_keymap
        def build_keymap_desc(entry):
            # """Build a keymap entry"""
            # TODO use current mode, for now assume normal
            # command = entry.get('rhs', "")
            # TODO use function to prettyprint the rhs, some characters
            # seem eaten
            return entry["lhs"] + " -> " + entry["rhs"]
        
        keymaps = self.vim.api.get_keymap( "n")
        import pprint as pp
        for entry in keymaps[:10]:
            pretty_entry = pp.pformat(entry)
            logger.debug(pretty_entry)
            desc = build_keymap_desc(entry)
            entries.append(desc)
        return entries


