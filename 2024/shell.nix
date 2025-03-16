{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    # stdenv.cc.libc.dev # Provides standard C headers (e.g., stdbool.h)
    # rustc # Rust compiler
    # cargo # Cargo build tool
    llvmPackages.clang-unwrapped.lib # libclang.so for bindgen
    # z3.dev # Z3 headers (e.g., z3.h)
    # llvmPackages.clang-unwrapped # Clang binary for bindgen
  ];
  LIBCLANG_PATH = "${pkgs.llvmPackages.clang-unwrapped.lib}/lib"; # Path to libclang.so
  # shellHook = ''
  #   export Z3_SYS_Z3_HEADER="${pkgs.z3.dev}/include/z3.h"  # Path to z3.h
  # '';
}
