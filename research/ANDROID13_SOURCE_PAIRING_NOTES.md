# Android 13 Joyeuse source pairing notes

Review date: 2026-10-20. This is a source audit, not a build result.

## Pinned candidate sources

- Device tree: nekoshirro/device_xiaomi_joyeuse, branch 13-FBEv1, commit 7bedf8a993c58b7743aebd49dfc5e3a7bfa9242f.
- Vendor files: nekoshirro/vendor_xiaomi_joyeuse, branch 13, commit ad53e0661749e8f697d9ed3bcd2f9aa47b82cc29.
- Kernel candidate: ArrowOS-Devices/android_kernel_xiaomi_sm6250, branch arrow-13.0, commit a8dc7bc9a34a090eccfc4d8d5c53c694d0f85186.

## Findings

1. The device tree's product file defines an AOSP-derived `aosp_joyeuse` product. It is not a MIUI product definition.
2. The device tree expects `kernel/xiaomi/sm6250`, config `cust_defconfig`, and a clang toolchain named `alchemist`. The candidate kernel has that config path and reports Linux 4.14.304, but no pinned manifest or build log proves the exact three source revisions were built together.
3. The kernel config enables `CONFIG_MODVERSIONS=y`, `CONFIG_MODULE_SIG=y`, and `CONFIG_MODULE_SIG_FORCE=y`. The inspected vendor repository tree contains no `.ko` files, so there is no evidence of prebuilt vendor kernel modules in that snapshot. Any separately supplied modules would still need ABI and signing compatibility.
4. The vendor commit history references Qualcomm QSSI 13 radio components and a telephony import from `SURYAGlobal_V14.0.1.0.SJGMIXM`. This is provenance evidence for selected blobs, not proof that every blob matches the proposed MIUI 14 China framework.
5. The device tree includes a broad Joyeuse-specific hardware configuration and a large VINTF manifest. No public reproducible build record for the exact proposed MIUI 14 `cupid` to Joyeuse combination was found in this search.

## Decision

Keep this as a research candidate only. Before a build can be called reproducible, identify a compatible manifest and exact toolchain revision, audit the framework/vendor interfaces and blob provenance, and validate the output in an isolated environment. No ROM was built and no live device was accessed.
