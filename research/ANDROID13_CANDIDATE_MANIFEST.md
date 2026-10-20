# Android 13 Joyeuse candidate manifest (research only)

Status: **candidate inventory, not a build-ready manifest**.

This file pins the exact revisions currently under consideration so branches are not silently mixed. The listed revisions have not been proven to build together. Do not use this list as a `repo init` manifest or as a recipe to produce a flashable ROM.

## Candidate revisions

| Component | Repository | Branch | Candidate revision | What is verified | What remains unverified |
|---|---|---|---|---|---|
| Joyeuse device tree | https://github.com/nekoshirro/device_xiaomi_joyeuse | `13-FBEv1` | `7bedf8a993c58b7743aebd49dfc5e3a7bfa9242f` | Android 13-era AOSP product files; kernel source path `kernel/xiaomi/sm6250`; `cust_defconfig`; clang label `alchemist` | Exact source manifest, build host/toolchain availability, matching common trees and runtime validation |
| Joyeuse vendor blobs | https://github.com/nekoshirro/vendor_xiaomi_joyeuse | `13` | `ad53e0661749e8f697d9ed3bcd2f9aa47b82cc29` | Generated vendor build definitions and proprietary blobs exist | Exact firmware extraction baseline, pairing with the exact device tree/kernel, redistribution rights |
| SM6250 kernel | https://github.com/ArrowOS-Devices/android_kernel_xiaomi_sm6250 | `arrow-13.0` | `a8dc7bc9a34a090eccfc4d8d5c53c694d0f85186` | Kernel 4.14.304; `arch/arm64/configs/cust_defconfig` exists | Proven pairing with the device tree/vendor snapshot; exact `alchemist` toolchain compatibility; forced module-signature key compatibility |
| MIUI source framework | Xiaomi 12 `cupid`, `V14.0.10.0.TLCCNXM` | China stable | Source package identified in public index, not downloaded or hash-verified | Android 13 MIUI 14 package is listed | Cross-device framework/HAL/VINTF/SELinux integration and lawful blob handling |

## Hard blockers before a ROM build

1. Obtain a pinned manifest or reliable build record proving the exact device, common, vendor, kernel, firmware, and build-system revisions were used together.
2. Verify the named clang toolchain is present and compatible with the selected kernel source and device-tree build flags.
3. Audit kernel module signing: the candidate config sets `CONFIG_MODULE_SIG_FORCE=y`; external modules must be signed by a key accepted by the kernel.
4. Reconcile device/vendor VINTF declarations, HAL versions, SELinux policy, permissions, partition layout, boot image parameters, and firmware baseline.
5. Establish how proprietary blobs may be used and distributed; do not publish an image containing blobs without appropriate permission.
6. Only then attempt a non-flashing, isolated source build and inspect build logs and output metadata. A successful compile would still not prove that the ROM boots or that hardware works.

## Important distinction

The product defined by `13-FBEv1` is AOSP-derived (`aosp_joyeuse`), not MIUI. The Xiaomi 12 framework is a different device's framework. These candidates are useful for engineering research only; there is currently no verified flashable MIUI 14 port for Joyeuse in this repository.
