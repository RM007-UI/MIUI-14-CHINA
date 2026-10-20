# Official Joyeuse MIUI 14 base package audit

Review date: 2026-10-20  
Status: **package metadata read from the remote archive; no full ROM download or image extraction performed**.

## Package identity

- Device: Redmi Note 9 Pro, codename `joyeuse`
- Region: Global
- Version: `V14.0.3.0.SJZMIXM`
- Android: 12 / SDK 31
- Security patch: 2023-02-01
- Build fingerprint metadata: `Redmi/joyeuse_global/joyeuse:12/RKQ1.211019.001/V14.0.3.0.SJZMIXM:user/release-keys`
- OTA metadata says `pre-device=joyeuse`, `ota-type=BLOCK`, and `ota-required-cache=0`.
- Package size reported by origin: 2,890,193,683 bytes (2.69 GiB)
- ZIP directory: 39 entries, central-directory size 2,807 bytes.
- Package listing reports MD5 `df17e3fabf2284cc28efe8d10d012007`. This is an index-provided value, not a hash independently calculated by this workflow.
- Source listing: https://mirom.ezbox.idv.tw/en/phone/joyeuse/
- Official release announcement: https://c.mi.com/global/post/589058
- Archive URL: `https://bigota.d.miui.com/V14.0.3.0.SJZMIXM/miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip`

## ZIP inventory observed by successful CI run

The workflow inspected the central directory using HTTP byte ranges and did not fetch the full 2.69 GiB archive. The inventory declares these entries:

| Entry | Uncompressed size (bytes) | Notes |
|---|---:|---|
| `product.new.dat.br` | 684,641,264 | Compressed block-based product image data |
| `system.new.dat.br` | 1,451,119,470 | Compressed block-based system image data |
| `system_ext.new.dat.br` | 221,645,394 | Compressed block-based system_ext image data |
| `vendor.new.dat.br` | 440,014,892 | Compressed block-based vendor image data |
| `boot.img` | 134,217,728 | Target-specific boot image; not extracted |
| `firmware-update/dtbo.img` | 8,388,608 | Target-specific DTBO; not extracted |
| `firmware-update/vbmeta.img` | 4,096 | Target AVB metadata; not extracted |
| `firmware-update/vbmeta_system.img` | 4,096 | Target AVB metadata; not extracted |
| `dynamic_partitions_op_list` | 857 | Logical partition operation description |
| `system.transfer.list` | 13,312 | Transfer map for block-based system image |
| `system_ext.transfer.list` | 2,587 | Transfer map for block-based system_ext image |
| `product.transfer.list` | 20,531 | Transfer map for block-based product image |
| `vendor.transfer.list` | 5,027 | Transfer map for block-based vendor image |
| `META-INF/com/google/android/updater-script` | 5,219 | Recovery installer script |
| `META-INF/com/google/android/update-binary` | 2,367,032 | Recovery installer binary |

The full inventory also includes Qualcomm firmware update payloads such as `NON-HLOS.bin`, `BTFM.bin`, `abl.elf`, `aop.mbn`, `dspso.bin`, `hyp.mbn`, `tz.mbn`, and `xbl.elf`. These are listed as metadata only. The workflow did not extract, inspect, or flash them.

**Important:** These are sizes declared in the official Joyeuse package's ZIP directory, not the sizes of a custom port. Do not use this inventory as permission to flash, repack, or mix Global and China ROM components.

## Parser correction

The recovery ZIP does **not** contain `payload.bin`. It declares `ota-type=BLOCK`, so it is not structured like the payload-based `cupid` archive. The first CI attempt correctly read the package metadata but failed because the generic parser incorrectly assumed every recovery ZIP contains `payload.bin`. The Joyeuse workflow has been updated to handle this package type by reporting the ZIP inventory instead of failing.

## What this proves — and does not prove

- It verifies that the selected remote archive metadata identifies the official Joyeuse Global MIUI 14 Android 12 package.
- It does not verify the downloaded package's signature or checksum, because the full package was not downloaded.
- It does not establish a compatible Android 13 China build or the final target partition layout.
- It does not mean the Global package should be flashed to or repackaged for a different device; it is a reference for target-specific framework and device configuration.
- The more directly relevant engineering reference is the community listing for a Joyeuse-only MIUI 14 China Android 13 port, but that listing reports bugs and has not been independently tested by this project: https://t.me/s/Miatoll?q=%23a13

No source image was extracted, no image was built, and no device partition was modified.
