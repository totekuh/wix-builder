# wix-builder

Wraps an EXE or arbitrary command into an MSI installer using the WiX toolset. The payload executes automatically on install via a `CustomAction` with `asyncNoWait` after `InstallFinalize`.

All MSI metadata (product name, manufacturer, component IDs, file IDs, GUIDs, version) is randomized per build using plausible-sounding tech names, making each output unique.

## Requirements

- Python 3.10+
- Docker (uses `dactiv/wix` image)

## Install

```bash
pip install -e .
```

## Usage

EXE mode - wraps and runs an executable:

```bash
wix-builder -e payload.exe -o output.msi
```

Command mode - runs an arbitrary command (no EXE needed):

```bash
wix-builder -c 'powershell -nop -w hidden -enc BASE64STRING' -o output.msi
```

| Flag | Description | Default |
|------|-------------|---------|
| `-e` / `--exe` | Path to the EXE payload | one required |
| `-c` / `--cmd` | Command to execute on install | one required |
| `-o` / `--output` | Output MSI filename | `sample.msi` |

`-e` and `-c` are mutually exclusive.

## How it works

1. (EXE mode) Copies the EXE into a temp directory, or (CMD mode) skips this step
2. Renders a WiX `.wxs` manifest with randomized metadata
3. Runs `candle` (compile) and `light` (link) via dockerized WiX
4. Outputs the final `.msi`

In EXE mode, the MSI installs the EXE to `Program Files/<random name>/` and fires it via a Type 18 CustomAction. In CMD mode, a Type 34 CustomAction runs the command directly - no files are dropped.

## On target

```
msiexec /i output.msi /qn /norestart
```

| Flag | Description |
|------|-------------|
| `/i` | Install |
| `/qn` | Quiet, no UI (silent install) |
| `/norestart` | Suppress reboot prompts |
| `/l*v log.txt` | Verbose install log (for debugging) |

**Note:** If running as SYSTEM, the MSI must be on a local path (not a mapped network drive). Copy it to `C:\Windows\Temp\` first.

## Project structure

```
src/wix_builder/
  cli.py       - CLI entry point, docker build orchestration
  names.py     - random name/version generation from word lists
  template.py  - WXS XML template and rendering
```
