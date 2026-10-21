#!/usr/bin/env python3
"""Read-only audit of pinned Joyeuse source revisions; never builds or flashes."""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/joyeuse-a13-candidate.json"
OUT = ROOT / "source-audit-report.txt"
API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"

def get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "joyeuse-source-preflight",
    })
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read()

def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lines = [
        "Joyeuse Android 13 candidate source preflight",
        "Mode: read-only metadata inspection; no build and no device operations",
        "Target: joyeuse / SM6250 / MIUI 14 China port",
        "",
    ]
    ok = True
    for source in manifest["sources"]:
        name = source["name"]
        owner_repo = source["repository"].removesuffix(".git").split("github.com/")[-1]
        sha = source["commit"]
        lines.append(f"## {name}")
        lines.append(f"Repository: {owner_repo}")
        lines.append(f"Pinned commit: {sha}")
        try:
            commit = json.loads(get(f"{API}/repos/{owner_repo}/commits/{sha}"))
            actual = commit.get("sha", "")
            state = "PASS" if actual.lower() == sha.lower() else "FAIL"
            lines.append(f"GitHub commit API: {state} ({actual or 'no SHA returned'})")
            if state != "PASS":
                ok = False
        except Exception as exc:
            lines.append(f"GitHub commit API: ERROR ({type(exc).__name__}: {exc})")
            ok = False

        if name == "device_tree":
            paths = ["AndroidProducts.mk", "aosp_joyeuse.mk", "device.mk", "BoardConfig.mk", "proprietary-files.txt"]
            terms = ("aosp_joyeuse", "common_full_phone", "fingerprint", "V12.5.4.0.RJZIDXM",
                     "TARGET_ARCH", "TARGET_KERNEL_SOURCE", "BOARD_SUPER_PARTITION_SIZE",
                     "BOARD_USES_METADATA_PARTITION")
        elif name == "vendor":
            paths = ["joyeuse-vendor.mk", "Android.mk", "Android.bp"]
            terms = ("V12.5.4.0", "V13.", "ro.vendor.build.version", "joyeuse")
        else:
            paths = ["Makefile", "arch/arm64/configs/cust_defconfig"]
            terms = ("VERSION =", "PATCHLEVEL =", "SUBLEVEL =", "EXTRAVERSION =",
                     "LOCALVERSION", "QSSI", "LA.UM", "CONFIG_LOCALVERSION")

        for path in paths:
            url = f"{RAW}/{owner_repo}/{sha}/{path}"
            try:
                content = get(url).decode("utf-8", "replace")
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    continue
                lines.append(f"Read {path}: HTTP {exc.code}")
                continue
            except Exception as exc:
                lines.append(f"Read {path}: ERROR ({type(exc).__name__}: {exc})")
                continue
            hits = [(i, line.strip()) for i, line in enumerate(content.splitlines(), 1)
                    if any(term.lower() in line.lower() for term in terms)]
            if hits:
                lines.append(f"Markers in {path}:")
                for number, line in hits[:30]:
                    lines.append(f"  {number}: {line[:240]}")
        lines.append("")

    lines += [
        "Interpretation:",
        "- A passing commit check confirms source identity only, not compatibility.",
        "- The device tree is AOSP-derived; the vendor extraction origin and VINTF compatibility need review.",
        "- Kernel, boot image, vendor blobs, firmware, SELinux, and MIUI framework have not been built or boot-tested together.",
        "- Do not treat this report as ROM build approval or a flashable package.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if not ok:
        raise SystemExit("One or more pinned source commits could not be verified.")

if __name__ == "__main__":
    main()
