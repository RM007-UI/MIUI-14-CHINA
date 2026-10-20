# Xiaomi 12 MIUI 14 payload metadata audit

Review date: 2026-10-20  
Status: **metadata verified from the OTA payload manifest; donor images are not target images**.

## Source identity

- Package: Xiaomi 12 China Stable Recovery ROM `V14.0.10.0.TLCCNXM`
- OTA source: `https://bigota.d.miui.com/V14.0.10.0.TLCCNXM/miui_CUPID_V14.0.10.0.TLCCNXM_9aa2f552b3_13.0.zip`
- Package length reported by the origin: 5,584,104,463 bytes (5.20 GiB)
- HTTP byte ranges: supported
- OTA metadata: `pre-device=cupid`, `post-sdk-level=33`, `ota-type=AB`, security patch `2023-11-01`, build `V14.0.10.0.TLCCNXM`
- Payload header: major version 2; manifest length 222,125 bytes; metadata signature length 267 bytes.
- Inspection method: read ZIP64 directory, package header/metadata and the payload manifest using small HTTP range requests. The full 5.20 GiB package was not downloaded.

## Declared new-image sizes

These sizes were parsed from `PartitionUpdate.new_partition_info` (protobuf field 7) and its nested size field. They describe the donor's update payload, not compatible target partition sizes.

| Partition | Declared image size (bytes) | Approx. MiB |
|---|---:|---:|
| abl | 204,800 | 0.20 |
| aop | 262,144 | 0.25 |
| aop_config | 16,384 | 0.02 |
| bluetooth | 1,830,912 | 1.75 |
| boot | 201,326,592 | 192.00 |
| cpucp | 155,648 | 0.15 |
| devcfg | 57,344 | 0.05 |
| dsp | 67,108,864 | 64.00 |
| dtbo | 25,165,824 | 24.00 |
| featenabler | 94,208 | 0.09 |
| hyp | 1,257,472 | 1.20 |
| imagefv | 6,299,648 | 6.01 |
| keymaster | 368,640 | 0.35 |
| modem | 278,949,888 | 266.00 |
| odm | 17,940,480 | 17.11 |
| product | 4,072,595,456 | 3,883.00 |
| qupfw | 53,248 | 0.05 |
| recovery | 104,857,600 | 100.00 |
| shrm | 69,632 | 0.07 |
| system | 790,605,824 | 753.76 |
| system_ext | 483,315,712 | 460.95 |
| tz | 3,801,088 | 3.62 |
| uefi | 2,760,704 | 2.63 |
| uefisecapp | 172,032 | 0.16 |
| vbmeta | 8,192 | 0.01 |
| vbmeta_system | 4,096 | 0.00 |
| vendor | 1,608,843,264 | 1,534.00 |
| vendor_boot | 100,663,296 | 96.00 |
| vendor_dlkm | 28,794,880 | 27.46 |
| vm-bootsys | 269,996,032 | 257.49 |
| xbl | 1,105,920 | 1.05 |
| xbl_config | 143,360 | 0.14 |
| xbl_ramdump | 811,008 | 0.77 |
| mi_ext | 28,672 | 0.03 |

## Interpretation

1. The source OTA identifies `cupid`, not `joyeuse`, and is marked A/B. Joyeuse is A-only according to the project target constraints. The donor package is **not a flashable Joyeuse ROM**.
2. Donor boot, recovery, vendor, firmware, modem, graphics, and other hardware-dependent images must not be transplanted to Joyeuse.
3. These measurements only establish what the donor payload declares. They do not establish Joyeuse partition capacities, target super layout, compatibility, signature validity, or bootability.
4. The more promising direction is to start from the official MIUI 14 ROM for Joyeuse itself, then separately assess whether China-region framework/apps/resources can be migrated without replacing target-specific kernel/vendor/firmware.
5. No full donor package download, extraction, build, phone query, or flash was performed.

## Reproducibility

- Corrected parser revision: `94c00b19372ba98229707d7896dfa33dc092c9e8`
- Successful GitHub Actions run: https://github.com/RM007-UI/MIUI-14-CHINA/actions/runs/39397618569
- The earlier run using protobuf field 4 was incorrect and is superseded by the successful field-7 parse.
