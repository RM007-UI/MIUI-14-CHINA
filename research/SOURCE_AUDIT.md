# Public source audit — MIUI 14 China `cupid` → `joyeuse`

Audit date: 2026-10-20
Status: metadata-only; no ROM package downloaded or unpacked.

## Confirmed source-package metadata

The XiaomiFirmwareUpdater public index lists `V14.0.10.0.TLCCNXM` as a **Xiaomi 12 China Stable Recovery** package based on Android `13.0`, approximately 5.6 GB, dated 2023-12-25. It also lists a separate Fastboot package at approximately 7.0 GB. These are distinct package formats and must not be treated as interchangeable.

Reference: https://github.com/XiaomiFirmwareUpdater/xiaomifirmwareupdater.github.io/blob/f3fd55eee00004d859cde590e446fabc4e93acc5/pages/miui/full/cupid.md

No package has been downloaded, verified by hash, or inspected in this project. The version metadata is confirmed from the index, but package authenticity and contents remain unverified here.

## Target device-tree inspection

Historical public tree: https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse

Observed facts from the tree's README and `BoardConfig.mk`:

- The README identifies `joyeuse` as Redmi Note 9 Pro with Qualcomm SM7125 / Snapdragon 720G and Adreno 618.
- `BoardConfig.mk` uses target platform `atoll` and points to kernel source `kernel/xiaomi/sm6250`.
- It contains target-specific audio, camera, Wi-Fi, init, partition, AVB, recovery and vendor configuration. These are examples of why the `cupid` device-specific components cannot simply be copied over.
- Its latest visible commit is dated 2022-10-21, and the tree describes itself as work in progress. It is historical reference material, not a verified Android 13 / MIUI 14 port base.
- The tree includes a declared vendor security patch level of 2021-10-01; this snapshot is old and cannot be adopted without a security and compatibility review.

## Newer public source candidates checked on 2026-10-20

These candidates were checked through public GitHub repository metadata and recent commit history. A recent commit is evidence of activity, **not proof that the repository builds or is compatible with MIUI 14**.

| Component | Candidate | Observed evidence | Assessment |
|---|---|---|---|
| Device tree (Android 13 branch) | https://github.com/nekoshirro/device_xiaomi_joyeuse/tree/13-FBEv1 | Branch `13-FBEv1`; latest observed commit 2023-08-28; `BoardConfig.mk` declares device `joyeuse`, boot header v2, dynamic partitions and kernel source path `kernel/xiaomi/sm6250` | Relevant Android 13-era candidate with device-specific configuration. The source tree is not a MIUI port and still needs build-context and dependency verification. |
| Vendor blobs (Android 13 branch) | https://github.com/nekoshirro/vendor_xiaomi_joyeuse/tree/13 | Branch `13`; latest observed commit 2023-08-28; target-specific vendor blob makefiles | Version label aligns with the Android 13 device-tree branch, but alignment of branch labels alone does not prove complete compatibility. |
| Kernel | https://github.com/jandaX/android_kernel_xiaomi_joyeuse/tree/Tanya | Repository description says “A13 kernel”; default branch `Tanya`; latest observed commit on this branch 2023-05-18; includes `joyeuse_defconfig` | Candidate kernel is Android 13-era, but the device tree branch specifies `cust_defconfig`, which was not found at `arch/arm64/configs/cust_defconfig` in this kernel branch. A follow-up scan of all six visible branches (`404`, `Siska`, `Tanya`, `Titaniya`, `Ulan`, `prebuild`) found `joyeuse_defconfig` and `stock_defconfig`, but no `cust_defconfig`. This confirms the mismatch across the checked branches; do not silently substitute a config without validating the intended kernel/device-tree pairing. |
| Newer default branches | https://github.com/nekoshirro/device_xiaomi_joyeuse/tree/16-los and https://github.com/nekoshirro/vendor_xiaomi_joyeuse/tree/16 | Recent commits observed in December 2025; branches target a newer Android generation | Useful as a future reference, not directly interchangeable with the Android 13 source ROM. |
| Older device/vendor snapshot | https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse and https://github.com/AOSP-joyeuse/platform_vendor_xiaomi_joyeuse | Last observed commits in October 2022 | Useful as historical reference only; not a modern base.
| Older device/vendor snapshot | https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse and https://github.com/AOSP-joyeuse/platform_vendor_xiaomi_joyeuse | Last observed commits in October 2022 | Useful as historical reference only; not a modern base. |

The newer device and vendor candidates are at:
- Device tree: https://github.com/nekoshirro/device_xiaomi_joyeuse
- Vendor blobs: https://github.com/nekoshirro/vendor_xiaomi_joyeuse
- Android 13-labelled kernel candidate: https://github.com/jandaX/android_kernel_xiaomi_joyeuse

No repositories were cloned, compiled, or integrated. Branch labels and commit dates are preliminary screening signals only.

## Engineering conclusion

This is a **high-risk cross-device port**: the source and target have different SoCs and vendor hardware stacks. The likely reusable part is the MIUI framework/system layer as a research target, not the source device's kernel, vendor image, firmware or partition layout. Even framework-level porting requires device-specific integration work and cannot be promised to boot.

The recent `joyeuse` device/vendor trees provide a better lead for further source inspection, but their default branches target a much newer Android generation than the Android 13 source ROM. The older Android 13-labelled kernel is not, by itself, enough to establish a coherent buildable stack. We still need to identify mutually compatible branches and verify the build configuration.

## Next safe research steps

1. Resolve the Android 13 kernel-config mismatch: public branch scan of the six visible branches in `jandaX/android_kernel_xiaomi_joyeuse` found no `cust_defconfig`. Identify the intended kernel repository/branch from the device-tree history or a matching build manifest; do not simply rename or substitute the config.
2. Inspect Android 13 device-tree and vendor dependencies, proprietary blob baseline and compatibility-matrix declarations.
3. Compare the source ROM's Android 13 framework/vendor interfaces against the selected target device/vendor baseline; do not assume the Xiaomi 12's proprietary components are reusable.
4. Record target partition/boot configuration from public source metadata, without issuing commands to the user's phone.
5. Keep CI limited to static checks until a documented and reproducible build strategy exists. Do not generate flashable artifacts or run `adb`/`fastboot` in CI.

## Explicitly not done

- No ROM images or firmware were downloaded.
- No proprietary blobs were copied.
- No ROM was built or packaged.
- No commands were sent to the phone.
- No claim is made that an installable or bootable port exists.
