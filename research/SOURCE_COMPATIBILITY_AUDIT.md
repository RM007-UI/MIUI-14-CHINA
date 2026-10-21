# Joyeuse source compatibility audit

Audit date: 2026-10-21. Status: **source metadata inspected; no source build performed**.

## Pinned candidate sources

These are candidate inputs only, not yet approved as a compatible MIUI port:

- Device tree: `nekoshirro/device_xiaomi_joyeuse`, branch `13-FBEv1`, commit `7bedf8a993c58b7743aebd49dfc5e3a7bfa9242f`.
- Vendor blobs: `nekoshirro/vendor_xiaomi_joyeuse`, branch `13`, commit `ad53e0661749e8f697d9ed3bcd2f9aa47b82cc29`.
- Kernel: `ArrowOS-Devices/android_kernel_xiaomi_sm6250`, branch `arrow-13.0`, commit `a8dc7bc9a34a090eccfc4d8d5c53c694d0f85186`.

## Findings from tracked files

### Device tree

- `AndroidProducts.mk` offers `aosp_joyeuse-user`, `userdebug`, and `eng`; it is not a MIUI product definition.
- `aosp_joyeuse.mk` inherits `vendor/aosp/config/common_full_phone.mk`, so the candidate is AOSP-derived.
- Its declared build fingerprint is a Google Pixel 7 Pro (`google/cheetah/cheetah:13/...`) even though the product device is Joyeuse. This is a build override, not evidence of actual device identity; it must not be carried into a release build without deliberate review.
- `device.mk` has MIUI Camera integration switches, but those alone do not make the product MIUI-compatible.
- `proprietary-files.txt` says the unpinned blobs are extracted from Joyeuse Android 11 Indonesian firmware `V12.5.4.0.RJZIDXM`. The blob source is older than the Android 13 target and needs explicit compatibility review.

### Kernel

- The candidate kernel's tracked Makefile identifies Linux `4.14.304`.
- `cust_defconfig` contains a local version marker referring to `LA.UM.9.1` and `QSSI13.0`, suggesting an Android 13-era Qualcomm base, but this alone does not establish compatibility with the selected vendor blobs, boot image format, or MIUI framework.
- Kernel source/config still needs reproducible build verification and comparison against the exact Joyeuse boot/vendor expectations.

### Vendor repository

- `joyeuse-vendor.mk` is generated from a proprietary blob extraction and copies files across system, system_ext, product, and vendor destinations. Its branch label is not proof that every blob came from Android 13.
- The vendor source revision and extraction origin must be reconciled with the device tree's Android 11 blob manifest before any build attempt.

## Compatibility decision

**Do not start a full ROM build from these sources yet.** The current inputs are useful AOSP-derived Joyeuse references, but are not a validated MIUI 14 China Android 13 source manifest. At minimum, next checks must:

1. Pin every source repository to exact commit SHAs in a manifest.
2. Compare vendor blob origin, VINTF manifests/matrices, sepolicy, init scripts, fstab, firmware expectations, and kernel modules.
3. Replace/review AOSP product definitions and generic fingerprint for the intended MIUI target rather than blindly copying them.
4. Confirm boot header/version, AVB/vbmeta arrangement, and actual Joyeuse partition sizes from trustworthy target-specific sources.
5. Run build and image validation only in an environment with sufficient disk/RAM; a standard GitHub-hosted runner is not a full Android build host.

## Evidence links

- Device tree BoardConfig: https://github.com/nekoshirro/device_xiaomi_joyeuse/blob/13-FBEv1/BoardConfig.mk
- Device tree product definition: https://github.com/nekoshirro/device_xiaomi_joyeuse/blob/13-FBEv1/aosp_joyeuse.mk
- Device tree blob manifest: https://github.com/nekoshirro/device_xiaomi_joyeuse/blob/13-FBEv1/proprietary-files.txt
- Vendor makefile: https://github.com/nekoshirro/vendor_xiaomi_joyeuse/blob/13/joyeuse-vendor.mk
- Kernel config: https://github.com/ArrowOS-Devices/android_kernel_xiaomi_sm6250/blob/arrow-13.0/arch/arm64/configs/cust_defconfig
- Kernel Makefile: https://github.com/ArrowOS-Devices/android_kernel_xiaomi_sm6250/blob/arrow-13.0/Makefile

## Automated source-pin preflight

On 2026-10-21, the lightweight GitHub Actions workflow verified that all three pinned commit SHAs exist in their stated repositories and inspected selected source files without cloning full source trees:

- Device tree: exact commit verified; product targets are `aosp_joyeuse`, inherit `vendor/aosp/config/common_full_phone.mk`, and declare a Pixel 7 Pro fingerprint override.
- Vendor: exact commit verified; repository is generated from proprietary blobs, but this does not prove that the blobs match the target MIUI Android 13 system.
- Kernel: exact commit verified; Linux version is 4.14.304 and its local-version string references a QSSI 13-era Qualcomm base.

Successful preflight run: https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39567928418

Artifact: `joyeuse-source-preflight`, text-only, expires 2026-11-04. This is identity and metadata validation only; it is not a build or boot test.


## Additional compatibility gate (2026-10-21)

A second direct read of the pinned source files reconfirmed the following details:

- `BoardConfig.mk` is a conventional Android device build configuration; it does not itself establish compatibility with the MIUI donor's proprietary framework.
- `AndroidProducts.mk` exposes only `aosp_joyeuse` lunch targets. A real MIUI port needs a deliberately reviewed product definition rather than simply building this target and renaming the output.
- `proprietary-files.txt` explicitly attributes the unpinned proprietary blobs to Joyeuse Android 11 Indonesia firmware `V12.5.4.0.RJZIDXM`. This is a concrete provenance mismatch to investigate against the Android 13 MIUI system, not proof that every individual blob is incompatible.
- The vendor makefile is generated packaging metadata; its branch name `13` cannot establish the Android version or firmware provenance of every included binary.

### Direct Joyeuse port reference

A public Redmi Note 9 Pro updates channel indexed a Joyeuse-only MIUI 14 China Android 13 weekly port by TheHan45 (build `V14.0.23.6.5.DEV`, June 2023), and a newer community listing describes `V14.0.10.0.TLCCNXM` as a Joyeuse-only beta dated 2026-10-16 with reported Setup Wizard and NFC issues. These posts establish that community ports have been announced; they do **not** establish that their downloads are still available, authentic, safe, or compatible with this phone's current state.

References:
- Historical Android 13 Joyeuse port listing: https://telegram.me/s/RN9ProUpdate/7152?q=%23A13
- Newer beta listing and reported bugs: https://en.tgdio.com/channel/%40rn9proupdate/7305

### Decision / next gate

No new image has been built and no device has been flashed. Do not treat the existing community ZIP as a release candidate until the full installer payload can be obtained reliably and its boot image, vendor partition, VINTF declarations, sepolicy, firmware assumptions, and partition layout have been checked against Joyeuse. The current Google Drive rate-limit failure is a transport/access blocker, not a compatibility verdict. Do not bypass it by flashing an unverified mirror.

The next useful automated step is a source-only gate that inventories device-tree partition, fstab, VINTF, sepolicy, and kernel-module configuration at the pinned commit, then compares that inventory to metadata recovered from the actual candidate package. A successful source-pin check alone is insufficient to authorize a build or flash.


## Focused configuration review after source-inventory run

The expanded preflight completed successfully on commit `90957865bd75ebe1491b6e04cd441639bcb891dc`:
https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39568647143

Artifact (text-only, expires 2026-11-04): https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39568647143/artifacts/12331340364

A direct read of the pinned device-tree files adds these concrete checks:

- Device VINTF manifest declares target-level 4 and HIDL HALs for core device functions; the device tree also points to a framework manifest and device compatibility matrix. These declarations need comparison with the donor's actual vendor/system manifests, not just presence checks.
- `rootdir/etc/fstab.qcom` mounts `system`, `system_ext`, `product`, and `vendor` as logical ext4 partitions in `super`, with AVB-related flags. It also includes metadata, userdata encryption, firmware, and other device-specific mounts. These are critical assumptions for any repackaged image.
- `BoardConfig.mk` expects boot header version 2, a separated DTBO, AVB enabled, and a 8,589,934,592-byte super partition/group configuration. These are source configuration values; actual phone partition sizes and donor boot/AVB layout must be confirmed independently before any image is approved.
- The GitHub recursive tree API marked the kernel repository tree as truncated (74,507 entries reported, partial response). Therefore, kernel path inventory is explicitly partial; the exact pinned Makefile and defconfig were read separately.

The preflight passed because all three pinned commits and selected source reads succeeded. It is **not** a compatibility pass. No build or device operation was performed.
