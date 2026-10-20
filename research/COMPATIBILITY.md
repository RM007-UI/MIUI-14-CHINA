# Initial compatibility review: cupid → joyeuse

Status: **unverified / research only**. This document records known constraints; it is not a build recipe.

## Source candidate

- Device: Xiaomi 12 China (`cupid`)
- Candidate MIUI build: `V14.0.10.0.TLCCNXM`
- Android base reported by the public firmware index: Android 13
- Reference: https://github.com/XiaomiFirmwareUpdater/xiaomifirmwareupdater.github.io/blob/f3fd55eee00004d859cde590e446fabc4e93acc5/pages/miui/full/cupid.md
- Validation still required: package signature/origin, full package metadata, hashes from a trusted source, and confirmation that the selected package is the intended China stable release.

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

Do not build or install an image based on this information. The source package can guide UI/framework research, but a safe port needs a target-specific technical plan and verified device sources first. No phone-side commands should be run as part of this research stage.
