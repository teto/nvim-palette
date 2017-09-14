from palette.source import Source
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class PaletteMenus(Source):
    def __init__(self, *args, **kwargs):
        print(args)
        self._cached_menu = pd.DataFrame()
        super().__init__(*args, **kwargs)
        self.vim.subscribe("update_menu")

    @Source.name.getter
    def name(self):
        """ (temporary) rename to ease testing"""
        return "menus"

    def retrieve_menus(self, force=False):
        """
        TODO build a pandaframe along the way to optimizeEnabling networkmanager should be enough for VPN plugins to work
        TODO on update_menu notification reload menus
        """

        # self.nvim.command("let m = export_menus('', 'n')")
        # self.nvim.command("let r = json_encode(m)")
        # TODO ask for a fix should work without r
        # self.nvim.command("let g:r = 'toto'")
        # # m = self.nvim.vars["m"]
        # m = "test"
        # r = self.nvim.vars["r"]
        # entries = []
        entries = {}
        if not self.cached_menus.empty and force is False:
            return self.cached_menus

        returned_menus = self.vim.eval("menu_get('')")
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
                if entry.get("submenus"):
                    # if it's a top menu
                    subentries = build_entries(entry["submenus"])
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


    def serialize(self, match):
        menus = self.retrieve_menus()
        return menus.desc.tolist()

    def map2command(self, line):

        logger.debug("Looking for %s" % line)
        df = self.cached_menus[self.cached_menus.desc == line]
        if len(df) > 0:
            row = df.iloc[0, ]
            cmd = row['command']
            logger.info("Found command %s" % cmd)
            return cmd

    @property
    def cached_menus(self):
        return self._cached_menu

    @cached_menus.setter
    def cached_menus(self, val):
        self._cached_menu = val


