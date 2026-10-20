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


## Additional provenance and integration checks

- The device tree's `proprietary-files.txt` explicitly says its unpinned blobs originate from `joyeuse-qssi-user-11-RKQ1.200826.002-V12.5.4.0.RJZIDXM-release-keys` (Android 11 / MIUI 12.5-era baseline). The vendor repository's later commits update selected components, including Qualcomm QSSI 13 radio/IMS-related blobs and telephony references, but this is a mixed provenance set, not proof every binary was refreshed for Android 13.
- The source tree's compatibility matrix is not empty: it declares a limited set of required HIDL interfaces. It still needs to be merged and checked against the final framework and vendor manifests; merely having XML files is not a compatibility test.
- The device fstab uses logical system/system_ext/product/vendor partitions and AVB options. Its paths and flags are build-source assumptions; they are not a live read of the target phone's actual partition table.
- The device tree contains both platform-private and vendor SELinux policy, including Xiaomi/Qualcomm-specific domains and property contexts. A MIUI framework introduces additional properties/services and permissions; policy must be audited and built without papering over denials with broad permissive rules.
- The exact source device ROM's full boot/partition metadata and the target device's live partition map have not been compared. No firmware archive was downloaded and no device was queried.

## Updated risk assessment

Blob provenance and policy integration are now high-priority blockers, alongside the missing pinned manifest/toolchain and framework/VINTF reconciliation. The Android 11 baseline line in the extraction list does not automatically make the tree unusable, because some blobs are separately updated; it does mean we cannot call the entire vendor stack a verified Android 13 baseline without per-component evidence.


## MIUI source-side comparison status

The pinned XiaomiFirmwareUpdater archive index identifies the proposed source package as Xiaomi 12 China Stable Recovery `V14.0.10.0.TLCCNXM`, Android 13, listed at approximately 5.6 GB (with a separate Fastboot package listed at approximately 7.0 GB). These are archive-index metadata only: the package was not downloaded, hashed, or inspected, so no source-side boot image, dynamic-partition map, AVB metadata, or proprietary framework payload has been verified.

Reference: https://github.com/XiaomiFirmwareUpdater/xiaomifirmwareupdater.github.io/blob/f3fd55eee00004d859cde590e446fabc4e93acc5/pages/miui/full/cupid.md

## Security and test-policy implications

The target device tree's SELinux rules include device-specific permissions and property labels. Any port must reconcile MIUI-added properties, service domains, and vendor interactions against enforcing policy. Broadly disabling SELinux or accepting a test-signed AVB setup is not an acceptable compatibility workaround.

The next source-only milestone is to acquire and inspect source-package metadata in a controlled build workspace, pin all input revisions and compiler provenance, then produce a concrete framework/VINTF/partition compatibility checklist before attempting a build. No target-phone commands, partition reads/writes, downloads of the large ROM, or flashing occurred during this review.


## Pinned target manifest cross-check

The exact pinned Joyeuse Android 13 device-tree files were fetched by commit/branch rather than inferred from the repository's moving default branch:

- `manifest.xml` at `13-FBEv1`, blob `b73e69f5d5ce685d4faeadc4a919fdd1bd4117fd`, declares device manifest target-level 4 and includes HIDL service declarations for device hardware such as audio, fingerprint, Bluetooth, camera, DRM, gatekeeper, keymaster, radio and media.
- `manifest_joyeuse.xml` at the same ref, blob `02182c079721fc1f5f457b6d1f41c476062dbdcc`, adds the Joyeuse NFC HAL.
- `compatibility_matrix.xml` at the same ref, blob `5f447e787c3cb6b4557be4ad519c68c27e1e015e`, contains required HIDL interfaces; it is not a proof that the Xiaomi 12 framework will accept this target vendor implementation.
- `BoardConfig.mk` at the same ref, blob `4067e1e9069d64d72e7c940442e1234c6b543fb3`, names target framework/device compatibility inputs and ODM manifest SKU files. Those exact inputs must be resolved in a complete source manifest before VINTF validation.

These declarations make the main risk concrete: the donor's framework and the target's hardware services are not interchangeable simply because both use Android 13. The final assembled framework compatibility matrix must be checked against the target's actual device/vendor/ODM manifests and the service implementations that will ship.

## Build gate decision

Do not download the 5.6 GB Recovery archive or the 7.0 GB Fastboot archive merely to start experimenting. The source archive index gives version and approximate size, but not enough evidence to choose or safely transform a package. First establish a pinned build manifest, toolchain provenance, sufficient workspace/storage, and a repeatable unpack/inspect workflow. If the donor package is later inspected, keep it as source material only: do not transplant the Xiaomi 12 boot, vendor, firmware, modem, or partition images onto Joyeuse.

No ROM archive was downloaded, no third-party build script was run, and no phone-side action was performed in this audit.

## Decision

Keep this as a research candidate only. Before a build can be called reproducible, identify a compatible manifest and exact toolchain revision, audit the framework/vendor interfaces and blob provenance, and validate the output in an isolated environment. No ROM was built and no live device was accessed.
