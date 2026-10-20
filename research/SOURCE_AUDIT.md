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

### Search for reproducible Android 13 build evidence

Checked the GitHub Actions runs and GitHub Releases endpoints for the inspected Android 13 device-tree, vendor, and kernel candidates; the queried endpoints returned no public workflow runs or releases for those repositories. A targeted public GitHub commit search for an explicit `joyeuse` + `MIUI 14` + `Android 13` combination also returned no matching commits.

This does **not** prove that nobody has ever built a ROM locally or through another CI system. It means the public evidence currently found is insufficient to claim a reproducible Android 13 build for the exact proposed component set, and there is no located public CI artifact we can responsibly use as a known-good baseline. Some newer commits in the broader `nekoshirro` repository family include later Android/QSSI integration fixes, which further reinforces that branches and build generations must not be mixed casually.

### Re-check of the Android 13 candidate set and reproducibility gap

A more precise cross-check of the older Android 13 candidate confirms:
- `nekoshirro/device_xiaomi_joyeuse` branch `13-FBEv1` points to source kernel path `kernel/xiaomi/sm6250`, config `cust_defconfig`, and clang toolchain label `alchemist`; inspected branch head is `7bedf8a993c58b7743aebd49dfc5e3a7bfa9242f` (2023-06-26).
- `ArrowOS-Devices/android_kernel_xiaomi_sm6250` branch `arrow-13.0` has `arch/arm64/configs/cust_defconfig` and labels its local version as a Qualcomm QSSI 13 / SM6250 kernel family; inspected head is `a8dc7bc9a34a090eccfc4d8d5c53c694d0f85186`.
- `nekoshirro/vendor_xiaomi_joyeuse` branch `13` exists and includes generated vendor build definitions and proprietary blobs.

These facts make the ArrowOS kernel a **plausible candidate by path and Android-generation clues**, not a proven matching kernel. The inspected sources do not establish an immutable manifest tying these exact device-tree, vendor, kernel, common-device/vendor and firmware revisions into one tested Android 13 build. The product makefile also represents an AOSP-derived product rather than MIUI. No claim is made that these parts build together, boot, or work with the `cupid` MIUI 14 framework. Keep all components as separate audit candidates until a source manifest/build log or other reproducible evidence is found.

### Newer AOSP-joyeuse source set: coherent project family, but not an Android 13 MIUI baseline

The newer `AOSP-joyeuse` organization exposes matching project-family repositories for device tree, SM6250 common device tree, Joyeuse vendor blobs, common vendor blobs, and kernel source, all on branch `bka`:
- device tree head `f06c14ed5374664c47b59611f0718d354d7096ef` (2025-12-12)
- Joyeuse vendor head `a53b109b9133fc8407244b1d0bcfcfcd98493e78` (2025-12-13)
- kernel head `bd0c53c5a3e98cd3d405b7675b86ac4319ee3c2f` (2025-12-13)
- common device tree and vendor repositories also exist on `bka`.

This is a stronger candidate for understanding how a later Joyeuse stack is assembled than mixing unrelated forks. However, it remains explicitly marked Working In Progress, the kernel repo itself carries a force-push warning, and the product file identifies a Lineage/Evolution-style Android 12 build fingerprint. Its device tree uses `vendor/xiaomi/miatoll_defconfig`, while the kernel's root config path is not `cust_defconfig`; the exact config is therefore not yet pinned from the inspected paths. This set is **not** evidence of an Android 13 MIUI build and should not be merged into the older `13-FBEv1` stack without a pinned manifest and compatibility audit.

The kernel history also contains a recorded Soong failure caused by duplicate `qti_kernel_headers` module definitions (commit `ec923a7a0101d17f7b03ebe21a4e9087a8edb28f`, 2025-08-27). Later commits may have addressed it, so this is historical evidence of integration issues, not a claim that the current head fails to build.

### Public build-script audit: useful references, but not a matching Android 13 manifest

The public `nekoshirro/platform_manifest-joyeuse` repository's `evox-q1/evolution.sh` is a build script for Evolution-X/AOSP Android 16, not the requested MIUI 14 Android 13 port. It pins no immutable commit IDs for the cloned device/vendor/kernel repositories (uses shallow clones), so it is not a reproducible source manifest. It clones newer AOSP-joyeuse device/vendor/common repositories and a different kernel repository/branch, which must not be silently substituted for the 2023 `13-FBEv1` + `vendor_xiaomi_joyeuse` snapshots. The script also contains broad destructive cleanup commands and a hard-coded Telegram bot credential. **The script was not executed and the credential is intentionally not reproduced here.** The credential should be treated as exposed and rotated/revoked by its owner; do not use it or contact the bot.

This repository is evidence that later Joyeuse builds use a separately assembled set of device, common, vendor, and kernel projects, but it does not establish a tested component set for this MIUI 14 cross-device port.

### Kernel dependency located: prebuilt kernel for `Bianca-13`

The previously missing repository has now been identified: [`nekoshirro/device_xiaomi_joyeuse-kernel`](https://github.com/nekoshirro/device_xiaomi_joyeuse-kernel), branch `Maverick`, head commit `60c8b0bf7ff4ce5e1d803ccb8eb04571ff9d6ba7` (2023-05-18). Its `BoardConfig.mk` points to prebuilt `Image` and `dtb.img`; its `device.mk` packages that Image as the kernel and supplies vendor kernel headers. The device tree's `Bianca-13` branch explicitly inherits this project's `BoardConfig.mk` and `device.mk`, so this is a real declared dependency for that branch—not merely a guessed repo name.

Important limits:
- This kernel repository contains prebuilt binary artifacts rather than the full source/configuration needed to independently rebuild and inspect the kernel. We have not established the exact source commit, defconfig, signing-key compatibility, or runtime test result for the binary.
- This pairing applies to `Bianca-13`; it does **not** establish a kernel pairing for `13-FBEv1`, whose BoardConfig directly names `kernel/xiaomi/sm6250` and `cust_defconfig`.
- The separate prebuilt repository's latest visible commit is from May 2023, while the vendor/device tree snapshots were last updated in August 2023. Dates alone neither prove incompatibility nor prove a successful integrated build.
- The Pixel 6 build fingerprint in `Bianca-13/joyeuse.mk` remains an unresolved provenance/configuration warning. It is not proof that the final build was tested on joyeuse.

This narrows the search but does not yet supply a complete, reproducible manifest tying a specific source ROM, device tree, vendor snapshot, kernel binary/source and firmware baseline into a verified build.

### Additional branch-history finding: similarly named branches are not interchangeable

A second branch audit exposed a trap worth recording. The device tree's `Bianca-13` branch has the same `cust_defconfig` and `kernel/xiaomi/sm6250` declarations, but its `BoardConfig.mk` and `joyeuse.mk` inherit a separate `device/xiaomi/joyeuse-kernel` prebuilt-kernel project. That path is not present inside the inspected `device_xiaomi_joyeuse` repository itself, so the kernel dependency must be found and pinned independently. The same product file carries a Google Pixel 6 `raven` Android 12 build description/fingerprint. That is a strong sign this branch's product identity/config was adapted from another base and it must not be treated as proof of a clean, tested Android 13 kernel pairing.

The newer `16-los` branch is a different layout again: it switches the device path and OTA asserts to the broader `miatoll` family and uses `vendor/xiaomi/miatoll_defconfig`, not root-level `cust_defconfig`. It is therefore not a drop-in replacement for the `13-FBEv1` tree. Mixing these branches' BoardConfig files, kernel configs, or vendor snapshots without a verified manifest would create a new untested stack.

## Engineering conclusion

This is a **high-risk cross-device port**: the source and target have different SoCs and vendor hardware stacks. The likely reusable part is the MIUI framework/system layer as a research target, not the source device's kernel, vendor image, firmware or partition layout. Even framework-level porting requires device-specific integration work and cannot be promised to boot.

The recent `joyeuse` device/vendor trees provide a better lead for further source inspection, but their default branches target a much newer Android generation than the Android 13 source ROM. The older Android 13-labelled kernel is not, by itself, enough to establish a coherent buildable stack. We still need to identify mutually compatible branches and verify the build configuration.

## Next safe research steps

1. Continue validating the closest filename-level pair: `ArrowOS-Devices/android_kernel_xiaomi_sm6250` `arrow-13.0` plus `nekoshirro/device_xiaomi_joyeuse` `13-FBEv1`. Check the exact manifest and compiler revision, plus the `CONFIG_MODULE_SIG_FORCE` signing implications for device/vendor modules. The config path matches, but no paired build or runtime test is confirmed. Do not rename configs or mix this with the separate EvolutionX `miatoll_defconfig` layout.
2. Find and pin the missing `device/xiaomi/joyeuse-kernel` dependency (or another documented kernel source) and locate a manifest/build record proving which exact kernel, device tree, vendor branch, and firmware baseline were used together. Do not mix `Bianca-13`, `13-FBEv1`, and `16-los` configurations just because some variable names overlap; audit VINTF and proprietary blob provenance.
3. Compare the source ROM's Android 13 framework/vendor interfaces against the selected target device/vendor baseline; do not assume the Xiaomi 12's proprietary components are reusable.
4. Record target partition/boot configuration from public source metadata, without issuing commands to the user's phone.
5. Keep CI limited to static checks until a documented and reproducible build strategy exists. Do not generate flashable artifacts or run `adb`/`fastboot` in CI.

## Explicitly not done

- No ROM images or firmware were downloaded.
- No proprietary blobs were copied.
- No ROM was built or packaged.
- No commands were sent to the phone.
- No claim is made that an installable or bootable port exists.


### Toolchain and packaging dependency check (2026-10-20)

A targeted follow-up checked the exact build declarations in `nekoshirro/device_xiaomi_joyeuse` branch `13-FBEv1` and the candidate kernel branch `arrow-13.0`:

- `BoardConfig.mk` explicitly selects `TARGET_KERNEL_CONFIG := cust_defconfig`, `TARGET_KERNEL_SOURCE := kernel/xiaomi/sm6250`, `TARGET_KERNEL_CLANG_VERSION := alchemist`, `LLVM=1`, and `LD=ld.lld`. This narrows the expected build environment, but it does not identify an immutable clang source revision or prove that `prebuilts/clang/host/linux-x86/clang-alchemist` is present in the intended ROM tree.
- The selected ArrowOS kernel candidate has Linux version 4.14.304 and the requested `arch/arm64/configs/cust_defconfig`. This confirms a path-level match only. No pinned manifest or build log was found tying this kernel SHA to the exact device/vendor SHAs, so it remains an unverified combination.
- The device product file `aosp_joyeuse.mk` declares `PRODUCT_NAME := aosp_joyeuse` and inherits `vendor/aosp/config/common_full_phone.mk`. Therefore this tree is an AOSP-derived target, not a MIUI product definition. A port would need a deliberately engineered product configuration rather than merely changing a product name.
- The selected kernel config enables `CONFIG_MODULE_SIG_FORCE=y`. This is a concrete review item: kernel modules supplied by the vendor must be compatible with the kernel's signature trust setup. The public config does not establish whether the exact modules and signing key match.
- The vendor repository's generated build definitions reference numerous proprietary system/vendor services and VINTF XML files. This reinforces that the target stack is more than a generic system image; exact HAL/service declarations and blob baseline must be reconciled before building.

No reproducible public manifest, exact compiler pin, build log, boot test, or successful MIUI 14 `cupid` → `joyeuse` artifact was found during this pass. This is a documented gap, not evidence that a build is impossible. No ROM was downloaded, compiled, packaged, or flashed.
