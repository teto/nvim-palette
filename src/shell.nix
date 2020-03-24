with import <nixpkgs> {};

let
  # todo make it automatic depending on nixpkgs' ghc
  # hie = (import hie_remote {} ).hie86;
  a = 3;

in
haskellPackages.shellFor {
  # the dependencies of packages listed in `packages`, not the
  packages = p: with p; [
    (import ../. )
  ];
  withHoogle = true;
  # haskellPackages.stack 
  nativeBuildInputs = [
    hie
    haskellPackages.cabal-install
    # haskellPackages.bytestring-conversion
    haskellPackages.gutenhasktags
    haskellPackages.haskdogs # seems to build on hasktags/ recursively import things
    haskellPackages.hasktags

    # for https://hackage.haskell.org/package/bytestring-conversion-0.2/candidate/docs/Data-ByteString-Conversion-From.html
  ];

  # export HIE_HOOGLE_DATABASE=$NIX_GHC_DOCDIR as DOCDIR doesn't exist it won't work
  shellHook = ''
    # check if it's still needed ?
    export HIE_HOOGLE_DATABASE="$NIX_GHC_LIBDIR/../../share/doc/hoogle/index.html"
    # export runghc=" "
  '';
}
