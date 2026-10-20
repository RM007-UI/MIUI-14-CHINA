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
| Device tree | https://github.com/nekoshirro/device_xiaomi_joyeuse | Default branch `16-los`; latest commit observed 2025-12-03; target-specific `joyeuse` changes | Most promising recent device-tree lead, but its Android 16-oriented branch is not automatically a suitable Android 13 base. Inspect branches and build configuration before selecting it. |
| Vendor blobs | https://github.com/nekoshirro/vendor_xiaomi_joyeuse | Default branch `16`; commits observed 2025-12-03, including camera and vendor compatibility changes | Active-looking target-specific vendor tree, but branch level differs from the Android 13 source ROM. Do not mix blindly across Android releases. |
| Kernel | https://github.com/jandaX/android_kernel_xiaomi_joyeuse | Repository description says “A13 kernel”; default branch `Tanya`; latest commit observed 2023-05-18 | Android 13-era candidate, but old. Its kernel config, toolchain, required modules and compatibility with the chosen device/vendor tree remain unverified. |
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

1. Inspect the candidate device tree's Android makefiles, `BoardConfig.mk`, dependencies and branch history.
2. Inspect vendor branch dependencies and the kernel's defconfig/toolchain assumptions; compare their Android generation and interfaces.
3. Record target Android/vendor API level and partition/boot configuration from public source metadata, without issuing commands to the user's phone.
4. Build a compatibility matrix and decide whether the source set is coherent before attempting any compile.
5. Keep CI limited to static checks until a documented and reproducible build strategy exists. Do not generate flashable artifacts or run `adb`/`fastboot` in CI.

## Explicitly not done

- No ROM images or firmware were downloaded.
- No proprietary blobs were copied.
- No ROM was built or packaged.
- No commands were sent to the phone.
- No claim is made that an installable or bootable port exists.
