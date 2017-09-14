import pandas as pd
from palette.source import Source

logger = logging.getLogger('palette')

class SettingsSource(Source):
    def __init__(self, vim):
        self._cached_opts = pd.DataFrame()
        Source.__init__(self, vim)

    @Source.name.getter
    def name(self):
        """ (temporary) rename to ease testing"""
        return "settings"

    def serialize(self, filters):
        return self.get_bools()

    def map2command(self, cmd):
        df = self.cached_options[self.cached_options.short_desc == stripped]
        stripped = line[:-len(" (switch OFF)")]
        logger.debug("Looking for short_desc=%s" % stripped)
        if len(df) > 0:
            # TODO escape it replace('"','\\"')
            row = df.iloc[0, ]
            cmd = "set " + row['full_name'] + "!"
            return cmd


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


    @property
    def cached_options(self):
        return self._cached_opts

    def load_options_definitions(self, force=False):
        """
        Load vim option descriptions from a mpack file
        """
        # r = g.bindtextdomain('nvim', locale_dir)

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
            logger.info("using configured g:palette_descriptions_file=%s" % fname)
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
            # todo maybe we can load it one at a time ?
            res = msgpack.loads(fd.read())
        except Exception as e:
            logger.error('Could not load definitions')
            self.nvim.command("echomsg 'Could not load definitions'")
            raise e

        # TODO here we should postprocess the data and cache it 
        # so that it's faster
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

        # todo convert scope to number
        df["scope"] = df["scope"].apply(lambda x: [e.decode() for e in x])
        return d

