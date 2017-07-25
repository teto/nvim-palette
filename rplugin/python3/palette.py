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
        # self.refresh_menu = True
        self._cached_menu = pd.DataFrame()
        self._cached_opts = pd.DataFrame()

        if nvim.vars['palette_debug']:
            # logger.addHandler(NeoVimLoggerHandler(nvim))
            handler = logging.FileHandler("nvimpalette.log", delay=True)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
            handler.setFormatter(formatter)

        self.nvim.subscribe("update_menu")

    @property
    def cached_menus(self):
        return self._cached_menu

    @cached_menus.setter
    def cached_menus(self, val):
        self._cached_menu = val

    @property
    def cached_options(self):
        return self._cached_opts


    def load_options_definitions(self, force=False):
        """
        Load vim option descriptions from a mpack file
        """
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
        # logger.debug(df["scope"].head())
        df["scope"] = df["scope"].apply(lambda x: [e.decode() for e in x])
        # print(df)
        return df

    # @neovim.function('PaletteGetMenu', sync=True)
    # def get_menus(self, args):
    #     entries = self.retrieve_menus()
    #     keys = list(entries.keys())
    #     res = self.nvim.call('PaletteFzf', keys)

    @neovim.function('PaletteSelect', sync=True)
    def get_propositions(self, opts=[{'options': True}]):
        entries = []
        logger.debug("options %r" % opts)
        opts = opts[0] # hack because vimL dict seems encapsulated into a list
        if opts.get('options'):
            entries += self.get_bools()

        if opts.get('menus'):
            menus = self.retrieve_menus()
            # keys = list(menus.keys())
            entries += menus.desc.tolist()

        logger.debug("Choosing between %s" % entries[:10])
        res = self.nvim.call('PaletteFzf', entries)

    def retrieve_menus(self, force=False):
        """
        TODO factor 
        TODO build a pandaframe along the way to optimize
        TODO on update_menu notification reload menus
        """

        # self.nvim.command("let m = export_menus('', 'n')")
        # self.nvim.command("let r = json_encode(m)")
        # TODO ask for a fix should work without r
        # self.nvim.command("let g:r = 'toto'")
        # # m = self.nvim.vars["m"]
        # m = "test"
        # r = self.nvim.vars["r"]
        # logger.info("m=%r r=%r" % (m, r))
        # entries = []
        # self.menus
        entries = {}
        if not self.cached_menus.empty and force is False:
            return self.cached_menus

        returned_menus = self.nvim.eval("menu_get('')")
        logger.debug('Loaded menus %s', returned_menus)
        self.refresh_menu = False

        def build_leaf_entry(entry):
            """Build a menu entry"""
            # TODO use current mode, for now assume normal
            command = entry.get("mappings", []).get("n", "").get('rhs', "")
            return {entry["name"]: command}

        def build_entries(menus, prefix=""):
            """
            returns a list of entries
            """
            entries = {}
            import pprint as pp
            for entry in menus:
                # name/hidden/enabled/submenus
                # pp.pprint(stream=)
                pretty_entry = pp.pformat(entry)

                # logger.debug('Parsing entry: %s', pretty_entry)
                # logger.debug('submenus value: %s', entry.get("submenus"))
                # logger.debug('submenus value: %s', entry.get("submenus"))
                if entry.get("submenus"):
                    # if it's a top menu
                    subentries = build_entries(entry["submenus"])
                    # logger.debug('subentries: %s', subentries)
                    entries.update(subentries)
                else:
                    subentry = build_leaf_entry(entry)
                    logger.debug('subentry=%s', pretty_entry)
                    entries.update(subentry)

            return entries

        entries = build_entries(returned_menus)
        self.cached_menus = pd.DataFrame.from_dict(
                { 'desc': list(entries.keys()), 'command': list(entries.values())}
                )
        # return entries
        return self.cached_menus

    # @neovim.function('PaletteGetBools', sync=True)
    def get_bools(self, ):
        """Get only boolean options"""
        entries = []
        if not self.cached_options.empty and force == False:
            return self.cached_options

        # else load descriptions

        # TODO load it on demand
        df = self.load_options_definitions(True)
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
        return entries

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
    def map_to_command(self, line):
        """
        Need to convert description back to its command

        first check if it's a menu description, then check for option desc
        """
        line = line[0]
        logger.info("Trying to map '%s' (type %s)" % (line, type(line)))
        logger.info("from\n %s " % self.cached_menus)
        df = self.cached_menus[self.cached_menus.desc == line]
        if len(df) > 0:
            row = df.iloc[0, ]
            cmd = row['command']
            logger.info("Found command %s" % cmd)
            return cmd
        else:
            df = self.cached_options[self.cached_options.short_desc == stripped]
            stripped = line[:-len(" (switch OFF)")]
            logger.debug("Looking for short_desc=%s" % stripped)
            if len(df) > 0:
                # TODO escape it replace('"','\\"')
                row = df.iloc[0, ]
                cmd = "set " + row['full_name'] + "!"
                return cmd
        return ":echom 'Nothing found for \"" + stripped + "\"'"



# class NeoVimLoggerHandler(logging.Handler):
#     def __init__(self, nvim):
#         super().__init__()
#         self.nvim = nvim

#     def emit(self, record):
#         msg = self.format(record).replace('"', '`')
