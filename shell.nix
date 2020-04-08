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
  local_nixpkgs = import <nixpkgs> {};
  # palette
  my_nvim = local_nixpkgs.genNeovim  [ ] {
    withHaskell = true;

    neovimRC = ''
      " commentaire par matt

      " draw a line on 80th column
      set colorcolumn+=30
    '';
  };

  # all-hies = import (fetchTarball "https://github.com/infinisil/all-hies/tarball/master") {};
  # attempt to fix libc compat
  all-hies = import (fetchTarball "https://github.com/teto/all-hies/tarball/test") {};

  # hercules-ci is a fork of cachix
  ghcide-nix = import (builtins.fetchTarball "https://github.com/cachix/ghcide-nix/tarball/master") {};

  # https://discourse.nixos.org/t/how-to-override-a-haskell-package-in-shell-nix/2907
  my_haskellPackages = nixpkgs.dontRecurseIntoAttrs( local_nixpkgs.haskell.packages."${compilerName}".extend (
    hself: hold: with local_nixpkgs.haskell.lib; rec {
      # useful to fetch newer libraries with callHackage
      # gutenhasktags = dontCheck (hprev.callPackage ./pkgs/gutenhasktags {});

      # for newer nixpkgs (March 2020)
      # base-compat = doJailbreak (hold.base-compat);
      # time-compat = doJailbreak (hold.time-compat);

      # msgpack = doJailbreak (hold.msgpack);
  }));


in
# compiler.shellFor {
# packages = p: with p; [ # (import ./. { inherit compiler;}) palette ] ++ [ ] ;
# withHoogle = true;
# nativeBuildInputs = with pkgs; [

(palette.envFunc { withHoogle = true; }).overrideAttrs (oa: {
  # the dependencies of packages listed in `packages`, not the

  nativeBuildInputs = oa.nativeBuildInputs ++ ([
    # all-hies.versions."${compilerName}"
    # my_nvim

    # or ghcide
    ghcide-nix."ghcide-${compilerName}"

    my_haskellPackages.hasktags
    my_haskellPackages.nvim-hs
    my_haskellPackages.nvim-hs-ghcid # too old, won't support nvim-hs-contrib 2
    my_haskellPackages.cabal-install

    # haskellPackages.gutenhasktags  # taken from my overlay
    # haskellPackages.haskdogs # seems to build on hasktags/ recursively import things
  ]);

  propagatedBuildInputs = [];

  shellHook = ''
    # check if it's still needed ?
    export HIE_HOOGLE_DATABASE="$NIX_GHC_LIBDIR/../../share/doc/hoogle/index.html"

    echo "cabal clean"
    echo "cabal configure --extra-include-dirs=/home/teto/mptcp/build/usr/include -v3"
  '';

})
