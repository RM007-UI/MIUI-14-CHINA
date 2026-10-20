# Audit of the community Joyeuse MIUI 14 China archive

Audit date: 2026-10-20. Status: **archive metadata inspected; not authenticated or boot-tested**.

## Source listing claims

The public community post labels the package `MIUI 14.0.10.0.TLCCNXM - JOYEUSE ONLY`, Android 13, build date 2026-10-16, maintainer `kitagawa`. The same post reports missing Setup Wizard and NFC. Those bug notes are community-reported, not independently verified.

Source listing: https://t.me/s/Miatoll?q=%23a13

## Archive findings from GitHub Actions

- Downloaded archive size: **3,835,264,305 bytes**.
- SHA-256 of the downloaded ZIP: `8c877aa011baca33c0e8a63c5a559ae92351e89c65c777c3db24cbd33d6fdf86`.
- ZIP central directory: **14 entries**, **8,189,542,635 bytes** declared uncompressed total.
- `images/boot.img`: 134,217,728 bytes declared.
- `images/dtbo.img`: 1,049,813 bytes declared.
- `super.img`: 8,053,063,680 bytes declared uncompressed.
- The package includes an Android recovery installer script that writes `boot.img`, `dtbo.img`, and `super.img` to target partitions. The workflow did not execute this script or extract the images.

The SHA-256 identifies only this downloaded archive; it does not prove who built it or that its contents are safe.

## Important mismatch to investigate

The installer assertion accepts `curtana`, `joyeuse`, and the generic `miatoll` product string, despite the post describing the package as Joyeuse-only. Its printed target build string refers to `Redmi/miatoll_global/miatoll:12/.../V14.0.3.0.SJZMIXM`, which identifies an Android 12 Global MIUI base rather than the advertised Android 13 China build. This may be stale installer metadata, but it must not be silently assumed harmless.

The candidate Joyeuse device tree declares a 134,217,728-byte boot partition and an 8,589,934,592-byte super partition. The archive's declared boot image size exactly matches the tree's boot size, and its super image is smaller than the tree's declared super size. These are repository/package declarations, not measurements of the actual phone partition table; matching sizes alone do not prove compatibility.

## What remains unverified

- Archive publisher authenticity and signature trust.
- AVB/vbmeta consistency and internal image hashes.
- Actual partition layout on the target phone.
- Whether the image boots, and whether calls, mobile data, Wi-Fi, camera, audio, NFC, fingerprint, encryption, and recovery work.
- The reported Setup Wizard and NFC bugs.

## Decision

Treat this archive as a **research reference only**. Do not label it as our own build, do not republish the proprietary ROM, and do not treat the ZIP hash or installer assertions as a safety guarantee. The audit workflow uploads only a small text report and deletes the ROM archive from the temporary runner; it does not modify any phone.

Workflow run: https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39399582768
Audit workflow: https://github.com/RM007-UI/MIUI-14-CHINA/actions/workflows/audit-existing-joyeuse-port.yml
