# Audit of the community Joyeuse MIUI 14 China archive

Audit date: 2026-10-20. Status: **archive and selected image metadata inspected; not authenticated or boot-tested**.

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
- The package includes an Android recovery installer script that writes `boot.img`, `dtbo.img`, and `super.img` directly to target partitions. Its embedded `META-INF/com/android/metadata` explicitly declares `pre-device=joyeuse` but also declares `post-build=Redmi/joyeuse_global/joyeuse:12/.../V14.0.3.0.SJZMIXM`, `post-sdk-level=31`, and the February 2023 security patch. Those are Android 12 Global base-package fields, but the later direct inspection of the `system` filesystem confirms that the actual system partition declares Android 13. The workflow did not execute the installer script or flash any image.

The SHA-256 identifies only this downloaded archive; it does not prove who built it or that its contents are safe. ZIP entries also contain timestamps dated 2026-10-26, later than this audit date (2026-10-20). ZIP timestamps can be wrong, so this is an anomaly to record, not proof of tampering.

## Important mismatch to investigate

The installer assertion accepts `curtana`, `joyeuse`, and the generic `miatoll` product string, despite the post describing the package as Joyeuse-only. Its printed target build string also refers to `Redmi/miatoll_global/miatoll:12/.../V14.0.3.0.SJZMIXM`. The embedded OTA metadata independently confirms SDK 31 (Android 12) and the Joyeuse Global `V14.0.3.0.SJZMIXM` base. The stale metadata is now explained in part: the actual `system` filesystem reports Android 13 China build `V14.0.10.0.TLCCNXM`, while the separate boot image still carries an Android 12 Global build marker. That cross-image mismatch remains a compatibility concern.

The candidate Joyeuse device tree declares a 134,217,728-byte boot partition and an 8,589,934,592-byte super partition. The archive's declared boot image size exactly matches the tree's boot size, and its super image is smaller than the tree's declared super size. These are repository/package declarations, not measurements of the actual phone partition table; matching sizes alone do not prove compatibility.

## What remains unverified

- Archive publisher authenticity and signature trust.
- AVB/vbmeta consistency and internal image hashes.
- Actual partition layout on the target phone.
- Whether the image boots, and whether calls, mobile data, Wi-Fi, camera, audio, NFC, fingerprint, encryption, and recovery work.
- The reported Setup Wizard and NFC bugs.
- Whether the `vendor`, `system_ext`, and `product` partitions match the Android 13 system and Joyeuse firmware expectations; vendor property inspection is the next check.

## Decision

Treat this archive as a **research reference only**. Do not label it as our own build, do not republish the proprietary ROM, and do not treat the ZIP hash or installer assertions as a safety guarantee. The audit workflow temporarily extracts the boot image and mapped system logical partition for read-only metadata inspection, deletes both temporary images and the archive, and uploads only a small text report. It does not modify any phone.

Workflow run: https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39399582768
Audit workflow: https://github.com/RM007-UI/MIUI-14-CHINA/actions/workflows/audit-existing-joyeuse-port.yml

## Super image metadata inspection (GitHub Actions run 6)

The next read-only inspection of the same archive confirmed:

- `super.img` is a raw (not Android-sparse) logical-partition image.
- Both liblp geometry copies were found at byte offsets 4096 and 8192; both 52-byte geometry checksums validate.
- Geometry declares a 65,536-byte metadata area, two metadata slots, and a 4,096-byte logical block size.
- Metadata slot 0 has LP metadata version 10.0; both its header and table SHA-256 checksums validate.
- The logical partition table contains four partitions: `system` (1,529,434,112 bytes), `system_ext` (758,718,464 bytes), `vendor` (1,391,788,032 bytes), and `product` (3,914,190,848 bytes).
- The dynamic group is `qti_dynamic_partitions`; its declared maximum is 8,053,063,680 bytes. The image's sole block device is named `super` and also declares 8,053,063,680 bytes.

These checks validate the container's internal logical-partition metadata; they do **not** validate that it is safe for a particular phone, prove the Android version, or prove successful boot. The next workflow revision temporarily extracts only the mapped `system` logical partition to inspect build properties, then removes it; only the text report is retained.

Run 6: https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39566884259

## Actual system identity from the logical partition (GitHub Actions run 8)

The workflow validated both liblp geometry checksums and the metadata header/table checksums, then temporarily extracted the mapped `system` logical partition to a temporary file. The file was identified as an ext filesystem; read-only `debugfs` inspection of `/system/build.prop` found:

- `ro.build.version.release=13`
- `ro.build.version.sdk=33`
- `ro.build.version.incremental=V14.0.10.0.TLCCNXM`
- `ro.build.version.security_patch=2023-11-01`

This independently supports that the **system partition itself is Android 13 China build V14.0.10.0.TLCCNXM**, despite stale Android 12 Global metadata in the recovery package and boot image. The system image was removed after inspection; it is not included in the artifact.

Run 8: https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39567162112

The next revision will inspect vendor build properties to assess whether the vendor stack agrees with this Android 13 system.
