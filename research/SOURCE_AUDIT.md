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
| Kernel | https://github.com/jandaX/android_kernel_xiaomi_joyeuse/tree/Tanya | Repository description says “A13 kernel”; default branch `Tanya`; latest observed commit on this branch 2023-05-18; includes `joyeuse_defconfig` | Candidate kernel is Android 13-era, but the device tree branch specifies `cust_defconfig`, which was not found at `arch/arm64/configs/cust_defconfig` in this kernel branch. A follow-up scan of all six visible branches (`404`, `Siska`, `Tanya`, `Titaniya`, `Ulan`, `prebuild`) found root-level `joyeuse_defconfig` and `stock_defconfig`, but no root-level `cust_defconfig`. Kernel commit history does contain older commits whose messages mention `cust_defconfig`, but at least one such commit modifies `arch/arm64/configs/vendor/xiaomi/miatoll_defconfig` rather than the expected root path. A further exact-match search found the Android 13 EvolutionX device tree at https://github.com/KRY0NiTE/EvolutionX-tiramisu/tree/device. Its `BoardConfig.mk` confirms the intended config is `vendor/xiaomi/miatoll_defconfig` (not root-level `cust_defconfig`), kernel source path `kernel/xiaomi/sm6250`, kernel version `4.14.315`, and clang `alchemist`. This corrects the earlier interpretation: the relevant expected path is the vendor-specific `vendor/xiaomi/miatoll_defconfig`, while the previously inspected `jandaX/android_kernel_xiaomi_joyeuse` `Tanya` branch exposes `vendor/atoll_defconfig` and `vendor/atoll-perf_defconfig` in its visible vendor config directory, not `vendor/xiaomi/miatoll_defconfig`. Therefore this branch is still not a verified exact match; do not substitute `atoll_defconfig` or rename a config without checking the matching kernel source revision and build manifest. |
| Newer default branches | https://github.com/nekoshirro/device_xiaomi_joyeuse/tree/16-los and https://github.com/nekoshirro/vendor_xiaomi_joyeuse/tree/16 | Recent commits observed in December 2025; branches target a newer Android generation | Useful as a future reference, not directly interchangeable with the Android 13 source ROM. |
| Older device/vendor snapshot | https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse and https://github.com/AOSP-joyeuse/platform_vendor_xiaomi_joyeuse | Last observed commits in October 2022 | Useful as historical reference only; not a modern base.
| Older device/vendor snapshot | https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse and https://github.com/AOSP-joyeuse/platform_vendor_xiaomi_joyeuse | Last observed commits in October 2022 | Useful as historical reference only; not a modern base. |

The newer device and vendor candidates are at:
- Device tree: https://github.com/nekoshirro/device_xiaomi_joyeuse
- Vendor blobs: https://github.com/nekoshirro/vendor_xiaomi_joyeuse
- Android 13-labelled kernel candidate: https://github.com/jandaX/android_kernel_xiaomi_joyeuse
- Additional Android 13 device-tree/build-context reference: https://github.com/KRY0NiTE/EvolutionX-tiramisu/tree/device

The EvolutionX `device` branch is useful as a separate comparison because its `BoardConfig.mk` spells out an Android 13-era kernel configuration and toolchain. Its setup script also performs broad `rm -rf device/xiaomi/*`-style cleanup and clones dependencies for its own build environment; inspect it as reference only, do not execute it in this project. A better filename-level match for the `nekoshirro` tree was found in `ArrowOS-Devices/android_kernel_xiaomi_sm6250` branch `arrow-13.0`, which has root-level `cust_defconfig`, but the kernel is reported as 4.14.304 rather than the separate EvolutionX reference's 4.14.315.

Further inspection of `aosp_joyeuse.mk` and `AndroidProducts.mk` confirms that this Android 13-era tree defines an **AOSP** product (`aosp_joyeuse`) and inherits `vendor/aosp/config/common_full_phone.mk`; it is not a ready-made MIUI ROM target. Its `device.mk` includes many hardware-specific components (camera, audio, display, radio, fingerprint, GNSS and vendor interfaces) that need to match the selected Android/vendor baseline. Commit history includes MIUI Camera configuration work, but that does not turn the whole tree into a MIUI system port.

No repositories were cloned, compiled, or integrated. Branch labels and commit dates are preliminary screening signals only.

### Static kernel-config comparison (metadata only)

The `ArrowOS-Devices/android_kernel_xiaomi_sm6250` `arrow-13.0` branch is the closest filename-level match found for `nekoshirro/device_xiaomi_joyeuse` `13-FBEv1`: both use the source path `kernel/xiaomi/sm6250`, and the device tree requests root-level `cust_defconfig`, which exists in that kernel branch. The kernel root Makefile reports Linux 4.14.304, while `cust_defconfig` identifies a Qualcomm LA.UM.9.1 / QSSI13-era configuration. This is encouraging but does **not** establish that the tree and kernel were tested together or that the kernel can be used for a MIUI 14 port.

Important config risk: `cust_defconfig` enables `CONFIG_MODULE_SIG_FORCE=y` and module signing. If external/vendor kernel modules are built with a key that does not match the kernel's trusted signing key, those modules may be rejected at runtime. The exact kernel/module signing setup must be verified before treating this as a viable pairing. This is a static observation from the config, not a tested failure.

The device tree sets `TARGET_KERNEL_CLANG_VERSION := alchemist` and several LLVM/LLD flags. The config file alone does not prove that the expected compiler exists in the chosen Android build tree or that this kernel revision builds with that toolchain. The matching manifest, compiler revision, vendor blobs, and device-specific modules remain unverified.

### Android 13 device/vendor interface audit

The `nekoshirro/device_xiaomi_joyeuse` `13-FBEv1` device manifest declares compatibility target level 4 and a set of HIDL hardware interfaces including audio, fingerprint, camera, keymaster/gatekeeper, radio, power, and Qualcomm/Dolby services. Its compatibility matrix lists required framework-facing interfaces. These declarations are useful as the target device's integration contract, but they do not prove that the MIUI 14 `cupid` framework will accept this combination without VINTF, permission, SELinux, and service-level adjustments.

The matching `nekoshirro/vendor_xiaomi_joyeuse` branch `13` contains generated vendor build definitions and a large `joyeuse-vendor.mk`/proprietary blob set, so there is at least a concrete Android 13-labelled target vendor snapshot to audit. Its `BoardConfigVendor.mk` is only a generated header in the inspected revision; that file alone does not identify the exact firmware extraction baseline. The existence of proprietary blobs also does not mean they can be redistributed inside a public ROM artifact.

This strengthens the target-side research baseline, but a key gap remains: no matching repo manifest or build record has yet proved that the exact `13-FBEv1` device tree, vendor branch `13`, and ArrowOS kernel branch `arrow-13.0` were built and tested together. Their labels are not proof of a coherent tested stack.

## Engineering conclusion

This is a **high-risk cross-device port**: the source and target have different SoCs and vendor hardware stacks. The likely reusable part is the MIUI framework/system layer as a research target, not the source device's kernel, vendor image, firmware or partition layout. Even framework-level porting requires device-specific integration work and cannot be promised to boot.

The recent `joyeuse` device/vendor trees provide a better lead for further source inspection, but their default branches target a much newer Android generation than the Android 13 source ROM. The older Android 13-labelled kernel is not, by itself, enough to establish a coherent buildable stack. We still need to identify mutually compatible branches and verify the build configuration.

## Next safe research steps

1. Continue validating the closest filename-level pair: `ArrowOS-Devices/android_kernel_xiaomi_sm6250` `arrow-13.0` plus `nekoshirro/device_xiaomi_joyeuse` `13-FBEv1`. Check the exact manifest and compiler revision, plus the `CONFIG_MODULE_SIG_FORCE` signing implications for device/vendor modules. The config path matches, but no paired build or runtime test is confirmed. Do not rename configs or mix this with the separate EvolutionX `miatoll_defconfig` layout.
2. Find a build manifest or public build record proving which exact kernel, device tree, vendor branch, and firmware baseline were used together; audit VINTF declarations and proprietary blob provenance.
3. Compare the source ROM's Android 13 framework/vendor interfaces against the selected target device/vendor baseline; do not assume the Xiaomi 12's proprietary components are reusable.
4. Record target partition/boot configuration from public source metadata, without issuing commands to the user's phone.
5. Keep CI limited to static checks until a documented and reproducible build strategy exists. Do not generate flashable artifacts or run `adb`/`fastboot` in CI.

## Explicitly not done

- No ROM images or firmware were downloaded.
- No proprietary blobs were copied.
- No ROM was built or packaged.
- No commands were sent to the phone.
- No claim is made that an installable or bootable port exists.
