#!/usr/bin/env python3
"""Generate signed SD-JWT VC (draft-ietf-oauth-sd-jwt-vc) example files for a schema version.

To add a new version (e.g. v4), add an entry to SCHEMAS below with its vct URL
and a flat list of (path, example_value) claims, then run:

    python3 scripts/generate_sdjwt_example.py v4

Each claim's path is a list of one or more keys. A one-element path is
selectively disclosed at the top level; a longer path is selectively
disclosed inside (nested, auto-created) container objects, mirroring how
Type Metadata addresses nested claims (see draft-ietf-oauth-sd-jwt-vc,
Section 5.6.1). Container objects themselves are always visible; only the
leaf claim is hidden behind a Disclosure.

Requires: pip install cryptography base58
"""

import base64
import hashlib
import json
import secrets
import subprocess
import sys
import time
from pathlib import Path

import base58
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ISSUER = "https://kela.pensiondemo.findy.fi"
HETU = "131052-308T"  # DVV-published test HETU, not a real person
EXP_SECONDS = 30 * 24 * 3600

SCHEMAS = {
    "v2": {
        "vct": "https://alennusperuste.todiste.fi/credentials/v2/PensionCredential",
        "claims": [
            (["Pension", "effectual"], True),
            (["Person", "personal_administrative_number"], HETU),
        ],
    },
    "v3": {
        "vct": "https://alennusperuste.todiste.fi/credentials/v3/PensionCredential",
        "claims": [
            (["Hetu"], HETU),
            (["Voimassa"], True),
            (["Muodostettu"], time.strftime("%Y-%m-%d")),
        ],
    },
}


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(result.stdout.strip())


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_json(obj) -> str:
    return b64url(json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode())


def digest(disclosure_b64: str) -> str:
    return b64url(hashlib.sha256(disclosure_b64.encode("ascii")).digest())


def make_disclosure(name, value) -> str:
    salt = b64url(secrets.token_bytes(16))
    return b64url_json([salt, name, value])


def add_claim(node: dict, path, value, disclosures: list):
    """Selectively disclose `value` at `path` inside `node`, creating
    intermediate (always-visible) container objects as needed."""
    if len(path) == 1:
        d = make_disclosure(path[0], value)
        disclosures.append(d)
        node.setdefault("_sd", []).append(digest(d))
    else:
        container = node.setdefault(path[0], {})
        add_claim(container, path[1:], value, disclosures)


def did_key_from_ed25519(pub_raw: bytes) -> str:
    # multicodec ed25519-pub (0xed01) + multibase base58btc ('z' prefix)
    return "did:key:z" + base58.b58encode(bytes([0xED, 0x01]) + pub_raw).decode()


def build(vct: str, claims, priv: Ed25519PrivateKey, kid: str, cnf_jwk: dict):
    now = int(time.time())
    payload = {
        "iss": ISSUER,
        "iat": now,
        "exp": now + EXP_SECONDS,
        "vct": vct,
        "cnf": {"jwk": cnf_jwk},
        "_sd_alg": "sha-256",
    }
    disclosures = []
    for path, value in claims:
        add_claim(payload, path, value, disclosures)

    header = {"typ": "dc+sd-jwt", "alg": "EdDSA", "kid": kid}
    signing_input = f"{b64url_json(header)}.{b64url_json(payload)}".encode()
    signature = priv.sign(signing_input)
    jwt = f"{signing_input.decode()}.{b64url(signature)}"

    # No Key Binding JWT: the trailing '~' after the last Disclosure is
    # required by SD-JWT to signal that explicitly.
    sd_jwt = jwt + "".join("~" + d for d in disclosures) + "~"
    return header, payload, sd_jwt


def main():
    versions = sys.argv[1:] or list(SCHEMAS)
    unknown = [v for v in versions if v not in SCHEMAS]
    if unknown:
        print(f"Unknown version(s): {', '.join(unknown)}. Known: {', '.join(SCHEMAS)}", file=sys.stderr)
        sys.exit(1)

    priv = Ed25519PrivateKey.generate()
    pub_raw = priv.public_key().public_bytes_raw()
    did = did_key_from_ed25519(pub_raw)
    kid = f"{did}#{did.rsplit(':', 1)[-1]}"
    cnf_jwk = {"kty": "OKP", "crv": "Ed25519", "x": b64url(pub_raw)}

    out_dir = repo_root() / "examples" / "sd-jwt-vc"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Issuer key (did:key): {did}\n")
    for version in versions:
        schema = SCHEMAS[version]
        header, payload, sd_jwt = build(schema["vct"], schema["claims"], priv, kid, cnf_jwk)

        jwt_path = out_dir / f"pensioncredential-{version}.jwt"
        payload_path = out_dir / f"pensioncredential-{version}-payload.json"
        jwt_path.write_text(sd_jwt)
        payload_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

        print(f"[{version}] wrote {jwt_path.relative_to(repo_root())}")
        print(f"[{version}] wrote {payload_path.relative_to(repo_root())}")
        print(f"[{version}] header: {header}\n")


if __name__ == "__main__":
    main()
