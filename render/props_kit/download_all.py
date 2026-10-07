#!/usr/bin/env python3
"""Tai het video + anh prop 3D vao thu muc ./props_download (chay: python3 download_all.py)."""
import os, sys, urllib.request
FILES = [
 [
  "videos/01_cang_bien.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_610ea37be154_579b0d3c.mp4"
 ],
 [
  "images/01_cang_bien.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_3440427f-3e8_21d2fe2c.png"
 ],
 [
  "videos/02_diem_kiem_tra_hai_quan.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_de9491e89f55_106b0758.mp4"
 ],
 [
  "images/02_diem_kiem_tra_hai_quan.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_609d6969-b12_eccdb0dc.png"
 ],
 [
  "videos/03_khoi_kinh_xe_qua_cong_quet.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_94f0924a40f2_50f01b97.mp4"
 ],
 [
  "images/03_khoi_kinh_xe_qua_cong_quet.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_e5663839-56e_8c988216.png"
 ],
 [
  "videos/04_cua_khau.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_8b5551536d80_eae58ce6.mp4"
 ],
 [
  "images/04_cua_khau.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_0457314e-e11_292826fa.png"
 ],
 [
  "videos/05_ba_hexagon.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_7cedff0a0420_3a29112b.mp4"
 ],
 [
  "images/05_ba_hexagon.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_71fca698-b63_a492411f.png"
 ],
 [
  "videos/06_bac_thang_sach_luat.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_e43195abf029_5af038a1.mp4"
 ],
 [
  "images/06_bac_thang_sach_luat.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_3d2d5db5-378_73809c06.png"
 ],
 [
  "images/07_ho_so_laptop.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_f51cd779-395_683ff20b.png"
 ],
 [
  "videos/08_hai_to_thu.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_c1386eca1429_3ee3cd6d.mp4"
 ],
 [
  "images/08_hai_to_thu.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_38868087-a63_aadf0474.png"
 ],
 [
  "videos/09_can_bo_ngoi_ban.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_9bfe61fff78c_d600ede2.mp4"
 ],
 [
  "images/09_can_bo_ngoi_ban.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_e514c840-dd9_4ad6c62e.png"
 ],
 [
  "videos/10_may_chu_mot_cua.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_13b546637e5f_7e5e760d.mp4"
 ],
 [
  "images/10_may_chu_mot_cua.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_75bbdbd2-376_a5952f26.png"
 ],
 [
  "videos/11_san_bay_cho_nghiep_vu.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_e6938a2ce229_5ec9c1fb.mp4"
 ],
 [
  "images/11_san_bay_cho_nghiep_vu.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_2126db5e-d44_80d5681e.png"
 ],
 [
  "videos/12_tau_container.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_d9025a7299c2_2889d3cd.mp4"
 ],
 [
  "images/12_tau_container.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_5e4cc9e9-724_8e6bfd86.png"
 ],
 [
  "videos/13_trung_tam_logistics.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_531a311fc7d7_163802fa.mp4"
 ],
 [
  "images/13_trung_tam_logistics.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_4ff2eebd-3e6_ffb3abae.png"
 ],
 [
  "videos/14_ben_container_cau_vang.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_9bacc2811b68_69153ffb.mp4"
 ],
 [
  "images/14_ben_container_cau_vang.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_3e3c8cc1-499_15a1e34f.png"
 ],
 [
  "videos/15_dam_may_buc.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_609ae84786bd_00e37238.mp4"
 ],
 [
  "images/15_dam_may_buc.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_9005c4ca-3bb_cc3a333f.png"
 ],
 [
  "videos/16_thap_may_chu_cot_bieu_do.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_e9982c09ec35_b6cd03ec.mp4"
 ],
 [
  "images/16_thap_may_chu_cot_bieu_do.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_26cfbc3b-da3_946dffc4.png"
 ],
 [
  "videos/17_vong_laptop.mp4",
  "https://cdn.plenxai.com/plenxai/videos/omni-vids/20261007/omni_vids_1080p_2d846a2893a5_395210fc.mp4"
 ],
 [
  "images/17_vong_laptop.png",
  "https://cdn.plenxai.com/plenxai/images/20261007/nexo_6a9e8c05-c32_7fc848a5.png"
 ]
]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "props_download")
ok = fail = 0
for rel, url in FILES:
    dst = os.path.join(base, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print("da co  ", rel); ok += 1; continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as f:
            f.write(r.read())
        print("da tai ", rel); ok += 1
    except Exception as e:
        print("LOI    ", rel, e); fail += 1
print(f"Xong: {ok} file, loi: {fail}. Thu muc: {base}")
sys.exit(1 if fail else 0)
