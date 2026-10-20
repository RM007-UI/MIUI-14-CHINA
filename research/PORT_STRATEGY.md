# Recommended port strategy: MIUI 14 China features on Joyeuse

Review date: 2026-10-20  
Status: **strategy recommendation / not a build recipe**.

## Decision

First inspect the existing Joyeuse-only MIUI 14 China Android 13 port as a reference, because a community archive lists a build `V14.0.10.0.TLCCNXM` dated 2026-10-16 specifically for Joyeuse. The listing reports missing Setup Wizard and NFC issues; these claims have not been independently verified, and the build should not be assumed safe or suitable for daily use. Do not redistribute its package or blindly adopt it.

For our own reproducible engineering work, use an official MIUI 14 build for Redmi Note 9 Pro (`joyeuse`) as the device-specific baseline. Investigate China-region MIUI apps, resources, and framework customizations as a separate migration layer. Do not use the Xiaomi 12 (`cupid`) ROM as a direct base or copy its hardware images.

This avoids transplanting a Snapdragon 8 Gen 1 device's full Android 13 system onto Joyeuse's Snapdragon 720G platform and also gives us a target-specific community port to compare against.

## Evidence

- Xiaomi Community announced official Redmi Note 9 Pro Joyeuse MIUI 14 Global Stable `V14.0.3.0.SJZMIXM`, based on Android 12: https://c.mi.com/global/post/589058
- The official recovery package is indexed as `miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip`, around 2.7 GB, MD5 `df17e3fabf2284cc28efe8d10d012007`: https://mirom.ezbox.idv.tw/en/phone/joyeuse/
- Public community archive lists a Joyeuse-only MIUI 14 China `V14.0.10.0.TLCCNXM` Android 13 port dated 2026-10-16. Its listing reports missing Setup Wizard and NFC issues. These are community claims, not independent validation: https://t.me/s/Miatoll?q=%23a13
- Earlier community archives also document MIUI China Android 12 ports for the Miatoll family. These are historical precedent only, not proof of quality or compatibility across all variants: https://telegram.me/s/JoyeuseUpdates?q=%23Port
- The proposed Xiaomi 12 China donor is Android 13 and marked A/B, while Joyeuse is A-only. Its hardware partitions and vendor stack are incompatible assumptions for a direct port. See `CUPID_PAYLOAD_AUDIT.md`.

## Layer boundaries

### Preserve from the Joyeuse base

- Boot/recovery configuration and target-specific kernel strategy
- Joyeuse vendor/HAL blobs, firmware, modem, audio, camera, sensors, biometrics, NFC, and power configuration
- Target partition layout, AVB setup, fstab, init, and target-specific VINTF as validated for this device
- Existing target-specific compatibility and SELinux policy as the starting point

### Evaluate separately for migration from a China MIUI donor

- MIUI China system applications, overlays, resources, fonts, and region-specific configuration
- Framework and framework-extension components only after API/ABI and service dependency checks
- Privileged apps and permissions only with matching signatures/permissions and a clear dependency audit
- Region features, updater behavior, account services, Chinese input/fonts, and China-specific settings as independent tests

Do not assume that copying an APK or framework JAR is sufficient. MIUI components can depend on matching framework APIs, privileged permissions, signatures, native libraries, services, properties, and vendor interfaces.

## Work plan and acceptance gates

1. **Verify the base package.** Inspect the official Joyeuse MIUI 14 package metadata and payload manifest using HTTP ranges. Record package identity, OTA type, partitions, declared image sizes, and checksums from trustworthy metadata.
2. **Inventory the target.** Pin Joyeuse device tree, vendor blobs, kernel, firmware baseline, build tools, and a source manifest. Distinguish repository declarations from live device partition facts.
3. **Establish the baseline.** Build or reproduce the closest known-good Joyeuse configuration before modifying MIUI system components. Confirm a build host with sufficient free disk/RAM and retain logs.
4. **Inventory the China donor.** Identify an Android-version-compatible MIUI China donor. Extract only metadata/framework resources in a controlled workspace; do not transplant boot, vendor, modem, or firmware images.
5. **Compare components.** Audit framework APIs, native libraries, signatures, privileged permissions, VINTF/HAL, SELinux/property contexts, init services, and partition space.
6. **Integrate incrementally.** Keep each change isolated and reversible. Do not disable SELinux or bypass AVB as a generic workaround.
7. **Build without flashing.** Verify image formats, sizes against the actual target layout, AVB metadata, OTA/update packaging, and output hashes.
8. **Test only with a controlled recovery path.** First boot and hardware testing must be performed by someone with the appropriate device access and a verified backup/recovery procedure. A successful compile alone is not a boot test.

## Current blockers

- No connected, verified Android build host is available in this session; GitHub Actions has limited runner resources and is not a suitable full Android source-build host.
- The exact Joyeuse ROM has not yet been downloaded or hash-verified in this workspace. A metadata-inspection workflow has been added to this repository, but its run result must be checked before treating its findings as verified.
- No pinned, reproducible manifest proves the current candidate device tree, vendor tree, kernel and toolchain build together.
- The China donor's exact compatible release and migration scope remain undecided by evidence.
- Proprietary blob licensing/redistribution must be reviewed before publishing a ROM artifact.

## Explicit non-claims

No Joyeuse ROM image has been built, no image has been boot-tested, and no device partition has been modified. Do not label this project a working ROM or publish a flashable ZIP until the gates above have passed.
