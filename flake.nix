{
  description = "Character Identify";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          git
          python312
          python312Packages.pip
          python312Packages.setuptools
          python312Packages.pygobject3
          gtk3
          uv
        ];

        shellHook = ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
            pkgs.libxcb
            pkgs.libGL
            pkgs.glib
            
            pkgs.libX11
            pkgs.libXext
            pkgs.libSM
            pkgs.libICE
            
            pkgs.pipewire
          ]}:$LD_LIBRARY_PATH"
        '';
      };
    };
}
