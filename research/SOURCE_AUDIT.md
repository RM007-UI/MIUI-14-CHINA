# Public source audit — MIUI 14 China `cupid` → `joyeuse`

Audit date: 2026-10-20
Status: metadata-only; no ROM package downloaded or unpacked.

## Confirmed source-package metadata

The XiaomiFirmwareUpdater public index lists `V14.0.10.0.TLCCNXM` as a **Xiaomi 12 China Stable Recovery** package based on Android `13.0`, approximately 5.6 GB, dated 2023-12-25. It also lists a separate Fastboot package at approximately 7.0 GB. These are distinct package formats and must not be treated as interchangeable.

Reference: https://github.com/XiaomiFirmwareUpdater/xiaomifirmwareupdater.github.io/blob/f3fd55eee00004d859cde590e446fabc4e93acc5/pages/miui/full/cupid.md

No package has been downloaded, verified by hash, or inspected in this project. The version metadata is confirmed from the index, but package authenticity and contents remain unverified here.

## Target device-tree inspection

Public tree: https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse

Observed facts from the tree's README and `BoardConfig.mk`:

- The README identifies `joyeuse` as Redmi Note 9 Pro with Qualcomm SM7125 / Snapdragon 720G and Adreno 618.
- `BoardConfig.mk` uses target platform `atoll` and points to kernel source `kernel/xiaomi/sm6250`.
- It contains target-specific audio, camera, Wi-Fi, init, partition, AVB, recovery and vendor configuration. These are examples of why the `cupid` device-specific components cannot simply be copied over.
- The repository's latest visible commit is dated 2022-10-21, and the tree describes itself as work in progress. It is historical reference material, not a verified Android 13 / MIUI 14 port base.
- The tree includes a declared vendor security patch level of 2021-10-01; that is another sign that this snapshot is old and cannot be adopted without a security and compatibility review.

## Engineering conclusion

This is a **high-risk cross-device port**: the source and target have different SoCs and vendor hardware stacks. The likely reusable part is the MIUI framework/system layer as a research target, not the source device's kernel, vendor image, firmware or partition layout. Even framework-level porting requires device-specific integration work and cannot be promised to boot.

## Next safe research steps

1. Find maintained Android 13-or-later `joyeuse` device tree, kernel and vendor repositories and verify branches/commits.
2. Record target Android/vendor API level and partition/boot configuration from public source metadata, without issuing commands to the user's phone.
3. Build a compatibility matrix and decide whether the existing target sources are adequate before attempting any compile.
4. Keep CI limited to static checks until a documented and reproducible build strategy exists. Do not generate flashable artifacts or run `adb`/`fastboot` in CI.

## Explicitly not done

- No ROM images or firmware were downloaded.
- No proprietary blobs were copied.
- No ROM was built or packaged.
- No commands were sent to the phone.
- No claim is made that an installable or bootable port exists.
