{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in rec {
      devShell = pkgs.mkShell {
        nativeBuildInputs = [ pkgs.bashInteractive ];
        buildInputs = [ 
          pkgs.python310 
          pkgs.python310Packages.urwid 
          pkgs.python310Packages.cryptography
        ];
      };
      packages.dml = 
      let python = 
        pkgs.python310.withPackages (
          pyPkgs: [
            pyPkgs.urwid
            pyPkgs.cryptography
          ]
        );
      in
        pkgs.stdenv.mkDerivation rec {
          name = "dml-${version}";
          version = "0.0.4";
          src = builtins.path { name = "dml"; path = ./.; };
          installPhase = ''
            mkdir -p $out/dml;
            cp -r . $out/dml
            mkdir -p $out/bin;
            dd status=none of=$out/bin/dml << EOF
            #!/bin/bash
            ${python}/bin/python $out/dml/main.py \$*
            EOF
            chmod +x $out/bin/dml
          '';
        };
      packages.default = packages.dml;
    });
}
