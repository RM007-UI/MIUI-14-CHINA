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
