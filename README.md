# MIUI 14 China Android 13 — Joyeuse research workspace

> **Status: research and compatibility work only. No ROM image has been built or boot-tested in this repository.**

Goal: assess a MIUI 14 China Android 13 build for Redmi Note 9 Pro (**joyeuse**, A-only).

## Current direction

The first hypothesis was to adapt Xiaomi 12 China `cupid` `V14.0.10.0.TLCCNXM`. Its OTA metadata has now been parsed successfully, but that package is marked A/B and targets different hardware. Its boot, vendor, firmware, modem, and other hardware-dependent images are **not** for Joyeuse.

The project has therefore pivoted to the safer and more realistic path:

1. Use Joyeuse-specific MIUI as the device baseline, and verify its package metadata.
2. Audit public Joyeuse-only MIUI China ports as engineering references.
3. Keep kernel, vendor, firmware, partition layout, AVB, and device-specific hardware configuration target-specific.
4. Do not label any output as flashable until a real build, image/partition checks, and controlled device testing are complete.

## Important new research findings

- Xiaomi officially released Joyeuse MIUI 14 Global `V14.0.3.0.SJZMIXM`, based on Android 12. This is a target-device reference, not the China build itself.
- Community archives list MIUI 14 China Android 13 ports for Joyeuse/Miatoll, including a recent Joyeuse-only `V14.0.10.0.TLCCNXM) post. That post reports bugs (including missing Setup Wizard and NFC); its claims are not independently verified here. Treat it as an upstream reference, not a proven daily-driver recommendation.
- The Xiaomi 12 source package metadata audit is recorded in [`research/CUPID_PAYLOAD_AUDIT.md`](research/CUPID_PAYLOAD_AUDIT.md).
- The recommended porting and verification gates are recorded in [`research/PORT_STRATEGY.md`](research/PORT_STRATEGY.md).

## Automated metadata checks

- [Inspect Joyeuse MIUI 14 base](https://github.com/RM007-UI/MIUI-14-CHINA/actions/workflows/inspect-joyeuse-base.yml)
- [Inspect Xiaomi 12 cupid source](https://github.com/RM007-UI/MIUI-14-CHINA/actions/workflows/inspect-cupid-source.yml)
- [All workflow runs](https://github.com/RM007-UI/MIUI-14-CHINA/actions)

The Joyeuse workflow reads package metadata and payload declarations through HTTP byte ranges; it is not a ROM builder. Check its latest run before relying on any output.

## Build constraints

A full Android build requires a suitable, measured Linux x86_64 host and a reproducible set of platform, device-tree, vendor, kernel, firmware, and toolchain revisions. The current GitHub Actions runner is suitable for short metadata checks, not a full Android source build. No connected build host is available in this session.

## Safety boundaries

- No automatic ADB/Fastboot, erase, format, partition-write, or flashing actions.
- Never flash the `cupid` donor's boot/vendor/firmware images to Joyeuse.
- Never lock the bootloader while using a non-stock system.
- Do not upload proprietary ROM images or personal device backups.
- A passing workflow means only that that workflow's checks passed. It does not prove a ROM builds, boots, or is safe to install.

## Research references

- [Xiaomi Community: official Joyeuse MIUI 14 Global release](https://c.mi.com/global/post/589058)
- [Joyeuse MIUI firmware index](https://mirom.ezbox.idv.tw/en/phone/joyeuse/)
- [Miatoll community archive: MIUI 14 China Android 13 port listing](https://t.me/s/Miatoll?q=%23a13)
- [XiaomiFirmwareUpdater: cupid V14.0.10.0.TLCCNXM index](https://github.com/XiaomiFirmwareUpdater/xiaomifirmwareupdater.github.io/blob/f3fd55eee00004d859cde590e446fabc4e93acc5/pages/miui/full/cupid.md)

