
import pandas as pd
import msgpack
import logging
import os
from palette.source import Source


class PaletteKeymaps(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # nvim_get_keymap

    @Source.name.getter
    def name(self):
        """ (temporary) rename to ease testing"""
        return "keymaps"
