#!/usr/bin/env python3
"""Read-only audit of pinned Joyeuse source revisions; never builds or flashes."""
import json
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
        "Mode: read-only metadata and source inventory; no build and no device operations",
        "Target: joyeuse / SM6250 / MIUI 14 China port",
        "",
    ]
    ok = True
    for source in manifest["sources"]:
        name = source["name"]
        owner_repo = source["repository"].removesuffix(".git").split("github.com/")[-1]
        sha = source["commit"]
        lines.extend([f"## {name}", f"Repository: {owner_repo}", f"Pinned commit: {sha}"])
        try:
            commit = json.loads(get(f"{API}/repos/{owner_repo}/commits/{sha}"))
            actual = commit.get("sha", "")
            state = "PASS" if actual.lower() == sha.lower() else "FAIL"
            lines.append(f"GitHub commit API: {state} ({actual or 'no SHA returned'})")
            if state != "PASS":
                ok = False
        except Exception as exc:
            lines.append(f"GitHub commit API: ERROR ({type(exc).__name__}: {exc})")
            lines.append("")
            ok = False
            continue

        try:
            tree = json.loads(get(f"{API}/repos/{owner_repo}/git/trees/{sha}?recursive=1"))
            entries = tree.get("tree", [])
            lines.append(f"Tracked tree entries: {len(entries)}; recursive response truncated: {tree.get('truncated', False)}")
            if tree.get("truncated"):
                lines.append("WARNING: GitHub returned a truncated tree; inventory below is partial.")
        except Exception as exc:
            entries = []
            lines.append(f"Tree inventory: ERROR ({type(exc).__name__}: {exc})")

        if name == "device_tree":
            exact_paths = ["AndroidProducts.mk", "aosp_joyeuse.mk", "device.mk", "BoardConfig.mk", "proprietary-files.txt"]
            terms = ("aosp_joyeuse", "common_full_phone", "fingerprint", "V12.5.4.0.RJZIDXM",
                     "TARGET_ARCH", "TARGET_KERNEL_SOURCE", "BOARD_SUPER_PARTITION_SIZE",
                     "BOARD_USES_METADATA_PARTITION", "BOARD_BOOT_HEADER_VERSION",
                     "BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE", "BOARD_AVB")
            inventory_patterns = ("fstab", "manifest", "compatibility_matrix", "sepolicy", "init", "modules")
        elif name == "vendor":
            exact_paths = ["joyeuse-vendor.mk", "Android.mk", "Android.bp", "BoardConfigVendor.mk"]
            terms = ("V12.5.4.0", "V13.", "ro.vendor.build.version", "joyeuse")
            inventory_patterns = ("manifest", "compatibility_matrix", "sepolicy", "fstab", "modules", "proprietary")
        else:
            exact_paths = ["Makefile", "arch/arm64/configs/cust_defconfig"]
            terms = ("VERSION =", "PATCHLEVEL =", "SUBLEVEL =", "EXTRAVERSION =",
                     "LOCALVERSION", "QSSI", "LA.UM", "CONFIG_LOCALVERSION",
                     "CONFIG_MODULES", "CONFIG_MODVERSIONS")
            inventory_patterns = ("joyeuse", "sm6250", "cust_defconfig", "module")

        selected = []
        for entry in entries:
            if entry.get("type") != "blob":
                continue
            path = entry.get("path", "")
            lower = path.lower()
            if any(pattern in lower for pattern in inventory_patterns):
                selected.append(path)
        lines.append(f"Relevant tracked paths ({min(len(selected), 100)} shown of {len(selected)} found):")
        lines.extend(f"  - {path}" for path in selected[:100])

        # Read key configuration files and print only compatibility-relevant markers.
        paths = list(dict.fromkeys(exact_paths + selected[:30]))
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
                for number, line in hits[:25]:
                    lines.append(f"  {number}: {line[:220]}")
        lines.append("")

    lines += [
        "Interpretation:",
        "- A passing commit check confirms source identity only, not compatibility.",
        "- Inventory is a source-only aid; a path or marker does not validate the contents of proprietary binaries.",
        "- Device tree, vendor blobs, VINTF, sepolicy, fstab, kernel modules, boot image, firmware, and MIUI framework still require a joined compatibility review.",
        "- Do not treat this report as ROM build approval or a flashable package.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if not ok:
        raise SystemExit("One or more pinned source commits could not be verified.")

if __name__ == "__main__":
    main()
