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

logger = logging.getLogger('palette')

locale_dir = "/home/teto/neovim2/build/locale"

@neovim.plugin
class PalettePlugin(object):

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
            handler = logging.FileHandler(".nvimpalette.log", delay=True)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
            handler.setFormatter(formatter)

        self.df = self.load()

    def load(self):
        r = g.bindtextdomain('nvim', locale_dir)

        fields = ["full_name", "short_desc", "abbreviation", "scope"]
        # we embed the mpack file to deal with old nvim
        folders = [
            self.nvim.eval('$VIMRUNTIME').strip(),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
        ]

        fname = None
        # TODO let the user be able to override default paths
        try:
            fname = self.nvim.vars['palette_descriptions_file']
            logger.info("using configured g:palette_descriptions_file value")
        except Exception as e:
            logger.debug("Looking for descriptions files")
            # NvimDevLintToggle
        if fname is None:

            for folder in folders:
                fname = os.path.join(folder, 'data', 'options.mpack')
                logger.debug("Checking path '%s'" % fname)
                if os.path.isfile(fname):
                    break

        # fname = '/home/teto/neovim2/build/runtime/data/options.mpack'
        # fname = os.path.join(filedir, "options.mpack"),
        logger.info("Loading descriptions from file %s" % fname)

        try:
            fd = open(fname, 'rb')
            res = msgpack.loads(fd.read())
        except Exception as e:
            logger.error('Could not load definitions')
            self.nvim.command("echomsg 'Could not load definitions'")
            raise e

        df = pd.DataFrame([], columns=fields)
        for entry in res:
            temp = {k.decode(): v.decode() if isinstance(v, bytes) else v for k, v in entry.items()}

        # unpacker = msgpack.Unpacker(fd, use_list=False)
        # for unpacked in unpacker:
        #     print(unpacked)
            df = df.append(temp, ignore_index=True)
        # df = pd.DataFrame(res, columns=fields)
        # df.from_records(res)
        logger.debug(df["scope"].head())
        df["scope"] = df["scope"].apply(lambda x: [e.decode() for e in x])
        # print(df)
        return df

    @neovim.function('PaletteGetMenu', sync=True)
    def get_menus(self, args):

        # self.nvim.command("let m = export_menus('', 'n')")
        # self.nvim.command("let r = json_encode(m)")
        # TODO ask for a fix should work without r
        self.nvim.command("let g:r = 'toto'")
        # m = self.nvim.vars["m"]
        m = "test"
        r = self.nvim.vars["r"]
        logger.info("m=%r r=%r" % (m, r))
        entries = []

        # d = json.loads()
        res = self.nvim.call('PaletteFzf', entries)

    @neovim.function('PaletteGetBools', sync=True)
    def get_bools(self, args):
        """
        fzf accepts a list as input
        """
        entries = []
        df = self.df
        # for now drop columns without desc
        # df = df.drop("short_desc")
        # sel = df[df.scope == "global"]
        sel = df
        sel = sel[sel.type == "bool"]
        for row in sel.itertuples():
            if "global" in row.scope:
                try:
                    logger.debug("scope =%r" % row.scope)
                    short_desc = g.gettext(row.short_desc)
                    short_desc += " (switch %s)" % ("OFF" if self.get_option_value(row.full_name, row.scope[0]) else "ON ")
                    entries.append(short_desc)
                except Exception as e:
                    logger.debug("Option '%s' seems not supported" % row.full_name)

        logger.debug("Sending entries=%r" % entries)
        res = self.nvim.call('PaletteFzf', entries)

    def get_option_value(self, full_name, scope):
        source = None
        if scope == "global":
            source = self.nvim.options
        elif scope == "window":
            source = self.nvim.current.window.options
        elif scope == "buffer":
            source = self.nvim.current.buffer.options
        # TODO else throw error ?
        return source[full_name]

    @neovim.function('PalettePostprocessChoice', sync=True)
    def TranslateToCommand(self, line):
        # BUG in client ? line is a list while vimscript sends it as a string
        line = line[0]
        logger.info("Translating command %s (type %s)" % (line, type(line)))
        stripped = line[:-len(" (switch OFF)")]
        logger.debug("Looking for short_desc=%s" % stripped)
        df = self.df[self.df.short_desc == stripped]
        if len(df) <= 0:
            # TODO escape it replace('"','\\"')
            return ":echom 'Nothing found for \"" + stripped + "\"'"

        row = df.iloc[0, ]
        cmd = "set " + row['full_name'] + "!"
        return cmd


# class NeoVimLoggerHandler(logging.Handler):
#     def __init__(self, nvim):
#         super().__init__()
#         self.nvim = nvim

#     def emit(self, record):
#         msg = self.format(record).replace('"', '`')
