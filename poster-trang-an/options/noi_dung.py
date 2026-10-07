"""Nội dung 5 poster "Nét thanh lịch người Tràng An" (bản thông tin).

Vùng cắt ghi theo tỉ lệ (x0, y0, x1, y1) của tranh gốc trong assets/.
"""

# ảnh nhỏ: các chi tiết cận cảnh lấy từ 5 tranh lụa
D_HANDS = ("dan-tranh.png", (0.32, 0.59, 0.82, 0.87))     # tay trên phím đàn
D_LOTUS = ("dan-tranh.png", (0.00, 0.475, 0.45, 0.725))     # đầm sen
D_TREE = ("dan-tranh.png", (0.50, 0.30, 1.00, 0.58))      # cây cổ thụ, chim
T_LOTUS = ("tra-sen.png", (0.03, 0.38, 0.50, 0.645))       # sen cắm
T_VASE = ("tra-sen.png", (0.00, 0.525, 0.47, 0.785))        # bình sen men ngọc
T_POT = ("tra-sen.png", (0.22, 0.61, 0.63, 0.835))         # ấm trà, chén trà
T_GIRL = ("tra-sen.png", (0.50, 0.50, 0.97, 0.76))        # thiếu nữ nghiêng mình
X_GIRL = ("xe-hoa.png", (0.31, 0.46, 0.76, 0.71))         # áo dài, nón lá
X_DAISY = ("xe-hoa.png", (0.555, 0.575, 0.97, 0.805))        # giỏ cúc họa mi
X_LOTUS = ("xe-hoa.png", (0.035, 0.59, 0.45, 0.82))        # giỏ sen
X_SHUT = ("xe-hoa.png", (0.57, 0.38, 1.00, 0.62))         # cửa chớp xanh
H_TOWER = ("ho-guom.png", (0.50, 0.40, 0.90, 0.80))       # Tháp Rùa
H_GIRL = ("ho-guom.png", (0.12, 0.42, 0.52, 0.82))        # thiếu nữ bên hồ
H_WILLOW = ("ho-guom.png", (0.00, 0.24, 0.45, 0.69))      # rặng liễu
H_MOON = ("ho-guom.png", (0.44, 0.24, 0.84, 0.64))        # trăng, mây
B_FLOWER = ("ban-cong.png", (0.40, 0.44, 0.80, 0.84))     # hoa giấy
B_GIRL = ("ban-cong.png", (0.16, 0.38, 0.52, 0.74))       # thiếu nữ tưới hoa
B_ROOF = ("ban-cong.png", (0.58, 0.60, 0.98, 1.00))       # mái ngói
B_RAIL = ("ban-cong.png", (0.00, 0.30, 0.38, 0.68))       # cửa chớp, lan can

SPECS = {
    "0": dict(
        name="0-mac-nguyet", no="Nº 01", hero=("dan-tranh.png", (0.0, 0.46, 1.0, 0.76)), hero_w=1700,
        bottom=(241, 222, 218),
        theme="Thanh lịch trong tâm hồn",
        lead="Người Tràng An thanh lịch từ bên trong: một tâm hồn biết lắng nghe, biết rung động trước cái đẹp giản dị.",
        items=[
            ("Tiếng đàn dân tộc", D_HANDS,
             "Tiếng đàn tranh, đàn bầu từng vang lên trong nhiều nếp nhà Hà Nội. Học đàn, nghe đàn là cách "
             "người xưa nuôi dưỡng sự tinh tế và lòng kiên nhẫn."),
            ("Hương sen thanh khiết", T_LOTUS,
             "Sen Hồ Tây gần bùn mà chẳng hôi tanh mùi bùn. Người Hà Nội yêu sen như yêu một phẩm cách: "
             "trong sạch, khiêm nhường, toả hương mà không phô trương."),
            ("Lời thơ, câu ca", H_WILLOW,
             "Ca dao, thơ phú thấm vào lời ăn tiếng nói hằng ngày. Nói có văn, có ý mà vẫn mềm mỏng "
             "là nét duyên riêng của người Kẻ Chợ."),
            ("Sống chậm, nghĩ sâu", T_GIRL,
             "Thanh lịch là biết dừng lại: ngắm một mùa hoa, nhấp một chén trà, suy xét trước khi nói. "
             "Sự điềm tĩnh ấy làm nên chiều sâu của người Hà Nội."),
        ]),
    "A": dict(
        name="A-ho-guom", no="Nº 02", hero=("ho-guom.png", (0.0, 0.28, 1.0, 0.76)), hero_w=1900,
        bottom=(222, 228, 234),
        theme="Trái tim nghìn năm",
        lead="Hồ Gươm là nơi lịch sử, truyền thuyết và nhịp sống đời thường của Hà Nội gặp nhau.",
        items=[
            ("Truyền thuyết trả gươm", H_TOWER,
             "Tương truyền vua Lê Lợi trả thanh gươm thần cho Rùa Vàng sau khi đánh thắng giặc Minh. "
             "Từ đó hồ Lục Thủy mang tên Hồ Hoàn Kiếm."),
            ("Tà áo bên hồ", X_GIRL,
             "Tà áo dài trắng bên mặt hồ đã thành hình ảnh quen thuộc của Thủ đô. Vẻ đẹp ấy kín đáo, "
             "dịu dàng mà vẫn rạng rỡ."),
            ("Dạo hồ sớm mai", D_TREE,
             "Mỗi sớm, người Hà Nội đi bộ quanh hồ, chào nhau bằng nụ cười và lời hỏi thăm nhẹ nhàng. "
             "Nhịp sống chậm rãi ấy mở đầu một ngày thanh thản."),
            ("Giữ gìn cảnh đẹp chung", B_FLOWER,
             "Không xả rác, không bẻ cây hái hoa, nói khẽ nơi công cộng. Người Tràng An trân trọng "
             "không gian chung như chính ngôi nhà mình."),
        ]),
    "B": dict(
        name="B-pho-co", no="Nº 03", hero=("ban-cong.png", (0.0, 0.30, 1.0, 0.78)), hero_w=1900,
        bottom=(240, 224, 210),
        theme="Nếp nhà phố cổ",
        lead="Trong những ngôi nhà ống mái ngói rêu phong, nếp sống thanh lịch được giữ gìn qua nhiều thế hệ.",
        items=[
            ("Ba mươi sáu phố phường", B_ROOF,
             "Mỗi con phố mang tên một nghề: Hàng Bạc, Hàng Đào, Hàng Mã… Người phố cổ buôn bán "
             "thật thà, giữ chữ tín như giữ nếp nhà."),
            ("Nếp nhà ngăn nắp", X_SHUT,
             "Cửa chớp xanh, ban công nhỏ, góc nhà luôn sạch sẽ, gọn gàng. Người Hà Nội xưa coi trọng "
             "sự chỉn chu từ những điều nhỏ nhất trong gia đình."),
            ("Lời ăn tiếng nói", H_GIRL,
             "“Lời nói chẳng mất tiền mua, lựa lời mà nói cho vừa lòng nhau.” Thưa gửi lễ phép, nói năng "
             "từ tốn là điều trẻ em phố cổ được dạy từ thuở nhỏ."),
            ("Tình làng nghĩa xóm", X_DAISY,
             "Hàng xóm sẻ chia nhau gánh hoa, bát canh, lúc vui lúc buồn. Sự tử tế và tế nhị trong "
             "cư xử làm nên nét ấm áp của khu phố."),
        ]),
    "C": dict(
        name="C-xe-hoa", no="Nº 04", hero=("xe-hoa.png", (0.075, 0.50, 0.927, 0.82)), hero_w=1700,
        bottom=(242, 230, 204),
        theme="Áo dài & gánh hoa",
        lead="Từ tà áo dài đến gánh hoa rong, cái đẹp của Hà Nội hiện lên trong từng chi tiết đời thường.",
        items=[
            ("Tà áo dài thướt tha", B_GIRL,
             "Áo dài là trang phục của sự kín đáo và duyên dáng. Người Hà Nội mặc áo dài không để khoe, "
             "mà để tỏ lòng tôn trọng chính mình và người đối diện."),
            ("Hoa theo mùa", T_VASE,
             "Sen tháng Năm, hoa sữa tháng Mười, cúc họa mi đầu đông, đào ngày Tết. Người Hà Nội "
             "đón mùa qua từng gánh hoa, nâng niu vẻ đẹp chóng qua của đất trời."),
            ("Chỉn chu, gọn gàng", T_GIRL,
             "Ra đường quần áo tề chỉnh, đầu tóc gọn gàng, nhà cửa sạch sẽ. Sự chỉn chu ấy là cách "
             "người Tràng An thể hiện văn hoá của mình."),
            ("Hoa ngày rằm", D_LOTUS,
             "Rằm và mồng một, nhà nhà mua một bó hoa tươi dâng lên bàn thờ tổ tiên. Thói quen nhỏ ấy "
             "giữ cho nếp nhà luôn ấm áp và thành kính."),
        ]),
    "D": dict(
        name="D-tra-sen", no="Nº 05", hero=("tra-sen.png", (0.0, 0.50, 1.0, 0.80)), hero_w=1700,
        bottom=(224, 233, 224),
        theme="Thú thưởng trà",
        lead="Một chén trà sen thơm là cả một nghệ thuật sống chậm của người Hà Nội.",
        items=[
            ("Ướp trà sen Tây Hồ", D_LOTUS,
             "Trà ngon được ướp trong hoa sen Bách Diệp của Hồ Tây, mỗi cân trà cần hàng nghìn bông sen. "
             "Sự kỳ công ấy cho thấy cái “sành” của người Hà Nội."),
            ("Chén trà mời khách", T_POT,
             "Khách đến nhà, chủ pha ấm trà nóng, rót mời bằng hai tay. Chén trà là lời chào trân trọng, "
             "mở đầu cho câu chuyện thân tình."),
            ("Lễ nghi nếp nhà", B_RAIL,
             "Con cháu kính trên nhường dưới, mời ông bà trước khi dùng bữa. Những lễ nghi giản dị ấy "
             "được giữ gìn như một phần của gia phong."),
            ("Thong thả, an nhiên", H_MOON,
             "Ngồi bên chén trà, ngắm trăng lên, nghe tiếng chim hót, người Hà Nội tìm thấy sự an nhiên "
             "giữa phố phường tấp nập."),
        ]),
}
