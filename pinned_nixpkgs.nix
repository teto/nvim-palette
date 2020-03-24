let
  overlay = self: prev: {
      haskell = prev.haskell // {
        packageOverrides = hnew: hold: with prev.haskell.lib;{

          # from nixpkgs-stackage overlay
          # ip = pkgs.haskell.lib.dontCheck hold.ip;
          all-hies = import (fetchTarball "https://github.com/infinisil/all-hies/tarball/master") {};

          # for newer nixpkgs (March 2020)
          base-compat = doJailbreak (hold.base-compat);
          time-compat = doJailbreak (hold.time-compat);
        };
      };
  };

  # pinned nixpkgs before cabal 3 becomes the default else hie fails
  nixpkgs = import <nixpkgs>
  # nixpkgs = import (builtins.fetchTarball {
  #     name = "before-libc-update";
  #     url = "https://github.com/nixos/nixpkgs/archive/fa7445532900f2555435076c1e7dce0684daa01a.tar.gz";
  #     sha256 = "1hbf7kmbxmd19hj3kz9lglnyi4g20jjychmlhcz4bx1limfv3c3r";
  # })
  {
    overlays = [overlay];
    # config = {allowBroken = true;}; 
  };
in
  nixpkgs
