# Build environment preflight — Joyeuse MIUI 14 Android 13

Review date: 2026-10-20  
Status: **BLOCKED — no verified build host or reproducible source manifest is available in this session.**

This is an execution gate, not a build recipe. Do not interpret the candidate source pins as a proven compatible set.

## Host requirements

The official AOSP setup guide currently specifies a 64-bit x86 workstation, at least 400 GB of free disk space (roughly 250 GB for checkout plus 150 GB for build output), at least 64 GB RAM, and 64-bit Linux with glibc 2.17 or later. These are current AOSP baseline requirements; the exact Android 13/vendor port may have different needs and should not be assumed to fit a smaller runner.

Reference: https://source.android.com/docs/setup/start/requirements

## Preflight gates

- [ ] A reachable, authorized Linux x86_64 build host is available.
- [ ] Host CPU, RAM, filesystem free space, and filesystem type have been measured.
- [ ] Build workspace has enough free disk for source checkout, extracted donor package, intermediate outputs, logs, and final artifacts.
- [ ] Exact Android 13 platform manifest/revision is pinned.
- [ ] Device tree, common tree, vendor blobs, kernel, firmware baseline, and clang toolchain are pinned as a compatible set with provenance.
- [ ] Donor Recovery package identity and SHA-256 are recorded before extraction.
- [ ] Donor images are inspected read-only; no donor cupid kernel/vendor/boot/partition images are transplanted to Joyeuse.
- [ ] Target VINTF, SELinux, property contexts, boot image configuration, AVB, and partition assumptions are reviewed.
- [ ] Proprietary blob use and any redistribution are handled appropriately.
- [ ] First build is isolated and non-flashing; build logs and output hashes are retained.
- [ ] A built image is not described as boot-tested unless a real, controlled boot and hardware test has been performed.

## Current result

The connected GitHub repository can run short metadata checks, but its current workflow does not provide a full Android build environment. No Desktop Commander host is connected in the current session. Therefore host capacity cannot be measured or a source sync/build truthfully started here.

No source ROM was downloaded or extracted, no Android source tree was synced, no ROM image was built, and no phone/partition/flash operation was performed.

## Pinned research candidates (not yet proven compatible)

- Device tree: `nekoshirro/device_xiaomi_joyeuse` at `7bedf8a993c58b7743aebd49dfc5e3a7bfa9242f`.
- Vendor tree: `nekoshirro/vendor_xiaomi_joyeuse` at `ad53e0661749e8f697d9ed3bcd2f9aa47b82cc29`.
- Kernel candidate: `ArrowOS-Devices/android_kernel_xiaomi_sm6250` at `a8dc7bc9a34a090eccfc4d8d5c53c694d0f85186`.
- MIUI donor candidate: Xiaomi 12 China Stable Recovery `V14.0.10.0.TLCCNXM`; public index lists it at about 5.6 GB, but the package itself has not been downloaded or hash-verified.

The three Git repositories above are candidate inputs only. Their revisions are not a reproducible manifest and have not been proven to build together. A cross-device MIUI port remains a high-risk engineering project, not a packaging task.
