#!/usr/bin/env python3
"""Update uri#integrity hashes in a VCT definition document."""

import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True
    )
    return Path(result.stdout.strip())


def sri_hash(file_path: Path) -> str:
    digest = hashlib.sha256(file_path.read_bytes()).digest()
    return "sha256-" + base64.b64encode(digest).decode()


def uri_to_local(uri: str, root: Path):
    path = urlparse(uri).path.lstrip("/")
    local = root / path
    return local if local.exists() else None


def find_integrity_entries(obj, path="root"):
    """Yield (obj, key_prefix, json_path) for every uri#integrity found."""
    if isinstance(obj, dict):
        if "uri#integrity" in obj:
            yield obj, path
        for k, v in obj.items():
            yield from find_integrity_entries(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from find_integrity_entries(item, f"{path}[{i}]")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <vct-file.json>", file=sys.stderr)
        sys.exit(1)

    vct_file = Path(sys.argv[1])
    if not vct_file.exists():
        print(f"File not found: {vct_file}", file=sys.stderr)
        sys.exit(1)

    root = repo_root()
    data = json.loads(vct_file.read_text())

    mismatches = []

    for obj, json_path in find_integrity_entries(data):
        uri = obj.get("uri")
        stored = obj["uri#integrity"]

        if not uri:
            print(f"  WARNING: uri#integrity at {json_path} has no sibling 'uri' key — skipping")
            continue

        local = uri_to_local(uri, root)
        if local is None:
            print(f"  WARNING: no local file for {uri} — skipping")
            continue

        actual = sri_hash(local)
        if actual == stored:
            print(f"  OK  {uri}")
        else:
            print(f"  MISMATCH  {uri}")
            print(f"    stored: {stored}")
            print(f"    actual: {actual}")
            mismatches.append((obj, uri, stored, actual))

    if not mismatches:
        print("\nAll integrity hashes match.")
        return

    print(f"\n{len(mismatches)} mismatch(es) found.")
    answer = input("Update the document with correct hashes? [y/N] ").strip().lower()
    if answer != "y":
        print("No changes made.")
        sys.exit(1)

    for obj, uri, _old, actual in mismatches:
        obj["uri#integrity"] = actual

    vct_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Updated {vct_file}")


if __name__ == "__main__":
    main()
