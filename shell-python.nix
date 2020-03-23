with import <nixpkgs> {};

let
  pyEnv = (pkgs.python36.withPackages (ps: [
  ps.jupyter_console ps.neovim ps.pandas ps.matplotlib ps.pyqt5]));
# pandas seems to depend on matplotlib ?
in
mkShell {
  name = "palette";
  buildInputs = [ pyEnv ];
}
