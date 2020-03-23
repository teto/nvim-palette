with import <nixpkgs> {};
let

  # 865
  compiler = pkgs.haskell.packages.ghc883;

  cabal2_nixpkgs = import ./pinned_nixpkgs.nix;
  pkgs = cabal2_nixpkgs.pkgs;
in
  compiler.callCabal2nix "nvim-palette" ./. {}
# haskell.lib.doHaddock (haskellPackages.callCabal2nix "nvim-palette" ./. {})
