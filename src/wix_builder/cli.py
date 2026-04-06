#!/usr/bin/env python3

import shutil
import subprocess
import tempfile
from argparse import ArgumentParser
from pathlib import Path

from .template import render_wxs, render_wxs_cmd

DOCKER_IMAGE = "dactiv/wix"


def run(cmd, **kwargs):
    print(f"> {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def _compile_msi(tmp: Path, output: Path):
    run([
        "docker", "run", "--rm",
        "-v", f"{tmp}:/wix",
        DOCKER_IMAGE,
        "candle", "sample.wxs",
    ])

    run([
        "docker", "run", "--rm",
        "-v", f"{tmp}:/wix",
        DOCKER_IMAGE,
        "light", "sample.wixobj", "-sval",
    ])

    built = tmp / "sample.msi"
    if not built.exists():
        raise SystemExit("[-] Build failed; sample.msi not produced")

    output_path = Path.cwd() / output
    shutil.copy2(built, output_path)
    print(f"[+] Built MSI: {output_path}")


def build_msi(exe_path: Path, output: Path):
    exe_path = exe_path.resolve()
    if not exe_path.is_file():
        raise SystemExit(f"[-] Executable not found: {exe_path}")

    with tempfile.TemporaryDirectory(prefix="wixbuild_") as tmpdir:
        tmp = Path(tmpdir)
        shutil.copy2(exe_path, tmp / exe_path.name)

        wxs_content = render_wxs(exe_name=exe_path.name)
        (tmp / "sample.wxs").write_text(wxs_content, encoding="utf-8")

        _compile_msi(tmp, output)


def build_msi_cmd(command: str, output: Path):
    with tempfile.TemporaryDirectory(prefix="wixbuild_") as tmpdir:
        tmp = Path(tmpdir)

        wxs_content = render_wxs_cmd(command=command)
        (tmp / "sample.wxs").write_text(wxs_content, encoding="utf-8")

        _compile_msi(tmp, output)


def main():
    parser = ArgumentParser(description="WiX MSI payload builder with randomized metadata")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--exe", help="Path to the EXE payload")
    group.add_argument("-c", "--cmd", help="Command to execute on install")
    parser.add_argument("-o", "--output", default="sample.msi", help="Output MSI filename (default: sample.msi)")
    args = parser.parse_args()

    if args.exe:
        build_msi(Path(args.exe), Path(args.output))
    else:
        build_msi_cmd(args.cmd, Path(args.output))


if __name__ == "__main__":
    main()
