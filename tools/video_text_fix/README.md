# video_text_fix

Công cụ sửa chữ trên mũ / bảng tên trong clip AI và dựng clip theo voice chuẩn
(dùng cho Phim hải quan – S07: 3 cỡ cảnh Toàn / Trung / Cận, mỗi cỡ 2 clip 10s).

## Quy trình

1. **Tracking** – `track.py cfg_X.json trk_X.json`: bám chuyển động vùng mũ và bảng tên
   bằng OpenCV ECC (affine), trả về ma trận cho từng khung.
2. **Sửa chữ** – `fix.py`: mỗi khung xoá chữ cũ trong vùng đã bám (inpaint hoặc
   phủ màu nền + hạt), rồi vẽ chữ mới:
   - `glyphpart`: chỉ thay dấu (HÀI → HẢI ở cảnh Cận).
   - `arc3`: chữ "HẢI QUAN VIỆT NAM" chạy theo cung tròn qua 3 điểm chân chữ (Trung, Toàn).
   - `line`: chữ thẳng (bảng tên "MINH CHÂU" ở cảnh Cận).
   - `plate`: dán bảng tên mẫu (`plate.py` lấy từ cảnh Cận 1 đã sửa) theo 4 góc
     bảng tên ở cảnh Trung / Toàn.
   - Xem trước: `python3 fix.py C1 0,5,9.8 x0,y0,x1,y1 <track>` → `prev_*.jpg`.
3. **Căn voice** – `timemap.py`: DTW trên MFCC giữa âm thanh từng clip và voice chuẩn,
   làm mượt, giới hạn tốc độ 0.8–1.25x → `timemap.json`.
4. **Xuất** – `render_out.py Toan|Trung|Can`: nửa đầu voice (0–9.48s) lấy clip 1,
   nửa sau lấy clip 2, chọn khung theo bảng thời gian, sửa chữ, ghép voice chuẩn,
   xuất H.264 4K 24fps.

Chạy trong thư mục chứa clip đã đổi tên `T1 T2 M1 M2 C1 C2 .mp4/.wav`, `voice.mp3/.wav`
và các file `cfg_*.json` (trong `configs/`).

Phụ thuộc: `ffmpeg`, `numpy scipy opencv-python-headless pillow librosa`,
font Liberation Sans Bold.
