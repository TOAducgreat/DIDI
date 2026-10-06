#!/usr/bin/env bash
# Tải tranh lụa tạo bằng PlenX (bản gốc + bản đã tách nền) về thư mục này.
# Cần mở mạng cho cdn.plenxai.com trong cấu hình môi trường cloud.
set -euo pipefail
cd "$(dirname "$0")"
get() { curl -sSfL -o "$1" "$2" && echo "ok  $1"; }
get dan-tranh.png      https://cdn.plenxai.com/plenxai/generated/20261006/5460260c-d0c1-499a-814b-f0df6d7cee6f_2k_e62689ba.png
get dan-tranh-cut.png  https://cdn.plenxai.com/images/3348d6de1e4e49aea3b8a6bffe442bd6.png
get xe-hoa.png         https://cdn.plenxai.com/plenxai/generated/20261006/a4537a7c-643e-4cd2-a512-f552c69f3fbb_2k_05ce27ad.png
get xe-hoa-cut.png     https://cdn.plenxai.com/images/bdde744a4812423faf98fca83d291a1a.png
get tra-sen.png        https://cdn.plenxai.com/plenxai/generated/20261006/9f28cb2e-b4f9-4d09-8e8d-4fcaa6d25ca3_2k_23f2a15c.png
get tra-sen-cut.png    https://cdn.plenxai.com/images/20f481b28eb24a768b0812a1b1c0503b.png
# Tranh 4k cho bản A (Hồ Gươm) và bản B (ban công phố cổ)
get ho-guom.png        https://cdn.plenxai.com/plenxai/images/20261006/nexo_d1eaef31-62d_914f5e89.png
get ban-cong.png       https://cdn.plenxai.com/plenxai/images/20261006/nexo_882dceaa-705_5b63fae8.png
