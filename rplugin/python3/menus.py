from . import Source
import pandas as pd

logger = logging.getLogger('palette')


class PaletteMenus(Source):
    def init(self, vim):
        vim.subscribe("update_menu")
        self._cached_menu = pd.DataFrame()


    def retrieve_menus(self, force=False):
        """
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


    def serialize(self, match):
        menus = self.retrieve_menus()
        return menus.desc.tolist()

    def map2command(self, line):

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


