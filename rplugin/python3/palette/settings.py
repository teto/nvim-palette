import pandas as pd
import msgpack
import logging
import os
from palette.source import Source
from typing import List

logger = logging.getLogger('palette')

class SettingsSource(Source):
    def __init__(self, *args, **kwargs):
        self._settings = pd.DataFrame()
        super().__init__(*args, **kwargs)

    @Source.name.getter
    def name(self):
        """ (temporary) rename to ease testing"""
        return "settings"

    def serialize(self, filters):
        return self.boolean_settings

    def map2command(self, entry):
        stripped = entry[:-len(" (switch OFF)")]
        logger.debug("Looking for short_desc=%s" % stripped)
        df = self.settings[self.settings.short_desc == stripped]
        if len(df) > 0:
            # TODO escape it replace('"','\\"')
            logger.debug("found a match=%s" % stripped)
            row = df.iloc[0, ]
            cmd = "set " + row['full_name'] + "!"
            return cmd

        raise Exception("Could not find a match for %s" % stripped)

    @property
    def boolean_settings(self, ) -> List[str]:
        """Get only boolean options"""
        entries = []
        # for now drop columns without desc
        # df = df.drop("short_desc")
        # sel = df[df.scope == "global"]
        sel = self.settings
        sel = sel[sel.type == "bool"]
        for row in sel.itertuples():
            # if "global" in row.scope:
                try:
                    # logger.debug("scope =%r" % row.scope)
                    short_desc = row.short_desc
                    short_desc += " (switch %s)" % ("OFF" if self.get_option_value(row.full_name, row.scope[0]) else "ON ")
                    entries.append(short_desc)
                except Exception as e:
                    logger.debug("Option '%s' seems not supported" % row.full_name)

        logger.debug("Sending entries=%r" % entries)
        return entries

    def get_option_value(self, full_name, scope):
        source = None
        if scope == "global":
            source = self.vim.options
        elif scope == "window":
            source = self.vim.current.window.options
        elif scope == "buffer":
            source = self.vim.current.buffer.options
        # TODO else throw error ?
        return source[full_name]


    @property
    def settings(self):

        if self._settings.empty is False:
            logger.debug("Returning from cache")
            return self._settings

        self._settings = self.load_options_definitions(True)
        return self._settings

    def load_options_definitions(self, force=False) -> pd.DataFrame:
        """
        Load vim option descriptions from a mpack file
        """
        # TODO restore gettext
        # r = g.bindtextdomain('vim', locale_dir)
        logger.debug("Loading descriptions ")

        fields = ["full_name", "short_desc", "abbreviation", "scope"]
        # we embed the mpack file to deal with old vim
        folders = [
            self.vim.eval('$VIMRUNTIME').strip(),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..')
        ]

        fname = None
        try:
            # let the user be able to override default paths
            fname = self.vim.vars['palette_descriptions_file']
            logger.info("using configured g:palette_descriptions_file=%s" % fname)
        except Exception as e:
            logger.debug("Looking for descriptions files")

        if fname is None:
            for folder in folders:
                fname = os.path.join(folder, 'data', 'options.mpack')
                logger.debug("Checking path '%s'" % fname)
                if os.path.isfile(fname):
                    break

        logger.info("Loading descriptions from file %s" % fname)

        try:
            fd = open(fname, 'rb')
            res = msgpack.loads(fd.read())
        except Exception as e:
            logger.error('Could not load definitions')
            self.vim.command("echomsg 'Could not load definitions'")
            raise e

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
        return df
