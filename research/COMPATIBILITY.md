# Compatibility review: MIUI 14 China on Joyeuse

Status: **unverified / research only**. This document records known constraints; it is not a build recipe. A Joyeuse-only MIUI 14 China Android 13 community port is listed publicly, but this project has not verified its package or tested its reported behavior.

## Relevant source candidates

- Target-specific base: official Joyeuse Global MIUI 14 `V14.0.3.0.SJZMIXM`, Android 12. Its remote metadata is recorded in `JOYEUSE_BASE_AUDIT.md`; the full package has not been downloaded or hash-verified in this workspace.
- China reference: community archive lists a Joyeuse-only MIUI 14 China `V14.0.10.0.TLCCNXM` Android 13 port dated 2026-10-16. The listing reports missing Setup Wizard and NFC issues; these claims are not independently verified. Reference: https://t.me/s/Miatoll?q=%23a13
- Original cross-device donor: Xiaomi 12 China `cupid` `V14.0.10.0.TLCCNXM`, Android 13. The package manifest has been parsed, but it is A/B and targets different hardware. See `CUPID_PAYLOAD_AUDIT.md`. It is not a direct flashing source.

## Target candidate sources

- Device: Redmi Note 9 Pro `joyeuse`
- Public device-tree lead: https://github.com/AOSP-joyeuse/platform_device_xiaomi_joyeuse
- That repository labels the tree work-in-progress and appears old. It cannot be treated as a complete or current foundation without reviewing its branches, commits, kernel, vendor dependencies, and build configuration.

## Compatibility questions — unresolved

| Area | Why it matters | Status |
|---|---|---|
| SoC / graphics | `cupid` and `joyeuse` are different hardware platforms; source blobs and graphics stack are not drop-in compatible | Unresolved |
| Kernel / modules | Kernel interfaces and vendor modules must match the target hardware and Android vendor interface | Unresolved |
| Vendor / firmware | Modem, camera, sensors, audio, biometrics and power depend on target-specific components | Unresolved |
| Partition layout | Source package layout cannot be copied blindly to the target | Unresolved |
| SELinux / init / services | Device-specific policy and service configuration need review | Unresolved |
| Boot and recovery | No validated boot/recovery strategy exists yet | Unresolved |

## Decision

Do not build or install an image based on this information alone. Prefer the target-specific Joyeuse base and use the existing China port only as a comparison/reference until its provenance, integrity, bugs, and compatibility are reviewed. A safe custom port still needs a reproducible source manifest, a verified build host, and target-specific compatibility checks. No phone-side commands should be run as part of this research stage.
