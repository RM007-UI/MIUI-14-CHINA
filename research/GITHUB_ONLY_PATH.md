# GitHub-only path for Joyeuse MIUI 14 China

Review date: 2026-10-20.

## Constraint

The project owner has only GitHub available: no local Linux workstation and no dedicated server. Standard GitHub-hosted runners are useful for metadata inspection, small scripts, tests, and validating archives, but are not a realistic environment for syncing and compiling the full Android platform plus device/vendor sources. A successful Actions run must not be described as a ROM build unless it actually produced and verified a ROM image.

## Practical approach

1. Treat the existing community Joyeuse-only MIUI 14 China Android 13 port as a reference candidate, not as a verified safe release.
2. Use GitHub Actions to inspect its public archive: record exact byte size and SHA-256, list ZIP entries, inspect recovery installer assertions and partition-writing commands, and publish only a text audit report.
3. Keep the ROM archive out of this repository and out of workflow artifacts. The workflow downloads it temporarily for inspection and removes it before the job ends.
4. Use audit results to decide whether it is actually Joyeuse-only and what image/partition layout it expects. Do not infer this from the filename alone.
5. Any future patch workflow should produce a small, reversible patch or metadata report rather than republishing proprietary ROM contents. Do not disable AVB or SELinux as a generic fix.
6. Never call the result a new custom ROM unless a changed, flashable image was actually produced. Never claim boot success without real device testing.

## Known candidate

A public community post lists MIUI 14.0.10.0.TLCCNXM - JOYEUSE ONLY, Android 13, build date 2026-10-16, maintainer kitagawa. The same post reports no Setup Wizard and NFC issues. These are community-reported notes, not independently verified facts.

Source listing: https://t.me/s/Miatoll?q=%23a13

The direct public mirror was reachable from the post, but the archive has not been independently authenticated. The audit workflow only inspects the archive and installer metadata; it does not flash, publish, or alter any phone.

## Workflow

- Audit workflow: https://github.com/RM007-UI/MIUI-14-CHINA/actions/workflows/audit-existing-joyeuse-port.yml
- Run history: https://github.com/RM007-UI/MIUI-14-CHINA/actions

## Limits

GitHub Actions cannot magically provide the hundreds of gigabytes of workspace normally needed for a full AOSP/Android source build on a standard hosted runner. This path can validate and analyze an existing Joyeuse-targeted ROM and build small supporting tools, but it is not a substitute for a full Android build host.
