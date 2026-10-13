# Poster "Sớm thu chín đỏ một cành hồng" – Phương Anh (Nhã An nữ sĩ)

A4 dọc (2480×3508 px, 300 dpi), nền sơn mài tông sáng. Cành hồng nằm bên phải, chạy suốt 4 khổ thơ. Bên trái là 4 tranh minh hoạ cho 4 khổ. Tranh vẽ bằng PlenX (`gpt-image-2`), chữ đặt bằng code (font Charm, Be Vietnam Pro).

## Chạy trên máy

```bash
git clone https://github.com/toaducgreat/didi.git
cd didi
git checkout claude/adoring-hopper-qmzy4j
cd poster-tho-thu
pip install pillow numpy
python poster.py          # → final/tho-thu-canh-hong.{svg,png,pdf}
```

- Cần Chrome hoặc Edge để chụp SVG ra PNG. Script tự tìm trên Windows/macOS/Linux.
- Nếu script không tìm thấy trình duyệt, đặt biến môi trường `POSTER_CHROME` tới file chạy, ví dụ:
  - Windows: `set POSTER_CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe`
  - macOS: `export POSTER_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`

## Thư mục

| Đường dẫn | Nội dung |
|---|---|
| `poster.py` | Toàn bộ dàn trang: nền sơn mài, tách nền cành hồng, tiêu đề, 4 khổ thơ, chân trang, xuất file |
| `assets/anh-goc/` | 2 ảnh gốc anh gửi (ảnh 1 phòng, ảnh 2 cành hồng), bản thu nhỏ |
| `assets/canh-hong.jpg` | Cành hồng sơn mài vẽ lại theo ảnh 2 (bản mới, bình còn sai) |
| `assets/canh-hong-ban-cu.jpg` | Cành hồng bản đầu (AI tự vẽ, không giống ảnh, bỏ) |
| `assets/kho1..4-*.jpg` | Tranh 4 khổ |
| `fonts/` | Charm, Be Vietnam Pro, Playfair (đều có dấu tiếng Việt) |
| `final/` | Bản nháp gần nhất: đã thay cành hồng mới nhưng chưa dàn lại, nửa phải của bó cành còn bị cắt ra ngoài mép (xem Việc còn lại, mục 2) |

Lưu ý: mọi ảnh trong `assets/` hiện là bản xem trước 1024 px, vì môi trường cloud bị chặn tải từ `images.plenxai.com`. Trên máy, anh tải bản gốc (link bên dưới) rồi lưu đè đúng tên, đổi đuôi thành `.png` là được. `poster.py` tự nhận `.png`, `.jpg` và `.webp`, ưu tiên `.png`.

## Ảnh trên PlenX (bản đầy đủ, PNG)

Mẫu link: `https://images.plenxai.com/cdn-cgi/imagedelivery/kdQv2TNFsgg6nS5bfVdpTg/<id>/format=png,quality=100`

| File cần lưu | id ảnh | task_id |
|---|---|---|
| `canh-hong.png` (bản mới, bình sai) | `3c73e45d-6518-4152-d76b-432265e5c600` | `571281e5-fa7e-407d-aeab-a8aa93b603f5` |
| `kho1-phong.png` | `be43e629-f7f5-4f12-7c37-d5f712960900` | `2aabf380-…` |
| `kho2-thu-ha-noi.png` | `ef70e38e-a388-46a3-0740-ec36c455d200` | `1cb33c50-…` |
| `kho3-trang-thu.png` | `a2f7dd3f-1fa2-40d7-1a75-a744de9a0f00` | `675a3c26-…` |
| `kho4-truc.png` | `59b36cdc-f7a5-41cf-d937-b2a0d016e500` | `67efddda-…` |

**Job đang chạy dở:** sửa lại bình cho đúng ảnh gốc.
- task_id: `b418f564-6af1-41c1-a342-37a8439625c5`
- Anh mở trong lịch sử PlenX, hoặc hỏi Claude local `check_job` task này.
- Bình cần: thấp và rộng như cái chum, vai tròn, miệng ngắn và rộng, gốm đen nhám có vân chấm nổi (búa), không vẽ hoa vàng, đặt ngay dưới gốc cành.
- Ra đúng thì lưu thành `assets/canh-hong.png`.

## Việc còn lại

1. **Chọn bản cành hồng có bình đúng** (job ở trên). Nếu vẫn sai thì gọi lại `generate_image`:
   - model `gpt-image-2`, tỉ lệ 9:16, độ phân giải 4k
   - `references_urls` gồm 2 ảnh:
     1. bản cành hồng mới (`3c73e45d…`)
     2. ảnh gốc anh gửi: `https://images.plenxai.com/cdn-cgi/imagedelivery/kdQv2TNFsgg6nS5bfVdpTg/aae2cdd5-8727-4782-9cbb-99e3238b3300/format=jpeg,quality=100`
   - prompt "giữ nguyên mọi thứ, chỉ đổi bình theo ảnh 2".
2. **Dàn lại cành hồng trong `poster.py`.** Phần cần sửa ở mục `# persimmon branch`, các biến `bh`, `bx`, `by`.
   - Bản mới là cả bó cành cắm trong bình, rộng hơn bản cũ. Nên đặt bình ngay trên chân trang bên phải, khoảng `by + bh ≈ 3300`, và cho cành vươn lên tới khổ 1.
   - Thu gọn cho cả bó nằm trong khung, không cắt mất nhánh.
3. **Chữ đè lá.** Đã thêm quầng sáng kem mờ (`#halo`) sau mỗi khổ thơ. Render xong anh xem lại 2 câu "…sen nồng." và "…man mác".
4. **Render và kiểm tra.** Chạy `python poster.py`, so lại nguyên văn 16 câu thơ, rồi in thử.

Bài thơ được giữ nguyên văn trong biến `POEM` ở `poster.py`.
