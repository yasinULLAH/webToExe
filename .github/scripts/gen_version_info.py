#!/usr/bin/env python3
"""Generate a PyInstaller VSVersionInfo resource file from app.py's APP_VERSION.

Usage:
    python .github/scripts/gen_version_info.py [app.py] [version_info.txt]

The produced file is passed to PyInstaller via --version-file so the compiled
executable shows proper Company / Product / Version / Copyright metadata in
Windows File Properties and Task Manager.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

COMPANY = "Bannu Software Solutions"
PRODUCT = "KioskForge Pro"
DESCRIPTION = "Enterprise Client Web App & Portable EXE Builder"
INTERNAL_NAME = "KioskForgePro"
COPYRIGHT = "Copyright (c) Bannu Software Solutions"

VERSION_PATTERN = re.compile(r'APP_VERSION\s*=\s*"([0-9]+(?:\.[0-9]+)*)"')


def parse_version(source: Path) -> tuple[int, int, int, int]:
    text = source.read_text(encoding="utf-8")
    match = VERSION_PATTERN.search(text)
    if not match:
        raise SystemExit(f"ERROR: could not find APP_VERSION in {source}")

    parts = [int(part) for part in match.group(1).split(".")][:4]
    while len(parts) < 4:
        parts.append(0)
    return parts[0], parts[1], parts[2], parts[3]


def build_resource(version: tuple[int, int, int, int]) -> str:
    version_tuple = f"({version[0]}, {version[1]}, {version[2]}, {version[3]})"
    version_string = ".".join(str(part) for part in version)

    return f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'{COMPANY}'),
            StringStruct(u'FileDescription', u'{DESCRIPTION}'),
            StringStruct(u'FileVersion', u'{version_string}'),
            StringStruct(u'InternalName', u'{INTERNAL_NAME}'),
            StringStruct(u'LegalCopyright', u'{COPYRIGHT}'),
            StringStruct(u'OriginalFilename', u'{INTERNAL_NAME}.exe'),
            StringStruct(u'ProductName', u'{PRODUCT}'),
            StringStruct(u'ProductVersion', u'{version_string}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""


def main() -> int:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "app.py")
    output = Path(sys.argv[2] if len(sys.argv) > 2 else "version_info.txt")

    if not source.is_file():
        print(f"ERROR: {source} not found", file=sys.stderr)
        return 1

    version = parse_version(source)
    output.write_text(build_resource(version), encoding="utf-8")
    print(f"Wrote {output} for version {'.'.join(str(part) for part in version)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
