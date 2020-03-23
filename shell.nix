# from https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/haskell.section.md
{

  nixpkgs ? import ./pinned_nixpkgs.nix
  # nixpkgs ? import <nixpkgs> {}
  , compilerName ? "ghc865"
  # , compilerName ? "ghc883"
}:

let
  compiler = pkgs.haskell.packages."${compilerName}";
  pkgs = nixpkgs.pkgs;

  palette = (import ./. );

  # genNeovim comes from overlay, not uploaded yet
  my_nvim = nixpkgs.genNeovim  [ palette ] {
    withHaskell = true;

    neovimRC = ''
      " commentaire par matt

      " draw a line on 80th column
      set colorcolumn+=30
    '';
  };

  all-hies = import (fetchTarball "https://github.com/infinisil/all-hies/tarball/master") {};

  # hercules-ci is a fork of cachix
  ghcide-nix = import (builtins.fetchTarball "https://github.com/cachix/ghcide-nix/tarball/master") {};

  # { inherit compiler;}
  my_pkg = (import ./. );

in
# compiler.shellFor {
# packages = p: with p; [ # (import ./. { inherit compiler;}) palette ] ++ [ ] ;
# withHoogle = true;
# nativeBuildInputs = with pkgs; [

(my_pkg.envFunc { withHoogle = true; }).overrideAttrs (oa: {
  # the dependencies of packages listed in `packages`, not the

    nativeBuildInputs = oa.nativeBuildInputs ++ (with pkgs; [
    # all-hies.versions."${compilerName}"

    # or ghcide
    ghcide-nix."ghcide-${compilerName}"

    haskellPackages.hasktags
    haskellPackages.nvim-hs
    haskellPackages.nvim-hs-ghcid # too old, won't support nvim-hs-contrib 2
    haskellPackages.cabal-install

    # haskellPackages.gutenhasktags  # taken from my overlay
    # haskellPackages.haskdogs # seems to build on hasktags/ recursively import things
  ]);

  shellHook = ''
    # check if it's still needed ?
    export HIE_HOOGLE_DATABASE="$NIX_GHC_LIBDIR/../../share/doc/hoogle/index.html"

    echo "cabal clean"
    echo "cabal configure --extra-include-dirs=/home/teto/mptcp/build/usr/include -v3"
  '';

})
