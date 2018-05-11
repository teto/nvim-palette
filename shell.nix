with import <nixpkgs> {};

# pandas seems to depend on matplotlib ?
(pkgs.python36.withPackages (ps: [ps.jupyter_console ps.neovim ps.pandas ps.matplotlib ps.pyqt5])).env
