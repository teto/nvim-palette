import panda as pd
import logging
from palette.source import Source
from typing import Dict

logger = logging.getLogger(__name__)


class PaletteKeymaps(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._keymaps = pd.DataFrame()

    @Source.name.getter
    def name(self):
        """ (temporary) rename to ease testing"""
        return "keymaps"

    def serialize(self, filter_cmd):
        # keymaps = self.retrieve_menus()
        # name
        return self.keymaps.desc.tolist()

    @property
    def keymaps(self,):
        if self._keymaps.empty or None:
            self._keymaps = self.load_keymaps()
        return self._keymaps

    def map2command(self, line):

        logger.debug("Looking for keymap %s" % line)
        # TODO trigger the keymap 
        # df = self.menu_entries[self.menu_entries.desc == line]
        # if len(df) > 0:
        #     row = df.iloc[0, ]
        #     cmd = row['command']
        #     logger.info("Found command %s" % cmd)
        #     return cmd

    def load_keymaps(self, ):
        """
        rhs
        """
        entries : Dict  = {}
        logger.debug('Loaded keymaps ')
        # :h nvim_get_keymap
        keymaps = self.vim.get_keymap("n")
        def build_leaf_entry(entry):
            """Build a menu entry"""
            # TODO use current mode, for now assume normal
            command = entry.get("mappings", []).get("n", "").get('rhs', "")
            return {entry["name"]: command}

        keymaps = pd.DataFrame.from_dict({
            'desc': list(entries.keys()), 
            'command': list(entries.values())
        })
        return keymaps


