let
  overlay = self: prev: {
      haskell = prev.haskell // {
        packageOverrides = hnew: hold: with prev.haskell.lib;{

          # from nixpkgs-stackage overlay
          # ip = pkgs.haskell.lib.dontCheck hold.ip;
          # all-hies = import (fetchTarball "https://github.com/infinisil/all-hies/tarball/master") {};

          # for newer nixpkgs (March 2020)
          base-compat = doJailbreak (hold.base-compat);
          time-compat = doJailbreak (hold.time-compat);

          # msgpack = doJailbreak (hold.msgpack);

        };
      };
  };

  # pinned nixpkgs before cabal 3 becomes the default else hie fails
  nixpkgs = import <nixpkgs>

  # nixpkgs = import (builtins.fetchTarball {
  #     name = "toto";
  #     url = "https://github.com/nixos/nixpkgs/archive/3320a06049fc259e87a2bd98f4cd42f15f746b96.tar.gz";
  #     sha256 = "1g5l186d5xh187vdcpfsz1ff8s749949c1pclvzfkylpar09ldkl";
  # })
  {
    # overlays = [overlay];
    # config = {allowBroken = true;}; 
  };
in
  nixpkgs
