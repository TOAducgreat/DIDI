#!/bin/bash
# Chỉnh màu hàng loạt cho cả thư mục video, lưu vào thư mục con mới.
# Mặc định: tăng sáng 2 nấc, giảm vàng 1 nấc, tăng màu (độ bão hoà) 1 nấc.
#
# Cách dùng (macOS, cần ffmpeg: brew install ffmpeg):
#   bash chinh_mau.sh "/Volumes/TeamVid_02/Đi ĐN 10.2026/Video"
#   bash chinh_mau.sh "<thư mục>" --test     # chỉ làm file đầu tiên, 5 giây, để duyệt màu
#
# Muốn mạnh/nhẹ hơn: sửa số nấc bên dưới (có thể dùng số lẻ, ví dụ 1.5).
SANG=2      # tăng sáng (số nấc)
VANG=-1     # âm = giảm vàng (ngả xanh), dương = tăng vàng
MAU=1       # tăng độ bão hoà màu
# Mỗi nấc tương ứng: sáng = gamma +0.06, vàng = kênh xanh dương +0.035, màu = bão hoà +10%

set -e
SRC="${1:?Thiếu đường dẫn thư mục video}"
TEST="$2"
OUT="$SRC/Da_chinh_mau"
mkdir -p "$OUT"

GAMMA=$(awk "BEGIN{print 1+0.06*$SANG}")
SAT=$(awk "BEGIN{print 1+0.10*$MAU}")
B=$(awk "BEGIN{print -0.035*$VANG}")
BH=$(awk "BEGIN{print -0.025*$VANG}")
VF="colorbalance=bs=$BH:bm=$B:bh=$BH,eq=gamma=$GAMMA:saturation=$SAT"
echo "Bộ lọc: $VF"
echo "Lưu vào: $OUT"

find "$SRC" -maxdepth 1 -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.mxf' -o -iname '*.mkv' \) ! -name '._*' -print0 | sort -z |
while IFS= read -r -d '' f; do
  name=$(basename "$f")
  dst="$OUT/$name"
  if [ "$TEST" = "--test" ]; then dst="$OUT/THU_$name"; fi
  if [ -e "$dst" ]; then echo "Bỏ qua (đã có): $name"; continue; fi
  vcodec=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$f")
  if [ "$vcodec" = "prores" ]; then
    ENC=(-c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le)
  else
    ENC=(-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p)
  fi
  LIM=()
  if [ "$TEST" = "--test" ]; then LIM=(-t 5); fi
  echo "Đang xử lý: $name"
  ffmpeg -nostdin -v error -y -i "$f" "${LIM[@]}" -map 0:v:0 -map 0:a? -vf "$VF" "${ENC[@]}" \
    -c:a copy -map_metadata 0 -movflags +faststart "$dst"
  if [ "$TEST" = "--test" ]; then echo "Xong bản thử: $dst"; break; fi
done
echo "Hoàn tất."
