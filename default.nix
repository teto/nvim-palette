with import <nixpkgs> {};

haskell.lib.doHaddock (haskellPackages.callCabal2nix "nvim-palette" ./. {})

