```mermaid
flowchart TD
    %% =========================================================================
    %% BẢNG MÀU PHONG CÁCH ĐỊNH NGHĨA TOÀN CẢNH (GLOBAL COLOR SYSTEM)
    %% =========================================================================
    classDef ancient fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#000;
    classDef bth fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
    classDef monarch fill:#fffbeb,stroke:#b45309,stroke-width:2px,color:#000;
    classDef victory fill:#dcfce7,stroke:#16a34a,stroke-width:2px,font-weight:bold,color:#000;
    classDef war fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#000;
    classDef crisis fill:#f1f5f9,stroke:#64748b,stroke-width:2px,color:#000;
    classDef mac fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#000;
    classDef le_th fill:#fdf4ff,stroke:#c026d3,stroke-width:2px,color:#000;
    classDef trinh fill:#f1f5f9,stroke:#475569,stroke-width:2px,color:#000;
    classDef nguyen fill:#fffbeb,stroke:#b45309,stroke-width:2px,color:#000;
    classDef ts fill:#fef2f2,stroke:#b91c1c,stroke-width:2px,color:#000;
    classDef qt fill:#fee2e2,stroke:#991b1b,stroke-width:3px,font-weight:bold,color:#000;
    classDef campaign fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000;
    classDef treaty fill:#f8fafc,stroke:#475569,stroke-width:2px,color:#000;
    classDef hero fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#000;
    classDef modern fill:#f0fdf4,stroke:#059669,stroke-width:2px,font-weight:bold,color:#000;

    %% =========================================================================
    %% 1. THỜI KỲ DỰNG NƯỚC: HỒNG BÀNG, VĂN LANG & ÂU LẠC (2879 TCN - 179 TCN)
    %% =========================================================================
    subgraph Sub1_HongBang ["1. KỶ HỒNG BÀNG & NƯỚC ÂU LẠC (2879 TCN - 179 TCN)"]
        HB_ORIGIN["KHỞI NGUYÊN DÂN TỘC & TIỀN SỬ (Trước 2879 TCN):<br>Các nền văn hóa Núi Đọ, Sơn Vi, Hòa Bình, Phùng Nguyên<br>Truyền thuyết Đế Minh chia cõi phương Nam cho con thứ Lộc Tục"]:::ancient
        -->|"2879 TCN: Lộc Tục xưng Kinh Dương Vương lập nước Xích Quỷ"| HB_KDV["Kinh Dương Vương (Lộc Tục)<br>2879 TCN - ?<br>Lập nước XÍCH QUỶ"]:::ancient
        --> HB_LLQ["Lạc Long Quân & Âu Cơ<br>Truyền thuyết Con Rồng Cháu Tiên<br>Mẹ Âu Cơ sinh bọc trăm trứng nở trăm con"]:::ancient
        --> HB_HV["18 Đời Hùng Vương (Lạc Việt)<br>Khoảng Tk VII TCN - 258 TCN<br>Quốc hiệu VĂN LANG - Đô: Phong Châu (Phú Thọ)"]:::ancient

        HB_E["Văn hóa Đông Sơn rực rỡ<br>Đúc Trống đồng Ngọc Lũ, Hoàng Hà<br>Nền văn minh lúa nước sông Hồng"]:::ancient
        HB_HV -.-> HB_E

        TAYAU_TP["Thục Phán (Thủ lĩnh Tây Âu / Âu Việt)<br>Địa bàn miền núi Việt Bắc - Cao Bằng"]:::ancient

        HB_HV -.->|"Thế kỷ III TCN: Văn Lang suy yếu cuối thời Hùng Duệ Vương"| WAR_258BC["CHIẾN TRANH ÂU - LẠC & HỢP NHẤT DÂN TỘC (258 TCN):<br>Thục Phán tiến đánh Văn Lang, Hùng Vương nhường ngôi hợp nhất cộng đồng"]:::war
        TAYAU_TP --> WAR_258BC

        WAR_258BC -->|"Thục Phán hợp nhất Âu Việt & Lạc Việt, xưng An Dương Vương"| AL_ADV["An Dương Vương (Thục Phán)<br>257 TCN - 179 TCN<br>Quốc hiệu ÂU LẠC - Đô: Cổ Loa (Đông Anh, Hà Nội)"]:::ancient
        
        AL_E["Xây dựng Thành Cổ Loa 9 vòng xoáy trôn ốc<br>Tướng Cao Lỗ chế tạo nỏ thần liên châu 'Lạc Quang thần nỏ'"]:::ancient
        AL_ADV -.-> AL_E

        AL_ADV --> TAYAU_QTAN["Kháng chiến chống 50 vạn quân Tần (218 - 208 TCN):<br>An Dương Vương lãnh đạo chung Âu - Lạc, đánh du kích giết Đồ Thư đại phá quân Tần"]:::victory
    end

    %% =========================================================================
    %% 2. THỜI KỲ BẮC THUỘC & ĐẤU TRANH ĐỘC LẬP (179 TCN - 938 SCN)
    %% =========================================================================
    subgraph Sub2_BacThuoc ["2. THỜI KỲ BẮC THUỘC & ĐẤU TRANH ĐỘC LẬP (179 TCN - 938)"]
        TRIEU_T1["Nhà Triệu (207 TCN - 111 TCN) - Triệu Vũ Đế (Triệu Đà)<br>207 TCN - 137 TCN | Nước Nam Việt (Phiên Ngung)"]:::bth
        -->|"111 TCN: Nhà Hán thôn tính Nam Việt, mở đầu thời kỳ Bắc thuộc lần 1"| KN_TRUNG["Khởi nghĩa Hai Bà Trưng (40 - 43 SCN)<br>Trưng Trắc & Trưng Nhị - Đô: Mê Linh<br>'Một xin rửa sạch nước thù, Hai xin đem lại nghiệp xưa họ Hùng'"]:::victory
        -->|"Năm 43 SCN: Mã Viện đàn áp đẫm máu; Bắc thuộc lần 2"| KN_TRIEU["Khởi nghĩa Bà Triệu (Triệu Thị Trinh - 248 SCN)<br>'Đạp luồng sóng dữ, chém cá kình ở biển Đông' chống quân Đông Ngô"]:::war
        -->|"542 - 544: Lý Bí phất cờ khởi nghĩa đánh đuổi thứ sử Tiêu Tư"| VX_LYND["LÝ NAM ĐẾ (LÝ BÍ) - NƯỚC VẠN XUÂN (544 - 548):<br>Dựng điện Vạn Thọ, niên hiệu Thiên Đức, đúc tiền riêng, dựng chùa Khai Quốc (Trấn Quốc)"]:::victory

        %% Song song thời kỳ Vạn Xuân phân liệt: Triệu Việt Vương vs Lý Phật Tử
        subgraph Sub2_VanXuanSplit ["CỤC DIỆN PHÂN TRANH NƯỚC VẠN XUÂN (548 - 602)"]
            VX_TVV["TRIỆU VIỆT VƯƠNG (TRIỆU QUANG PHỤC: 548 - 571):<br>Kế thừa binh quyền của Lý Nam Đế; lui về đầm Dạ Trạch đánh du kích.<br>Năm 550: Nhân lúc Trần Bá Tiên về bắc, tổng phản công thu phục Long Biên"]:::victory
            VX_LPT["ĐÀO LANG VƯƠNG & LÝ PHẬT TỬ (548 - 602):<br>Lý Thiên Bảo cùng Lý Phật Tử chạy vào Cửu Chân lập nước Dã Năng.<br>Thiên Bảo mất, Lý Phật Tử nối quyền xưng vương"]:::crisis

            VX_TVV -.->|"557: Lý Phật Tử đem quân đánh Triệu Quang Phục; hai bên bất phân thắng bại, chia đất tại bãi Quần Đầu"| VX_LPT
            VX_LPT -->|"571: Lý Phật Tử dùng kế thông gia gả con đánh úp Triệu Quang Phục, xưng Hậu Lý Nam Đế"| VX_HLY["Hậu Lý Nam Đế (Lý Phật Tử: 571 - 602)<br>Đóng đô tại Ô Diên (Hà Nội).<br>Năm 602: Tướng Tùy Lưu Phương mang đại quân xâm lược, Lý Phật Tử đầu hàng; Vạn Xuân diệt vong"]:::bth
        end

        VX_LYND -->|"548: Lý Nam Đế ốm nặng trao binh quyền cho Triệu Quang Phục; hoàng tộc chạy vào Nam"| VX_TVV
        VX_LYND --> VX_LPT

        VX_HLY -->|"Thời kỳ Bắc thuộc lần 3 (Tùy - Đường cai trị khắc nghiệt)"| BTH_MHD["Khởi nghĩa Mai Hắc Đế (Mai Thúc Loan: 713 - 722)<br>Căn cứ Vạn An (Hoan Châu - Nghệ An), giải phóng toàn bộ An Nam"]:::war
        --> BTH_PH["Bố Cái Đại Vương Phùng Hưng (766/791 - 791)<br>Khởi nghĩa Đường Lâm, vây đánh chiếm phủ thành Tống Bình (Hà Nội)"]:::war
        --> TC_KTD["Khúc Thừa Dụ (905 - 907)<br>Chớp thời cơ nhà Đường suy sụp, khởi nghĩa chiếm phủ thành xưng Tiết độ sứ, mở nền tự chủ"]:::ancient
        --> TC_KH["Khúc Hạo (907 - 917) & Khúc Thừa Mỹ (917 - 930)<br>Cải cách hành chính 'Chính sự khoan dung, giản dị, nhân dân đều được yên vui'"]:::ancient

        %% Song song: Sự biến Kiều Công Tiễn rước giặc vs Ngô Quyền khởi binh
        subgraph Sub2_KieuNgoSplit ["SỰ BIẾN 937 - 938: PHẢN TẶC RƯỚC GIẶC & NGÔ QUYỀN ĐẠI PHÁ BẠCH ĐẰNG"]
            TC_DDN["DƯƠNG ĐÌNH NGHỆ (931 - 937):<br>Từ Ái Châu dấy binh quét sạch quân Nam Hán của Lý Tiến và Trần Bảo, giải phóng Đại La"]:::victory
            -->|"937: Kiều Công Tiễn (hào trưởng Phong Châu) làm phản sát hại Dương Đình Nghệ đoạt chức Tiết độ sứ"| TC_KCT["KIỀU CÔNG TIỄN PHẢN NGHỊCH (937 - 938):<br>Bị cả nước căm ghét cô lập; hoảng sợ bèn dâng biểu sai sứ sang cầu viện vua Nam Hán Lưu Cung"]:::crisis
            -->|"Vua Nam Hán sai con trai Lưu Hoằng Tháo chỉ huy thủy quân vượt biển tràn sang xâm lược"| TC_NAMHAN["QUÂN XÂM LƯỢC NAM HÁN (938):<br>Vạn thuyền chiến do Hoằng Tháo chỉ huy tiến thẳng vào cửa sông Bạch Đằng"]:::war

            NGO_QUYEN_START["NGÔ QUYỀN KHỞI BINH TỪ ÁI CHÂU (937 - 938):<br>Con rể Dương Đình Nghệ, tập hợp hào kiệt Bắc - Nam tiến quân thần tốc ra thành Đại La diệt trừ phản tặc Kiều Công Tiễn"]:::victory
            -->|"Tháng 10/938: Ngô Quyền hạ Đại La giết Kiều Công Tiễn, dẹp yên nội phản trước khi giặc Nam Hán kịp tới"| TRANS_BD938["ĐẠI THẮNG BẠCH ĐẰNG LỊCH SỬ (NĂM 938):<br>Ngô Quyền cắm hàng nghìn cọc nhọn bọc sắt ngầm ở cửa biển Bạch Đằng.<br>Lợi dụng thủy triều rút, dồn toàn lực tổng phản công nhấn chìm toàn bộ chiến thuyền Nam Hán.<br>Chém chết tướng giặc Lưu Hoằng Tháo; Vua Nam Hán khóc thương không dám sang nữa.<br>CHẤM DỨT HƠN 1.000 NĂM BẮC THUỘC, MỞ RA KỶ NGUYÊN ĐỘC LẬP TỰ CHỦ LÂU DÀI"]:::victory

            TC_KCT -.->|"Tin phản nghịch Kiều Công Tiễn cầu viện giặc truyền tới Ái Châu"| NGO_QUYEN_START
            TC_NAMHAN --> TRANS_BD938
        end

        TC_KH -->|"930: Quân Nam Hán bắt Khúc Thừa Mỹ"| TC_DDN
    end

    TAYAU_QTAN -->|"179 TCN: Triệu Đà dùng mưu Mỵ Châu - Trọng Thủy cướp nỏ thần thôn tính Âu Lạc"| TRIEU_T1

    %% =========================================================================
    %% 3. THỜI KỲ ĐỘC LẬP XÂY DỰNG QUỐC GIA: NGÔ - ĐINH - TIỀN LÊ (939 - 1009)
    %% =========================================================================
    subgraph Sub3_NgoDinhLe ["3. NGÔ - ĐINH - TIỀN LÊ (939 - 1009)"]
        NGO_NQ["Tiền Ngô Vương (Ngô Quyền)<br>939 - 944 | Xưng Vương - Đóng đô tại Cổ Loa, bãi bỏ chức Tiết độ sứ"]:::monarch
        --> NGO_DTK["Dương Tam Kha (944 - 950: Cướp ngôi cháu)"]:::crisis
        --> NGO_NXV["Nam Tấn Vương Ngô Xương Văn (950-965) & Thiên Sách Vương Ngô Xương Ngập (951-954)<br>Nhà Ngô suy yếu; đến năm 965 Xương Văn mất, triều đình hoàn toàn tan rã"]:::monarch

        %% Song song: 12 Sứ quân cát cứ vs Đinh Bộ Lĩnh thống nhất
        subgraph Sub3_12SuQuan ["LOẠN 12 SỨ QUÂN & CÔNG CUỘC THỐNG NHẤT (965 - 968)"]
            SUQUAN_12["12 SỨ QUÂN CÁT CỨ ĐỊA PHƯƠNG (965 - 967):<br>- Đỗ Cảnh Thạc (Đỗ Động Giang), Kiều Công Hãn (Bạch Hạc), Kiều Thuận (Hồi Hồ)<br>- Nguyễn Siêu (Tây Phù Liệt), Lữ Đường (Tế Giang), Ngô Xương Xí (Bình Kiều)<br>- Ngô Nhật Khánh (Đường Lâm), Lý Khuê (Siêu Loại), Nguyễn Thủ Tiệp (Tiên Du)...<br>Chiến tranh hỗn loạn tàn phá làng xóm"]:::crisis

            DINH_BL_START["ĐINH BỘ LĨNH KHỞI BINH TẠI HOA LƯ (NINH BÌNH):<br>Cùng con trai Đinh Liễn dấy binh; liên minh kết nghĩa với Sứ quân Trần Lãm (Bố Hải Khẩu - Thái Bình).<br>Trần Lãm trao toàn bộ binh quyền; chiêu phục Sứ quân Phạm Bạch Hổ (Đằng Châu - Hưng Yên)"]:::victory
            -->|"Dùng mưu lược và quân sự tài tình, Đinh Bộ Lĩnh bẻ gãy từng sứ quân, thu phục lòng dân"| DINH_DBL["ĐINH TIÊN HOÀNG (ĐINH BỘ LĨNH: 968 - 979):<br>Được tôn xưng là 'VẠN THẮNG VƯƠNG', quét sạch loạn cát cứ, thu non sông về một mối.<br>Lên ngôi Hoàng đế (968), đặt Quốc hiệu ĐẠI CỒ VIỆT - Đô: Hoa Lư.<br>Đúc tiền Thái Bình hưng bảo, xác lập nền độc lập bình đẳng với các hoàng đế phương Bắc"]:::victory

            SUQUAN_12 -->|"Đinh Bộ Lĩnh đánh dẹp và thu phục toàn bộ 12 sứ quân (967 - 968)"| DINH_DBL
        end

        NGO_NXV -->|"965: Vua Ngô mất, các tướng lĩnh và thổ hào nổi dậy chia cắt đất nước"| SUQUAN_12
        NGO_NXV --> DINH_BL_START

        DINH_DBL -->|"979: Đỗ Thích ám sát Đinh Tiên Hoàng và Nam Việt Vương Đinh Liễn"| DINH_DT["Đinh Phế Đế (Đinh Toàn: 979 - 980)<br>Mới 6 tuổi lên ngôi; nhà Tống chuẩn bị đại quân xâm lược"]:::monarch
        -->|"Thái hậu Dương Vân Nga vì đại nghĩa quốc gia, trao áo Long bào cho Thập đạo Tướng quân Lê Hoàn"| TLE_LH["LÊ ĐẠI HÀNH (LÊ HOÀN: 980 - 1005):<br>Sáng lập Nhà Tiền Lê - Đô: Hoa Lư.<br>Kháng chiến chống Tống lần 1 (981): Chém chủ tướng Hầu Nhân Bảo trên sông Bạch Đằng, bắt sống tướng Quách Quỳ.<br>Bình Chiêm Thành (982); cày ruộng Tịch điền khuyến nông đầu xuân"]:::victory
        --> TLE_LTV["Lê Trung Tông (Lê Long Việt - 1005: Trị vì 3 ngày)"]:::monarch
        --> TLE_LLD["Lê Ngọa Triều (Lê Long Đĩnh: 1005 - 1009)<br>Vị vua cuối cùng triều Tiền Lê"]:::monarch
    end

    TRANS_BD938 --> NGO_NQ

    %% =========================================================================
    %% 4. THỜI KỲ ĐẠI VIỆT HOÀNG KIM: TRIỀU LÝ (1009 - 1225: 9 ĐỜI HOÀNG ĐẾ)
    %% =========================================================================
    subgraph Sub4_Ly ["4. VƯƠNG TRIỀU LÝ (1009 - 1225: 9 ĐỜI HOÀNG ĐẾ)"]
        LY_1["1. Lý Thái Tổ (Lý Công Uẩn)<br>1009 - 1028 | Năm 1010 ban 'Chiếu dời đô' từ Hoa Lư về Thăng Long"]:::monarch
        --> LY_2["2. Lý Thái Tông (Lý Phật Mã)<br>1028 - 1054 | Ban Bộ Hình thư (1042), dựng Chùa Một Cột (1049)"]:::monarch
        --> LY_3["3. Lý Thánh Tông (Lý Nhật Tôn)<br>1054 - 1072 | Đổi tên nước thành ĐẠI VIỆT (1054), lập Văn Miếu (1070)"]:::monarch
        --> LY_4["4. Lý Nhân Tông (Lý Càn Đức)<br>1072 - 1127 | Lập Quốc Tử Giám (1076) - Trường đại học đầu tiên.<br>Lý Thường Kiệt 'tiên phát chế nhân' đánh Ung Châu, đại phá Tống trên sông Như Nguyệt (1077) - Thơ thần 'Nam quốc sơn hà'"]:::victory
        --> LY_5["5. Lý Thần Tông (Lý Dương Hoán - 1128 - 1138)"]:::monarch
        --> LY_6["6. Lý Anh Tông (Lý Thiên Tộ - 1138 - 1175: Lập trang cảng Vân Đồn 1149)"]:::monarch
        --> LY_7["7. Lý Cao Tông (Lý Long Cán - 1175 - 1210)"]:::monarch
        --> LY_8["8. Lý Huệ Tông (Lý Hạo Sảm - 1210 - 1224)"]:::monarch
        --> LY_9["9. Lý Chiêu Hoàng (Lý Phật Kim)<br>1224 - 1225 | Nữ hoàng đế duy nhất trong lịch sử Việt Nam"]:::monarch
    end

    TLE_LLD -->|"Tháng 10/1009: Triều thần và sư Vạn Hạnh suy tôn Lý Công Uẩn lên ngôi hoàng đế"| LY_1

    %% =========================================================================
    %% 5. ĐẠI VIỆT TRIỀU TRẦN, TRIỀU HỒ & NHÀ HẬU TRẦN (1226 - 1413)
    %% =========================================================================
    subgraph Sub5_TranHo ["5. TRIỀU TRẦN, TRIỀU HỒ & NHÀ HẬU TRẦN (1226 - 1413)"]
        TRAN_1["1. Trần Thái Tông (Trần Cảnh)<br>1226 - 1258 | Thái sư Trần Thủ Độ phụ chính: 'Đầu tôi chưa rơi xuống đất, xin bệ hạ đừng lo'<br>Kháng chiến Mông Cổ lần 1 (1258): Thắng lợi Đông Bộ Đầu"]:::victory
        --> TRAN_2["2. Trần Thánh Tông (Trần Hoảng - 1258 - 1278)"]:::monarch
        --> TRAN_3["3. Trần Nhân Tông (Trần Khâm)<br>1278 - 1293 | Sáng lập Thiền phái Trúc Lâm Yên Tử<br>Hội nghị Bình Than, Hội nghị Diên Hồng 'Muôn người cùng hô ĐÁNH!'<br>Quốc công Tiết chế Trần Hưng Đạo - Hịch tướng sĩ - Đại thắng Nguyên Mông lần 2 (1285) & lần 3 (Bạch Đằng 1288)"]:::victory
        --> TRAN_4["4. Trần Anh Tông (1293 - 1314)"]:::monarch
        --> TRAN_5["5. Trần Minh Tông (1314 - 1329)"]:::monarch
        --> TRAN_6["6. Trần Hiến Tông (1329 - 1341)"]:::monarch
        --> TRAN_7["7. Trần Dụ Tông (1341 - 1369)"]:::monarch
        --> TRAN_8["8. Dương Nhật Lễ (1369 - 1370)"]:::crisis
        --> TRAN_9["9. Trần Nghệ Tông (1370 - 1372)"]:::monarch
        --> TRAN_10["10. Trần Duệ Tông (1372 - 1377: Tử trận tại Đồ Bàn)"]:::war
        --> TRAN_11["11. Trần Phế Đế (1377 - 1388)"]:::monarch
        --> TRAN_12["12. Trần Thuận Tông (1388 - 1398)"]:::monarch
        --> TRAN_13["13. Trần Thiếu Đế (1398 - 1400)"]:::monarch

        %% Triều Hồ & Kháng Minh
        HO_1["TRIỀU HỒ - HỒ QUÝ LY (1400):<br>Lập nước ĐẠI NGU - Xây Thành Tây Đô bằng đá khối.<br>Cải cách tiền giấy 'Thông bảo hội sao' (1396), súng Thần cơ Hồ Nguyên Trừng"]:::monarch
        --> HO_2["Hồ Hán Thương (1400 - 1407)<br>Đối mặt nguy cơ quân Minh xâm lược"]:::monarch
        -->|"1407: Giặc Minh (Trương Phụ) viện cớ 'Phù Trần diệt Hồ' xâm chiếm Đại Ngu, bắt cha con Hồ Quý Ly"| MINH_INVADE["ÁCH ĐÔ HỘ TÀN BẠO CỦA NHÀ MINH (1407 - 1427):<br>Đổi Đại Ngu thành quận Giao Chỉ; vơ vét tài nguyên, thiêu hủy sách vở văn hóa Đại Việt"]:::bth

        %% Song song: Phong trào Nhà Hậu Trần kháng Minh (1407 - 1413)
        subgraph Sub5_HauTranSplit ["PHONG TRÀO NHÀ HẬU TRẦN KHÁNG MINH (1407 - 1413)"]
            HTRAN_1["Giản Định Đế (Trần Ngỗi: 1407 - 1409):<br>Khởi binh tại Yên Mô (Ninh Bình); cùng danh tướng Đặng Tất, Nguyễn Cảnh Chân đại phá quân Minh trận Bô Cô (1408)"]:::victory
            -->|"Giản Định Đế nghe lời gièm pha giết oan Đặng Tất, Nguyễn Cảnh Chân làm suy yếu nghĩa quân"| HTRAN_2["Trùng Quang Đế (Trần Quý Khoáng: 1409 - 1413):<br>Được Đặng Dung, Nguyễn Cảnh Dị phò tá tiếp tục chiến đấu ngoan cường; đến 1413 bị giặc bắt tuẫn tiết"]:::monarch
        end

        TRAN_13 -->|"Tháng 02/1400: Hồ Quý Ly truất ngôi Thiếu Đế, sáng lập triều Hồ"| HO_1
        MINH_INVADE --> HTRAN_1
    end

    LY_9 -->|"10/01/1226: Lý Chiêu Hoàng nhường ngôi cho chồng là Trần Cảnh"| TRAN_1

    %% =========================================================================
    %% 6. THỜI KỲ KHỞI NGHĨA LAM SƠN & TRIỀU LÊ SƠ (1418 - 1527: 12 ĐỜI VUA)
    %% =========================================================================
    subgraph Sub6_LeSo ["6. KHỞI NGHĨA LAM SƠN & TRIỀU LÊ SƠ (1418 - 1527)"]
        LS_KHOINGHIA["10 NĂM KHỞI NGHĨA LAM SƠN (1418 - 1427):<br>Lê Lợi xưng Bình Định Vương - Quân sư Nguyễn Trãi (Hội thề Lũng Nhai 1416)<br>Trận Tốt Động - Chúc Động (1426), Trận Chi Lăng - Xương Giang chém Liễu Thăng (1427)<br>Hội thề Đông Quan buộc 10 vạn quân Minh rút sạch về nước không cần đánh"]:::victory
        --> LESO_1["1. Lê Thái Tổ (Lê Lợi: 1428 - 1433)<br>Nguyễn Trãi soạn 'BÌNH NGÔ ĐẠI CÁO' - Bản tuyên ngôn độc lập bất hủ khẳng định chủ quyền Đại Việt"]:::monarch
        --> LESO_2["2. Lê Thái Tông (Lê Nguyên Long: 1433 - 1442 | Vụ án Lệ Chi Viên)"]:::monarch
        --> LESO_3["3. Lê Nhân Tông (Lê Bang Cơ: 1442 - 1459)"]:::monarch
        --> LESO_4["4. Lê Nghi Dân (1459 - 1460)"]:::crisis
        --> LESO_5["5. LÊ THÁNH TÔNG (LÊ TƯ THÀNH: 1460 - 1497):<br>Thời kỳ cực thịnh hoàng kim Hồng Đức - Quốc gia Đại Việt hùng mạnh bậc nhất Đông Nam Á.<br>Ban hành Bộ luật Hồng Đức (Quốc triều hình luật), lập Bản đồ Hồng Đức (1469), sáng lập Hội Tao Đàn"]:::victory
        --> LESO_6["6. Lê Hiến Tông (1497 - 1504)"]:::monarch
        --> LESO_7["7. Lê Túc Tông (1504)"]:::monarch
        --> LESO_8["8. Lê Uy Mục (1504 - 1509: 'Quỷ vương' - Triều chính bắt đầu suy đồi)"]:::crisis
        --> LESO_9["9. Lê Tương Dực (1509 - 1516: 'Trĩ vương' - Xây Cửu Trùng Đài)"]:::crisis
        --> LESO_10["10. Lê Quang Trị (1516)"]:::crisis
        --> LESO_11["11. Lê Chiêu Tông (1516 - 1522 | Loạn Trần Cao, tướng lĩnh tranh giành quyền bính)"]:::crisis
        --> LESO_12["12. Lê Cung Hoàng (1522 - 1527 | Mạc Đăng Dung thao túng triều chính)"]:::crisis
    end

    HTRAN_2 -->|"Nhà Hậu Trần thất bại (1413); năm 1418 Lê Lợi phất cờ khởi nghĩa Lam Sơn tại Thanh Hóa"| LS_KHOINGHIA

    %% =========================================================================
    %% 7. THỜI KỲ NAM - BẮC TRIỀU & TRỊNH - NGUYỄN PHÂN TRANH (1527 - 1789)
    %% CỤC DIỆN 4 NHÀ PARALLEL: MẠC - LÊ TRUNG HƯNG - CHÚA TRỊNH - CHÚA NGUYỄN
    %% =========================================================================
    subgraph Sub7_PhanLiet ["7. THỜI KỲ NAM - BẮC TRIỀU & PHÂN LIỆT ĐÀNG TRONG - ĐÀNG NGOÀI (1527 - 1789)"]

        %% CỘT 1: BẮC TRIỀU - NHÀ MẠC (1527 - 1677)
        subgraph Sub7_Mac ["1. BẮC TRIỀU: NHÀ MẠC (1527 - 1677)"]
            MAC_1["MẠC THÁI TỔ (MẠC ĐĂNG DUNG: 1527 - 1529):<br>Tháng 06/1527: Phế truất Lê Cung Hoàng, lập Triều Mạc đóng đô tại Thăng Long (Bắc triều)"]:::mac
            --> MAC_2["MẠC HÀNG GIẢ NHÀ MINH (1540):<br>Nhà Minh đe dọa xâm lược; Mạc Đăng Dung lên ải Nam Quan chịu trói hàng giả, dâng biểu xưng thần và cắt đất biên giới nhằm tránh họa chiến tranh hủy diệt cho đất nước"]:::mac
            --> MAC_3["THỜI KỲ THỊNH TRỊ NHÀ MẠC TẠI THĂNG LONG:<br>Mạc Thái Tông (Đăng Doanh), Mạc Phúc Hải, Mạc Phúc Nguyên.<br>Trọng dụng hiền tài, khoa cử nở rộ (Trạng Trình Nguyễn Bỉnh Khiêm, Giáp Hải)"]:::mac
            --> MAC_4["MẠC MẬU HỢP BỊ DIỆT TẠI THĂNG LONG (1592):<br>Nhà Mạc suy đồi; quân Nam Triều do Trịnh Tùng chỉ huy đánh chiếm Thăng Long.<br>Mạc Mậu Hợp bị bắt và xử tử"]:::mac
            --> MAC_5["TẠI SAO NHÀ MẠC CHẠY LÊN CAO BẰNG? (1592 - 1677):<br>Tàn quân họ Mạc (Mạc Kính Chỉ, Kính Cung, Kính Khoan, Kính Vũ) rút lên đất Cao Bằng hiểm trở lập phòng tuyến Bản Phủ.<br>Họ Mạc thần phục và triều cống nhà Minh, rồi sau đó là nhà Thanh sơ kỳ.<br>Minh và Thanh dùng nhà Mạc làm 'VÙNG ĐỆM BIÊN GIỚI' để kiềm chế chính quyền Lê - Trịnh, ép Trịnh không được đánh Cao Bằng"]:::mac
            --> MAC_6["NHÀ MẠC BỊ TIÊU DIỆT HOÀN TOÀN (1677):<br>Nhân lúc nhà Thanh bận đối phó Loạn Tam Phiên (Ngô Tam Quế) mất khả năng bảo trợ cho Mạc, Chúa Trịnh Tạc sai Đinh Văn Tả tiến đánh giải phóng Cao Bằng, dẹp sạch Mạc Kính Vũ sau 150 năm tồn tại"]:::mac
        end

        %% CỘT 2: NAM TRIỀU & VƯƠNG TRIỀU LÊ TRUNG HƯNG (1533 - 1789)
        subgraph Sub7_Le ["2. NAM TRIỀU & VƯƠNG TRIỀU LÊ TRUNG HƯNG (1533 - 1789)"]
            LE_1["LÊ TRANG TÔNG (LÊ DUY NINH: 1533 - 1548):<br>Nguyễn Kim tìm được con vua Chiêu Tông bên Lào, tôn lên ngôi vua tại Vạn Lại (Thanh Hóa), giương cờ 'Phù Lê diệt Mạc', lập nên Nam Triều"]:::le_th
            --> LE_2["CÁC VUA LÊ THỜI KỲ ĐẦU TRUNG HƯNG (1548 - 1592):<br>Lê Trung Tông, Lê Anh Tông, Lê Thế Tông.<br>Thực tế quyền bính rơi vào tay họ Trịnh; vua Lê đóng vai trò bình phong chính thống hiệu triệu muôn dân"]:::le_th
            --> LE_3["LÊ THẾ TÔNG VỀ LẠI THĂNG LONG (1592):<br>Sau khi dẹp Mạc ở Thăng Long, vua Lê trở về kinh sư nhưng hoàn toàn bị quyền lực họ Trịnh thâu tóm"]:::le_th
            --> LE_4["MÔ HÌNH LƯỠNG ĐẦU 'VUA LÊ - CHÚA TRỊNH' (1592 - 1786):<br>16 đời Hoàng đế Lê Trung Hưng nối tiếp nhau ngự Cung Vua chỉ giữ quyền tế tự, phong tước, nhận triều bái danh nghĩa; mất toàn bộ quyền binh, tài chính và quan chế vào tay Phủ Chúa Trịnh"]:::le_th
            --> LE_5["VUA LÊ HIỂN TÔNG (1740 - 1786):<br>Vị vua trị vì lâu nhất triều Lê Trung Hưng (46 năm).<br>Tháng 07/1786: Nguyễn Huệ ra Bắc 'Phù Lê diệt Trịnh', yết kiến vua Lê, kết duyên cùng Công chúa Ngọc Hân.<br>Vua Lê Hiển Tông phong Nguyễn Huệ làm Nguyên soái Uy quốc công, không lâu sau thì băng hà"]:::le_th
        end

        %% CỘT 3: ĐÀNG NGOÀI - 13 ĐỜI CHÚA TRỊNH (1545 - 1787)
        subgraph Sub7_Trinh ["3. PHỦ CHÚA ĐÀNG NGOÀI: 13 ĐỜI CHÚA TRỊNH (1545 - 1787)"]
            TRINH_1["THÁI SƯ TRỊNH KIỂM (1545 - 1570):<br>Con rể Nguyễn Kim; sau khi cha vợ bị ám hại, Trịnh Kiểm nắm trọn binh quyền Nam Triều, khởi đầu quyền lực họ Trịnh"]:::trinh
            --> TRINH_2["BÌNH AN VƯƠNG TRỊNH TÙNG (1570 - 1623):<br>Đánh bật nhà Mạc khỏi Thăng Long (1592); thiết lập Phủ Chúa với hệ thống Lục phiên lấn át hoàn toàn Cung Vua"]:::trinh
            --> TRINH_3["TRỊNH - NGUYỄN ĐẠI CHIẾN (1627 - 1672):<br>Trịnh Tráng & Trịnh Tạc 7 lần dồn binh lực tinh nhuệ nam chinh vượt sông Gianh đánh Đàng Trong nhưng không phá nổi phòng tuyến Lũy Thầy"]:::war
            --> TRINH_4["ĐÌNH CHIẾN LẤY SÔNG GIANH CHIA ĐÔI ĐẤT NƯỚC (1672 - 1774):<br>Hai bên kiệt quệ chấp nhận hòa hoãn; Trịnh Tạc rảnh tay đưa quân lên tiêu diệt sào huyệt Cao Bằng của họ Mạc (1677)"]:::trinh
            --> TRINH_5["KHỦNG HOẢNG ĐÀNG NGOÀI & KHỞI NGHĨA NÔNG DÂN (Giữa TK XVIII):<br>Thời Trịnh Giang ăn chơi xa đọa; nông dân cùng quẫn vùng lên khởi nghĩa khắp Bắc Hà: Quận He Nguyễn Hữu Cầu, Hoàng Công Chất, Nguyễn Danh Phương..."]:::crisis
            --> TRINH_6["TĨNH ĐÔ VƯƠNG TRỊNH SÂM ĐÁNH CHIẾM PHÚ XUÂN (1774):<br>Chớp thời cơ Tây Sơn nổi dậy ở Đàng Trong, Trịnh Sâm sai Hoàng Ngũ Phúc đem đại quân vượt sông Gianh đánh chiếm kinh đô Phú Xuân của Chúa Nguyễn"]:::victory
            --> TRINH_7["LOẠN KIÊU BINH & CƠ NGHIỆP HỌ TRỊNH SỤP ĐỔ (1782 - 1786):<br>Sau khi Trịnh Sâm mất, kiêu binh Tam phủ làm loạn phế Trịnh Cán lập Trịnh Khải.<br>Năm 1786: Nguyễn Huệ thần tốc tiến ra Thăng Long đánh tan quân Trịnh; Trịnh Khải bị bắt cắt cổ tự vẫn; cơ nghiệp Chúa Trịnh sụp đổ sau 242 năm"]:::crisis
        end

        %% CỘT 4: ĐÀNG TRONG - 10 ĐỜI CHÚA NGUYỄN (1558 - 1777)
        subgraph Sub7_Nguyen ["4. CÕI ĐÀNG TRONG: 10 ĐỜI CHÚA NGUYỄN (1558 - 1777)"]
            NGUYEN_1["CHÚA TIÊN NGUYỄN HOÀNG (1558 - 1613):<br>Thấy anh trai Nguyễn Uông bị Trịnh Kiểm sát hại, lo sợ cho mạng sống; nghe theo lời sấm của Trạng Trình: 'Hoành sơn nhất đái, vạn đại dung thân', xin vào trấn thủ Thuận Hóa, đặt nền móng dựng nghiệp Đàng Trong"]:::nguyen
            --> NGUYEN_2["CHÚA SÃI NGUYỄN PHÚC NGUYÊN (1613 - 1635):<br>Trọng dụng mưu sĩ Đào Duy Từ đắp Lũy Thầy kiên cố; cự tuyệt nộp thuế cho Chúa Trịnh, kiên cường đánh bại các đợt tiến công của quân Trịnh"]:::nguyen
            --> NGUYEN_3["CHIẾN ĐẤU GIỮ VỮNG ĐÀNG TRONG TRONG 7 LẦN GIAO TRANH (1627 - 1672):<br>Dựa vào thành lũy hiểm trở và vũ khí đại bác Bồ Đào Nha đập tan các cuộc nam chinh của họ Trịnh"]:::victory
            --> NGUYEN_4["SỰ NGHIỆP MỞ CÕI PHƯƠNG NAM VĨ ĐẠI (NAM TIẾN):<br>- 1698: Chúa Minh Nguyễn Phúc Chu sai Nguyễn Hữu Cảnh vào Nam kinh lược, lập Phủ Gia Định (định hình đất Sài Gòn - Nam Bộ).<br>- 1708: Mạc Cửu dâng toàn bộ vùng đất Hà Tiên thần phục Chúa Nguyễn.<br>- Thành lập Đội Hoàng Sa & Đội Bắc Hải cắm mốc, đo đạc hải trình khẳng định chủ quyền Hoàng Sa, Trường Sa"]:::victory
            --> NGUYEN_5["KHỦNG HOẢNG ĐÀNG TRONG THẾ KỶ XVIII:<br>Chúa Định Vương Nguyễn Phúc Thuần nhỏ tuổi bất tài; quyền thần Trương Phúc Loan chuyên quyền tham nhũng, sưu cao thuế nặng làm nhân dân Đàng Trong cùng quẫn, dẫn tới bùng nổ khởi nghĩa Tây Sơn"]:::crisis
            --> NGUYEN_6["CHÚA NGUYỄN ĐÀNG TRONG SỤP ĐỔ (1774 - 1777):<br>Năm 1774: Quân Trịnh Hoàng Ngũ Phúc đánh chiếm Phú Xuân.<br>Chúa Nguyễn dạt vào Gia Định. Năm 1777 Nguyễn Huệ tiến đánh Gia Định giết Định Vương Nguyễn Phúc Thuần & Tân Chính Vương Nguyễn Phúc Dương.<br>Cơ nghiệp hơn 200 năm Chúa Nguyễn Đàng Trong sụp đổ; Nguyễn Ánh đào tẩu lưu vong"]:::crisis
        end

        %% CÁC KẾT NỐI PARALLEL LIÊN NHÀ (CROSS-CONNECTORS GIỮA 4 NHÀ)
        MAC_1 -->|"1533: Nguyễn Kim sang Lào tôn Lê Duy Ninh lên làm vua Lê Trang Tông lập Nam triều 'Phù Lê diệt Mạc'"| LE_1
        MAC_1 -->|"1545: Hàng tướng Mạc Dương Chấp Nhất đầu độc Nguyễn Kim; Trịnh Kiểm lên nắm trọn binh quyền"| TRINH_1
        TRINH_1 -->|"1558: Nguyễn Hoàng sợ Trịnh Kiểm ám hại, theo lời Trạng Trình xin vào trấn thủ Thuận Hóa"| NGUYEN_1
        TRINH_2 -->|"1592: Trịnh Tùng đánh Thăng Long chém Mạc Mậu Hợp; ép tàn dư họ Mạc chạy dạt lên cố thủ Cao Bằng"| MAC_4
        TRINH_2 -->|"1592: Trịnh Tùng rước vua Lê về Thăng Long, thiết lập Phủ Chúa thâu tóm mọi quyền lực thực tế"| LE_3
        MAC_4 -->|"1592: Mạc rút lên Cao Bằng núp bóng nhà Minh/Thanh bảo trợ để làm vùng đệm kiềm chế Trịnh"| MAC_5
        NGUYEN_2 -->|"1627: Chúa Sãi cự tuyệt triều cống họ Trịnh, Đào Duy Từ đắp Lũy Thầy; Trịnh Tráng phát binh nam chinh"| TRINH_3
        TRINH_3 -.->|"1672: Bất phân thắng bại sau 7 lần giao tranh ác liệt; lấy SÔNG GIANH chia đôi non sông suốt hơn một thế kỷ"| NGUYEN_3
        TRINH_4 -->|"1677: Thừa dịp nhà Thanh bận dẹp Loạn Tam Phiên, Trịnh Tạc sai Đinh Văn Tả tiến đánh quét sạch Cao Bằng"| MAC_6
        TRINH_6 -->|"1774: Hoàng Ngũ Phúc hạ Phú Xuân; Chúa Nguyễn rơi vào thế lưỡng đầu thọ địch, bỏ chạy vào Gia Định"| NGUYEN_5
        NGUYEN_5 -->|"1771: Sự hà khắc tham tàn của Trương Phúc Loan làm bùng nổ Khởi nghĩa Tây Sơn"| TS_START
    end

    LESO_12 -->|"Tháng 06/1527: Mạc Đăng Dung cướp ngôi nhà Lê lập ra Triều Mạc"| MAC_1

    %% =========================================================================
    %% 8. PHONG TRÀO TÂY SƠN: CỤC DIỆN ĐA CỰC & THỐNG NHẤT NON SÔNG (1771 - 1802)
    %% CỤC DIỆN 3 NHÁNH PARALLEL: VƯƠNG TRIỀU TÂY SƠN - VUA LÊ/MÃN THANH - NGUYỄN ÁNH
    %% =========================================================================
    subgraph Sub8_TaySonDaCuc ["8. PHONG TRÀO TÂY SƠN & CỤC DIỆN ĐA CỰC THỐNG NHẤT (1771 - 1802)"]

        %% NHÁNH 1: VƯƠNG TRIỀU TÂY SƠN & VUA QUANG TRUNG NGUYỄN HUỆ
        subgraph Sub8_TaySonBranch ["1. VƯƠNG TRIỀU TÂY SƠN: ANH HÙNG ÁO VẢI QUANG TRUNG NGUYỄN HUỆ"]
            TS_START["KHỞI NGHĨA TÂY SƠN THƯỢNG ĐẠO (1771):<br>Ba anh em Nguyễn Nhạc, Nguyễn Huệ, Nguyễn Lữ dựng cờ tại An Khê (Gia Lai).<br>'Lấy của nhà giàu chia cho người nghèo', lật đổ ách áp bức của Trương Phúc Loan"]:::ts
            --> TS_QN1773["HẠ THÀNH QUY NHƠN (1773):<br>Nguyễn Nhạc dùng mẹo ngồi cũi vào thành, nửa đêm phá cũi mở cổng đánh chiếm"]:::ts
            --> TS_HOATRINH["HÒA TRỊNH ĐÁNH NGUYỄN (1774 - 1775):<br>Tạm hòa hoãn với Hoàng Ngũ Phúc để dồn toàn lực tiến đánh Chúa Nguyễn"]:::ts
            --> TS_GD1777["TIẾN ĐÁNH GIA ĐỊNH & DIỆT CHÚA NGUYỄN (1776 - 1777):<br>Nguyễn Huệ cầm quân đánh chiếm Gia Định, bắt và xử tử 2 chúa Nguyễn Phúc Thuần & Nguyễn Phúc Dương.<br>Cơ nghiệp Chúa Nguyễn Đàng Trong sụp đổ; Nguyễn Nhạc xưng Thái Đức Hoàng đế (1778) tại Quy Nhơn"]:::victory
            --> TS_RACM["ĐẠI THẮNG RẠCH GẦM - XOÀI MÚT (20/01/1785):<br>Nguyễn Huệ bố trí mai phục hỏa công trên sông Tiền, tiêu diệt sạch 5 vạn quân xâm lược Xiêm La và 300 thuyền chiến.<br>'Người Xiêm sau trận ấy sợ Tây Sơn như sợ cọp'"]:::victory
            --> TS_PX1786["GIẢI PHÓNG THUẬN HÓA - PHÚ XUÂN (06/1786):<br>Nguyễn Huệ đánh tan 3 vạn quân Trịnh của Phạm Ngô Cầu, thu phục toàn bộ đất cũ Đàng Trong"]:::victory
            --> TS_BAC1786["BẮC TIẾN 'PHÙ LÊ DIỆT TRỊNH' (07/1786):<br>Nguyễn Huệ vượt Đèo Ngang hạ Vị Hoàng, tiến vào Thăng Long; xóa sổ cơ nghiệp Chúa Trịnh.<br>Nguyễn Huệ yết kiến vua Lê Hiển Tông, kết duyên cùng Công chúa Ngọc Hân; xóa bỏ ranh giới Sông Gianh"]:::victory
            --> TS_TAMPHU["CỤC DIỆN PHÂN CHIA TAM PHỦ (1787):<br>- Trung ương Hoàng đế Nguyễn Nhạc: Quy Nhơn.<br>- Bắc Bình Vương Nguyễn Huệ: Phú Xuân (đô thành).<br>- Đông Định Vương Nguyễn Lữ: Gia Định"]:::crisis
            --> TS_QT_DANGCO["NGUYỄN HUỆ LÊN NGÔI HOÀNG ĐẾ QUANG TRUNG (22/12/1788):<br>PARALLEL KHI QUÂN THANH TRÀN VÀO THĂNG LONG:<br>Nguyễn Huệ tại Phú Xuân nhận tin cấp báo từ Ngô Thì Nhậm.<br>Tế cáo trời đất tại Núi Bân (Huế), đăng quang Hoàng đế, xuất quân thần tốc ra Bắc.<br>Hội quân tại Tam Điệp khao quân ăn Tết trước: 'Đánh cho để dài tóc, Đánh cho để đen răng...'"]:::qt
            --> TS_QT_CHIENDICH["ĐẠI THẮNG 29 VẠN QUÂN THANH TẾT KỶ DẬU (1789):<br>- Đêm 30 Tết: Đột kích hạ đồn Gián Khẩu.<br>- Mùng 3 Tết: Vây bức hàng đồn Hà Hồi không tốn một mũi tên.<br>- Sáng mùng 5 Tết: Công phá đại đồn Ngọc Hồi; Trận Khương Thượng - Đống Đa, Đô đốc Đặng Tiến Đông đánh úp, Sầm Nghi Đống thắt cổ tự tử.<br>- Trưa mùng 5 Tết: Vua Quang Trung ngự áo bào sạm khói súng tiến vào Thăng Long.<br>Tôn Sĩ Nghị cắt cầu phao chạy trốn; quét sạch 29 vạn quân Mãn Thanh"]:::victory
            --> TS_QT_REFORMS["CANH TÂN ĐẤT NƯỚC & VUA QUANG TRUNG BĂNG HÀ (1789 - 1792):<br>- Ban Chiếu khuyến nông, Chiếu cầu hiền, đưa chữ Nôm vào khoa cử, đúc tiền Quang Trung thông bảo.<br>- Ngày 16/09/1792: Vua Quang Trung đột ngột băng hà ở tuổi 40"]:::qt
            --> TS_QUANGTOAN["CẢNH THỊNH HOÀNG ĐẾ (QUANG TOẢN: 1792 - 1802):<br>Lên ngôi lúc 10 tuổi; Thái sư Bùi Đắc Tuyên lộng quyền, nội bộ tướng lĩnh nghi kỵ thanh trừng lẫn nhau làm triều Tây Sơn suy yếu trầm trọng"]:::crisis
        end

        %% NHÁNH 2: VUA LÊ CHIÊU THỐNG & 29 VẠN QUÂN MÃN THANH (1786 - 1789)
        subgraph Sub8_LeThanhBranch ["2. VUA LÊ CHIÊU THỐNG CẦU VIỆN & QUÂN XÂM LƯỢC MÃN THANH"]
            LE_CT_START["LÊ CHIÊU THỐNG NỐI NGÔI TẠI THĂNG LONG (1786):<br>Sau khi Nguyễn Huệ rút quân về Nam, Chiêu Thống bất lực trước sự lộng hành của Trịnh Bồng và Nguyễn Hữu Chỉnh; kinh thành Thăng Long bị cướp bóc tàn phá"]:::crisis
            --> LE_CT_CAUVIEN["CHIÊU THỐNG BỎ CHẠY SANG TÀU CẦU VIỆN NHÀ THANH (Cuối 1788):<br>Bỏ ngai vàng tháo chạy sang Quảng Tây dâng biểu cầu viện Hoàng đế Càn Long đem quân cứu viện phục ngôi"]:::crisis
            --> LE_CT_BUNHIN["29 VẠN QUÂN THANH TRÀN VÀO THĂNG LONG (11/1788):<br>Tổng đốc Lưỡng Quảng Tôn Sĩ Nghị dẫn 29 vạn quân Thanh hộ tống Chiêu Thống chiếm đóng Thăng Long.<br>Chiêu Thống làm vua bù nhìn hà khắc, mượn bóng giặc tàn sát trả thù người trung nghĩa.<br>Quân Tây Sơn Ngô Thì Nhậm, Ngô Văn Sở tạm lui về phòng tuyến Tam Điệp - Biện Sơn"]:::war
            --> LE_CT_DIETVONG["CHIÊU THỐNG THÁO CHẠY THỤC MẠNG SANG BẮC KINH (05 Tết 1789):<br>Bị Vua Quang Trung đánh tan tác trong trận Đống Đa, Tôn Sĩ Nghị cùng Chiêu Thống chạy trối chết sang biên giới.<br>Chiêu Thống lưu vong nhục nhã tại Bắc Kinh rồi uất hận chết xứ người (1793); TRIỀU HẬU LÊ CHÍNH THỨC DIỆT VONG"]:::bth
        end

        %% NHÁNH 3: PHE CHÚA NGUYỄN PHỤC HỒI - NGUYỄN ÁNH (1777 - 1802)
        subgraph Sub8_NguyenAnhBranch ["3. PHE NGUYỄN ÁNH: CỦNG CỐ GIA ĐỊNH & ĐẠI PHẢN CÔNG"]
            NA_BONTAL["NGUYỄN ÁNH BÔN TẨU & LÁNH NẠN (1777 - 1783):<br>Sống sót sau cuộc tàn sát của Tây Sơn tại Gia Định, tập hợp tàn quân kháng cự, nhiều lần lánh nạn ra đảo Phú Quốc"]:::nguyen
            --> NA_CAUXIEM["NGUYỄN ÁNH CẦU VIỆN QUÂN XIÊM LA (1784 - 1785):<br>Sang Vọng Các cầu viện vua Xiêm Rama I mang 5 vạn quân sang xâm lược miền Tây Nam Bộ.<br>Bị Nguyễn Huệ quét sạch trong trận Rạch Gầm - Xoài Mút; Ánh lại phải chạy sang Xiêm lưu vong"]:::war
            --> NA_TAICHIEMGD["NGUYỄN ÁNH TÁI CHIẾM GIA ĐỊNH (08/1788):<br>PARALLEL LÚC NGUYỄN HUỆ ĐANG Ở BẮC HÀ VÀ PHÚ XUÂN:<br>Nhân lúc Nguyễn Huệ bận lo việc Bắc Hà và Nguyễn Lữ bỏ chạy về Quy Nhơn, Nguyễn Ánh từ Xiêm trở về đánh chiếm lại toàn bộ Gia Định"]:::nguyen
            --> NA_CONGCOGD["CỦNG CỐ NAM HÀ & XÂY DỰNG LỰC LƯỢNG (1789 - 1799):<br>PARALLEL THỜI KỲ VUA QUANG TRUNG ĐẠI PHÁ QUÂN THANH & CANH TÂN:<br>Nguyễn Ánh xây thành Bát Quái Gia Định (1790), lập đồn điền tích thảo lương, thuê chuyên gia Pháp đúc súng đại bác, đóng tàu chiến bọc đồng kiểu phương Tây"]:::nguyen
            --> NA_DAICHIEN["ĐẠI PHẢN CÔNG TÂY SƠN (1799 - 1801):<br>- 1799 - 1801: Đại vây hãm thành Bình Định (Võ Tánh tự thiêu lầu Bát Giác, Ngô Tùng Châu tuẫn tiết).<br>- 02/1801: ĐẠI THỦY CHIẾN THỊ NẠI tiêu diệt hoàn toàn hạm đội Tây Sơn; Nguyễn Ánh đánh chiếm lại kinh đô Phú Xuân"]:::war
            --> NA_THONGNHAT["TRẬN TRẤN NINH & TIÊU DIỆT NHÀ TÂY SƠN (1802):<br>Quang Toản cùng Nữ tướng Bùi Thị Xuân phản công tại Trấn Ninh thất bại.<br>Nguyễn Ánh tiến quân ra Bắc bắt sống Quang Toản; chấm dứt hoàn toàn triều đại Tây Sơn"]:::victory
        end

        %% CÁC KẾT NỐI TƯƠNG TÁC THỜI GIAN GIỮA 3 NHÁNH TRONG SECTION 8 VÀ SECTION 7
        TRINH_6 -->|"1774 - 1775: Hoàng Ngũ Phúc hạ Phú Xuân; Nguyễn Nhạc tạm hòa hoãn với Trịnh để dồn lực đánh Chúa Nguyễn"| TS_HOATRINH
        TS_GD1777 -->|"1777: Nguyễn Huệ hạ Gia Định giết 2 chúa Nguyễn; cơ nghiệp Chúa Nguyễn Đàng Trong hoàn toàn sụp đổ"| NGUYEN_6
        NGUYEN_6 -->|"1777: Hậu duệ duy nhất trốn thoát là Nguyễn Ánh bôn tẩu tìm đường khôi phục"| NA_BONTAL

        NA_BONTAL -->|"1784: Nguyễn Ánh rước 5 vạn quân Xiêm La vào xâm lược miền Tây"| NA_CAUXIEM
        NA_CAUXIEM -->|"20/01/1785: Nguyễn Huệ đập tan 5 vạn giặc Xiêm tại Rạch Gầm - Xoài Mút; Nguyễn Ánh lưu vong sang Xiêm"| TS_RACM

        TS_BAC1786 -->|"07/1786: Nguyễn Huệ tiến ra Thăng Long đánh tan quân Trịnh; Trịnh Khải bị bắt cắt cổ tự vẫn; cơ nghiệp Chúa Trịnh sụp đổ"| TRINH_7
        TS_BAC1786 -->|"07/1786: Nguyễn Huệ yết kiến vua Lê Hiển Tông, trả lại quyền bính cho nhà Lê, kết duyên cùng Công chúa Ngọc Hân"| LE_5
        LE_5 -->|"Tháng 08/1786: Vua Lê Hiển Tông băng hà, Lê Chiêu Thống lên ngôi; Nguyễn Huệ rút quân về Nam; Bắc Hà rơi vào hỗn loạn"| LE_CT_START

        TS_TAMPHU -->|"1788: Nguyễn Lữ bỏ chạy; Nguyễn Ánh từ Xiêm về tái chiếm Gia Định trong lúc Nguyễn Huệ bận việc Bắc Hà"| NA_TAICHIEMGD

        LE_CT_START -->|"1788: Chiêu Thống trốn khỏi kinh thành, chạy sang Trung Quốc cầu viện Càn Long"| LE_CT_CAUVIEN
        LE_CT_CAUVIEN -->|"Cuối 1788: Càn Long điều Tôn Sĩ Nghị mang 29 vạn quân Thanh chiếm đóng Thăng Long"| LE_CT_BUNHIN
        LE_CT_BUNHIN -->|"20/12/1788: Ngô Thì Nhậm cấp báo về Phú Xuân; Nguyễn Huệ đăng quang Hoàng đế Quang Trung, thần tốc xuất binh"| TS_QT_DANGCO
        TS_QT_CHIENDICH -->|"Mùng 5 Tết 1789: Quang Trung đại phá quân Thanh; Chiêu Thống hoảng loạn chạy theo giặc sang Bắc Kinh; triều Hậu Lê diệt vong"| LE_CT_DIETVONG

        TS_QT_REFORMS -.->|"1789 - 1792: Vua Quang Trung canh tân phía Bắc; Nguyễn Ánh xây thành Gia Định, đúc súng, đóng tàu bọc đồng ở phía Nam"| NA_CONGCOGD
        TS_QUANGTOAN -->|"1799 - 1801: Triều Cảnh Thịnh nội bộ thanh trừng chia rẽ; Nguyễn Ánh mở đại phản công hạ Quy Nhơn và Phú Xuân"| NA_DAICHIEN
        NA_CONGCOGD --> NA_DAICHIEN
        NA_DAICHIEN --> NA_THONGNHAT
    end

    %% CHUYỂN GIAO THỜI KỲ TÂY SƠN - VƯƠNG TRIỀU NGUYỄN
    NA_THONGNHAT -->|"Tháng 06/1802: Nguyễn Ánh lên ngôi Hoàng đế Gia Long tại Phú Xuân, thống nhất non sông trọn vẹn"| VNGUYEN_1

    %% =========================================================================
    %% 9. VƯƠNG TRIỀU NGUYỄN KẾ THỪA THỐNG NHẤT & KHÁNG PHÁP (1802 - 1945)
    %% PARALLEL: TRIỀU ĐÌNH ĐẦU HÀNG VS PHONG TRÀO KHÁNG CHIẾN CỦA TOÀN DÂN
    %% =========================================================================
    subgraph Sub9_TrieuNguyen ["9. VƯƠNG TRIỀU NGUYỄN KẾ THỪA THỐNG NHẤT & KHÁNG CHIẾN CHỐNG PHÁP (1802 - 1945)"]

        %% CÁC VUA ĐẦU TRIỀU NGUYỄN
        subgraph Sub9_CungCoThongNhat ["CỦNG CỐ THỐNG NHẤT & BẢO VỆ CHỦ QUYỀN (1802 - 1858)"]
            VNGUYEN_1["1. GIA LONG (NGUYỄN PHÚC ÁNH: 1802 - 1820):<br>Đặt Quốc hiệu VIỆT NAM (1804) - Thống nhất bờ cõi từ Ải Nam Quan đến Mũi Cà Mau.<br>Xây dựng Kinh thành Huế; Ban hành Hoàng triều luật lệ (Luật Gia Long).<br>Năm 1816: Cắm cờ xác lập chủ quyền vững chắc trên Quần đảo Hoàng Sa và Trường Sa"]:::monarch
            --> VNGUYEN_2["2. MINH MẠNG (NGUYỄN PHÚC ĐẢM: 1820 - 1841):<br>Đổi quốc hiệu thành ĐẠI NAM (1838) - Đỉnh cao cải cách hành chính chia 30 tỉnh và 1 phủ Thừa Thiên (1831-1832).<br>Chiến tranh Việt - Xiêm (1833-1834): Đánh tan giặc Xiêm trên sông Vàm Nao và kênh Vĩnh Tế; dẹp loạn Lê Văn Khôi (1833-1835)"]:::monarch
            --> VNGUYEN_3["3. Thiệu Trị (1841 - 1847 | Chiến tranh Việt - Xiêm 1841-1845 giữ yên biên cương Tây Nam)"]:::monarch
            --> VNGUYEN_4["4. Tự Đức (Nguyễn Phúc Hồng Nhậm: 1847 - 1883)<br>Nho học bảo thủ; đối mặt với nguy cơ thực dân Pháp nổ súng xâm lược Đà Nẵng (01/09/1858)"]:::monarch
        end

        %% PARALLEL: TRIỀU ĐÌNH NHU NHƯỢC KÝ HIỆP ƯỚC VS DÂN CHÚNG KHÁNG CHIẾN
        subgraph Sub9_PhapXamLuocSplit ["GIAI ĐOẠN PHÁP XÂM LƯỢC: TRIỀU ĐÌNH ĐẦU HÀNG VS NHÂN DÂN KHÁNG CHIẾN (1858 - 1884)"]
            subgraph Sub9_TrieuDinhDauHang ["TRIỀU ĐÌNH HUẾ THỎA HIỆP & KÝ HIỆP ƯỚC ĐẦU HÀNG"]
                F_DANANG["CHIẾN DỊCH ĐÀ NẴNG (1858 - 1860):<br>Liên quân Pháp - Tây Ban Nha nổ súng tấn công bán đảo Sơn Trà"]:::war
                --> F_NAMKY["CHIẾN DỊCH NAM KỲ (1859 - 1867):<br>Pháp hạ thành Gia Định (1859), phá đại đồn Chí Hòa (1861).<br>Triều đình ký Hiệp ước Nhâm Tuất (1862) cắt 3 tỉnh miền Đông; năm 1867 mất nốt 3 tỉnh miền Tây; Phan Thanh Giản tuyệt thực"]:::war
                --> F_BACKY1["CHIẾN DỊCH BẮC KỲ LẦN 1 (1873):<br>Garnier đánh chiếm Hà Nội; Triều đình ký Hiệp ước Giáp Tuất (1874) công nhận Nam Kỳ là thuộc địa của Pháp"]:::war
                --> F_BACKY2["CHIẾN DỊCH BẮC KỲ LẦN 2 (1882):<br>Henri Rivière hạ thành Hà Nội; Tổng đốc Hoàng Diệu thắt cổ tuẫn tiết"]:::war
                --> F_THUANAN["HIỆP ƯỚC HÀM PHỤC MẤT NƯỚC (1883 - 1884):<br>Pháp bắn phá Thuận An; Triều đình ký Hiệp ước Quý Mùi (Harmand 1883) & Giáp Thân (Patenôtre 1884), đặt trọn quyền bảo hộ của Pháp lên toàn cõi Việt Nam"]:::treaty
            end

            subgraph Sub9_NhanDanKhangChien ["PHONG TRÀO TOÀN DÂN ANH DŨNG KHÁNG CHIẾN"]
                RES_LIENTRI["Nguyễn Tri Phương lập phòng tuyến Liên Trì giam chân giặc Pháp 18 tháng tại Đà Nẵng"]:::victory
                --> RES_TRUONGDINH["Khởi nghĩa Trương Định (Bình Tây Đại nguyên soái: 1861 - 1864) tại Tân An - Gò Công"]:::hero
                --> RES_TRUNGTRUC["Nguyễn Trung Trực đốt cháy tàu Espérance (1861) và hạ đồn Kiên Giang (1868):<br>'Bao giờ người Tây nhổ hết cỏ nước Nam mới hết người Nam đánh Tây'"]:::hero
                --> RES_CAUGIAY1["Đại thắng Cầu Giấy lần 1 (21/12/1873): Tiêu diệt Francis Garnier"]:::victory
                --> RES_CAUGIAY2["Đại thắng Cầu Giấy lần 2 (19/05/1883): Tiêu diệt Henri Rivière"]:::victory
            end

            F_DANANG -.-> RES_LIENTRI
            F_NAMKY -.-> RES_TRUONGDINH
            RES_TRUONGDINH -.-> RES_TRUNGTRUC
            F_BACKY1 -.-> RES_CAUGIAY1
            F_BACKY2 -.-> RES_CAUGIAY2
        end

        VNGUYEN_4 --> F_DANANG
        VNGUYEN_4 --> RES_LIENTRI

        %% PARALLEL TIẾP THEO: VUA BÙ NHÌN VS PHONG TRÀO CẦN VƯƠNG & KHÁNG PHÁP
        subgraph Sub9_CanVuongSplit ["PHONG TRÀO CẦN VƯƠNG & PHONG TRÀO ĐẤU TRANH ĐẦU TK XX (1885 - 1945)"]
            subgraph Sub9_TrieuDinhBuNhin ["TRIỀU ĐÌNH BÙ NHÌN DO PHÁP THIẾT LẬP"]
                VNGUYEN_567["Thời kỳ 'Tứ nguyệt tam vương' (1883 - 1884):<br>Dục Đức (3 ngày) -> Hiệp Hòa (4 tháng) -> Kiến Phúc (1883-1884)"]:::crisis
                --> VNGUYEN_8["8. HÀM NGHI (1884 - 1885):<br>Tôn Thất Thuyết tập kích kinh thành Huế (05/07/1885) bất thành.<br>Rước vua ra Tân Sở (Quảng Trị) ban 'CHIẾU CẦN VƯƠNG' kêu gọi toàn dân phò vua cứu nước"]:::hero
                --> VNGUYEN_9["9. Đồng Khánh (1885 - 1889: Vua bù nhìn do Pháp đặt lên ngôi)"]:::crisis
                --> VNGUYEN_10["10. Thành Thái (1889 - 1907: Vua yêu nước chống Pháp, bị đày sang Réunion)"]:::monarch
                --> VNGUYEN_11["11. Duy Tân (1907 - 1916: Cùng Thái Phiên khởi nghĩa vũ trang, bị đày sang Réunion)"]:::monarch
                --> VNGUYEN_12["12. Khải Định (1916 - 1925: Thân Pháp hoàn toàn)"]:::monarch
                --> VNGUYEN_13["13. BẢO ĐẠI (1926 - 1945):<br>Vị hoàng đế cuối cùng của chế độ phong kiến Việt Nam"]:::monarch
            end

            subgraph Sub9_PhongTraoYeuNuoc ["CÁC CUỘC KHỞI NGHĨA VŨ TRANG & PHONG TRÀO CÁCH MẠNG"]
                CV_WARS["CÁC CUỘC KHỞI NGHĨA CẦN VƯƠNG VŨ TRANG (1885 - 1913):<br>- Ba Đình (1886 - 1887: Đinh Công Tráng, Phạm Bành)<br>- Bãi Sậy (1883 - 1892: Nguyễn Thiện Thuật)<br>- Hương Khê (1885 - 1896: Phan Đình Phùng, Cao Thắng tự chế tạo súng kiểu Pháp)<br>- Khởi nghĩa Yên Thế (1884 - 1913: Hoàng Hoa Thám - 'Hùm xám Yên Thế' 30 năm kháng cự kiên cường)"]:::war
                --> XX_MOVEMENTS["PHONG TRÀO YÊU NƯỚC ĐẦU THẾ KỶ XX:<br>- Phong trào Đông Du (Phan Bội Châu) & Duy Tân (Phan Châu Trinh)<br>- Khởi nghĩa Thái Nguyên (1917: Đội Cấn) & Yên Bái (1930: Nguyễn Thái Học - VNQDĐ)<br>- 03/02/1930: NGUYỄN ÁI QUỐC SÁNG LẬP ĐẢNG CỘNG SẢN VIỆT NAM<br>- Phong trào Xô Viết Nghệ Tĩnh (1930-1931), Nam Kỳ & Bắc Sơn (1940: Cờ đỏ sao vàng xuất hiện)<br>- 09/03/1945: Nhật đảo chính Pháp; Mặt trận Việt Minh phát động cao trào kháng Nhật cứu nước"]:::hero
                --> XX_CMT8["TỔNG KHỞI NGHĨA CÁCH MẠNG THÁNG TÁM (19/08/1945):<br>Toàn dân tộc vùng lên giành trọn chính quyền ở Hà Nội (19/08), Huế (23/08), Sài Gòn (25/08)"]:::victory
            end

            VNGUYEN_8 --> CV_WARS
        end

        F_THUANAN --> VNGUYEN_567

        %% KẾT THÚC VƯƠNG TRIỀU NGUYỄN
        XX_CMT8 --> XX_THOAIVI["CHIẾU THOÁI VỊ TẠI NGỌ MÔN (30/08/1945):<br>Vua Bảo Đại trao ấn vàng kiếm ngọc cho chính quyền Việt Minh: 'Trẫm thà làm dân một nước độc lập hơn làm vua một nước nô lệ'.<br>CHẤM DỨT HOÀN TOÀN TRIỀU ĐẠI NHÀ NGUYỄN, KHÉP LẠI HƠN 1.000 NĂM CHẾ ĐỘ PHONG KIẾN"]:::monarch
        VNGUYEN_13 --> XX_THOAIVI
    end

    %% =========================================================================
    %% 10. KHÁNG CHIẾN CHỐNG THỰC DÂN PHÁP (1945 - 1954)
    %% PARALLEL: CHÍNH QUYỀN KHÁNG CHIẾN VNDCCH VS LIÊN QUÂN PHÁP & QUỐC GIA VIỆT NAM
    %% =========================================================================
    subgraph Sub10_ChongPhap ["10. KHÁNG CHIẾN CHỐNG THỰC DÂN PHÁP (1945 - 1954)"]
        P10_START["TUYÊN NGÔN ĐỘC LẬP (02/09/1945):<br>Chủ tịch Hồ Chí Minh khai sinh nước VIỆT NAM DÂN CHỦ CỘNG HÒA.<br>23/09/1945: Nam Bộ kháng chiến bùng nổ khi thực dân Pháp nổ súng tái chiếm Sài Gòn"]:::victory
        --> P10_TOANQUOC["LỜI KÊU GỌI TOÀN QUỐC KHÁNG CHIẾN (19/12/1946):<br>'Chúng ta thà hy sinh tất cả chứ nhất định không chịu mất nước, nhất định không chịu làm nô lệ!'<br>Trận chiến 60 ngày đêm giam chân địch trong lòng Thủ đô Hà Nội của Trung đoàn Thủ đô"]:::victory

        %% Hai tuyến đối đầu song song: Chiến lược quân sự Pháp vs Đòn tiến công của VNDCCH
        subgraph Sub10_ChienDichDoiDau ["CÁC KẾ HOẠCH QUÂN SỰ PHÁP BỊ ĐẬP TAN TRÊN CHIẾN TRƯỜNG"]
            P10_VB1947["BẺ GÃY KẾ HOẠCH LÉA - CHIẾN DỊCH VIỆT BẮC THU - ĐÔNG (1947):<br>Valluy điều 12.000 quân dù và thủy bộ bao vây Việt Bắc hòng xóa sổ đầu não kháng chiến.<br>Pháo binh Sông Lô, Đoan Hùng bắn chìm tàu chiến; Phục kích Đèo Bông Lau diệt xe cơ giới.<br>Bảo vệ an toàn cơ quan đầu não kháng chiến; Pháp phá sản chiến lược đánh nhanh thắng nhanh"]:::victory
            --> P10_BIENGIOI["PHÁ VỠ KẾ HOẠCH RƠ-VE - CHIẾN DỊCH BIÊN GIỚI THU - ĐÔNG (1950):<br>Tiêu diệt cụm cứ điểm Đông Khê (La Văn Cầu nhờ chặt cánh tay phá bom); tiêu diệt 2 binh đoàn Le Page & Charton tại Cốc Xá.<br>Giải phóng 750km biên giới Việt - Trung; giành hoàn toàn quyền chủ động chiến lược trên chiến trường chính Bắc Bộ"]:::victory
            --> P10_TIENCONG["ĐÁNH BẠI KẾ HOẠCH DE LATTRE DE TASSIGNY (1950 - 1953):<br>Chiến dịch Trần Hưng Đạo, Hoàng Hoa Thám, Quang Trung (1951); Chiến dịch Hòa Bình (1951-1952);<br>Chiến dịch Tây Bắc (1952: giải phóng Nghĩa Lộ); Chiến dịch Thượng Lào (1953: giải phóng Sầm Nưa)"]:::campaign
            --> P10_NAVARRE["ĐÁNH BẠI KẾ HOẠCH NAVARRE & ĐÔNG - XUÂN 1953 - 1954:<br>Navarre xây Điện Biên Phủ thành 'Pháo đài bất khả xâm phạm' với 16.200 quân viễn chinh và 49 cứ điểm.<br>Bộ Tổng tư lệnh mở 5 đòn tiến công chiến lược phân tán khối cơ động của Navarre ra khắp Đông Dương"]:::campaign
            --> P10_DBP["ĐẠI CHIẾN DỊCH ĐIỆN BIÊN PHỦ (13/03 - 07/05/1954 - 56 NGÀY ĐÊM):<br>- Đợt 1 (13 - 17/03): Tiêu diệt Him Lam (Phan Đình Giót lấp lỗ châu mai), Độc Lập, Bản Kéo.<br>- Đợt 2 (30/03 - 30/04): Đánh chiếm các đồi phía Đông A1, C1; đào hào siết chặt sân bay Mường Thanh.<br>- Đợt 3 (01 - 07/05): Kích nổ khối bộc phá nghìn cân đồi A1, tổng công kích vào Sở chỉ huy Mường Thanh.<br>Chiều 07/05/1954: Bắt sống Tướng De Castries cùng toàn bộ Bộ chỉ huy tập đoàn cứ điểm.<br>CHIẾN THẮNG ĐIỆN BIÊN PHỦ 'LỪNG LẪY NĂM CHÂU, CHẤN ĐỘNG ĐỊA CẦU'"]:::victory
        end

        P10_TOANQUOC --> P10_VB1947

        P10_DBP --> P10_GENEVE["HIỆP ĐỊNH GENÈVE (21/07/1954):<br>Pháp công nhận độc lập, chủ quyền, thống nhất và toàn vẹn lãnh thổ của Việt Nam.<br>Buộc quân đội Pháp rút hết; Miền Bắc hoàn toàn giải phóng; Vĩ tuyến 17 tạm thời làm giới tuyến quân sự"]:::treaty
    end

    XX_THOAIVI --> P10_START

    %% =========================================================================
    %% 11. KHÁNG CHIẾN CHỐNG MỸ (1954 - 1975): HAI MIỀN ĐÁNH BẠI 4 CHIẾN LƯỢC MỸ
    %% PARALLEL: HẬU PHƯƠNG LỚN MIỀN BẮC VS TIỀN TUYẾN LỚN MIỀN NAM
    %% =========================================================================
    subgraph Sub11_ChongMy ["11. KHÁNG CHIẾN CHỐNG MỸ CỨU NƯỚC: HAI MIỀN THỐNG NHẤT NON SÔNG (1954 - 1975)"]

        subgraph Sub11_HaiMienSplit ["CỤC DIỆN HAI MIỀN THỰC HIỆN HAI NHIỆM VỤ CHIẾN LƯỢC SONG SONG"]
            %% MIỀN BẮC
            subgraph Sub11_MienBac ["HẬU PHƯƠNG LỚN MIỀN BẮC XÃ HỘI CHỦ NGHĨA"]
                MB_HAUPHUONG["XÂY DỰNG CNXH & CHI VIỆN TUYẾN LỬA (1954 - 1975):<br>- Mở Đường Trường Sơn 559 trên bộ và Đường 759 trên biển (Đoàn tàu Không số).<br>- 'Thóc không thiếu một cân, quân không thiếu một người', chi viện vũ khí và sức người cho miền Nam"]:::modern
                --> MB_CHONGPHASAN["ĐÁNH BẠI CHIẾN TRANH PHÁ HOẠI CỦA KHÔNG QUÂN MỸ:<br>- Chiến dịch Sấm Rền (Rolling Thunder 1965-1968): Bắn rơi hàng nghìn máy bay giặc Mỹ.<br>- Ngày 03/09/1969: CHỦ TỊCH HỒ CHÍ MINH QUA ĐỜI - Để lại Di chúc thiêng liêng: 'Đánh cho Mỹ cút, Đánh cho ngụy nhào'"]:::war
                --> MB_DIENBIEN_AIR["ĐẠI THẮNG 'ĐIỆN BIÊN PHỦ TRÊN KHÔNG' (18 - 30/12/1972):<br>Hà Nội, Hải Phòng đập tan chiến dịch Linebacker II của Nixon; bắn rơi 81 máy bay Mỹ (34 pháo đài bay B-52).<br>Buộc Mỹ phải ký Hiệp định Paris rút toàn bộ quân viễn chinh về nước"]:::victory
            end

            %% MIỀN NAM
            subgraph Sub11_MienNam ["TIỀN TUYẾN LỚN MIỀN NAM ANH DŨNG CHIẾN ĐẤU"]
                MN_DONPHUONG["1. ĐÁNH BẠI 'CHIẾN TRANH ĐƠN PHƯƠNG' CỦA MỸ - DIỆM (1954 - 1960):<br>Mỹ dựng Ngô Đình Diệm xé Hiệp định Genève, ban hành Đạo luật 10/59 lê máy chém khắp miền Nam.<br>PHONG TRÀO ĐỒNG KHỞI (17/01/1960 - Mỏ Cày, Bến Tre) của 'Đội quân tóc dài' Nguyễn Thị Định.<br>20/12/1960: Thành lập MẶT TRẬN DÂN TỘC GIẢI PHÓNG MIỀN NAM VIỆT NAM"]:::victory
                --> MN_DACBIET["2. ĐÁNH BẠI 'CHIẾN TRANH ĐẶC BIỆT' (1961 - 1965):<br>Công thức: 'Quân đội Sài Gòn + Cố vấn, vũ khí Mỹ + Ấp chiến lược + Trực thăng vận & Thiết xa vận'.<br>ĐẠI THẮNG ẤP BẮC (02/01/1963) phá tan chiến thuật trực thăng vận và xe M113.<br>Đảo chính Diệm - Nhu (1963); Chuỗi chiến thắng tiêu diệt chiến đoàn ngụy: Bình Giã, Ba Gia, Đồng Xoài (1965)"]:::victory
                --> MN_CUCTBO["3. ĐÁNH BẠI 'CHIẾN TRANH CỤC BỘ' & MẬU THÂN 1968 (1965 - 1968):<br>Mỹ đổ hơn 54 vạn quân viễn chinh vào miền Nam.<br>- Thắng Mỹ trận đầu: Núi Thành (05/1965) & Vạn Tường (08/1965).<br>- Thung lũng Ia Đrăng (11/1965) đánh tan kỵ binh không vận Mỹ; Bẻ gãy Junction City (1967).<br>TỔNG TIẾN CÔNG VÀ NỔI DẬY TẾT MẬU THÂN 1968:<br>Đồng loạt đánh Tòa Đại sứ Mỹ, Dinh Độc Lập; buộc Johnson ngừng ném bom miền Bắc và ngồi vào đàm phán Paris"]:::victory
                --> MN_VIETNAMHOA["4. ĐÁNH BẠI 'VIỆT NAM HÓA CHIẾN TRANH' (1969 - 1973):<br>Đánh bại cuộc hành quân Lam Sơn 719 Đường 9 - Nam Lào (1971).<br>Tiến công chiến lược 1972 & Cuộc chiến đấu 81 ngày đêm bảo vệ Thành cổ Quảng Trị kiên cường"]:::victory
            end

            MB_HAUPHUONG -.->|"Chi viện liên tục sức người, vũ khí qua đường Trường Sơn"| MN_DACBIET
            MN_CUCTBO -.->|"Tết Mậu Thân 1968 buộc Mỹ đàm phán; Mỹ điên cuồng ném bom miền Bắc trả đũa"| MB_CHONGPHASAN
        end

        MN_VIETNAMHOA --> P11_PARIS["HIỆP ĐỊNH PARIS (27/01/1973):<br>Mỹ cam kết tôn trọng độc lập, chủ quyền, toàn vẹn lãnh thổ Việt Nam; rút sạch quân viễn chinh về nước.<br>Hoàn thành mục tiêu 'ĐÁNH CHO MỸ CÚT'"]:::treaty
        MB_DIENBIEN_AIR --> P11_PARIS

        P11_PARIS --> P11_DAITHANG1975["5. ĐẠI THẮNG MÙA XUÂN 1975 - GIẢI PHÓNG HOÀN TOÀN MIỀN NAM ('ĐÁNH CHO NGỤY NHÀO'):<br>- Chiến thắng Phước Long (01/1975) thử lửa đòn trinh sát chiến lược.<br>- CHIẾN DỊCH TÂY NGUYÊN (04 - 24/03): Đột phá then chốt Buôn Ma Thuột (10/03), tiêu diệt toàn bộ QĐ2 ngụy.<br>- CHIẾN DỊCH HUẾ - ĐÀ NẴNG (21 - 29/03): Giải phóng Huế (26/03), Đà Nẵng (29/03), xóa sổ QĐ1 ngụy.<br>- Giải phóng các đảo thuộc Quần đảo Trường Sa (14 - 29/04/1975).<br>- Đập tan 'cánh cửa thép' Xuân Lộc (09 - 21/04/1975).<br>CHIẾN DỊCH HỒ CHÍ MINH LỊCH SỬ (26 - 30/04/1975):<br>5 cánh quân thần tốc giải phóng Sài Gòn. 10h45 ngày 30/04: Xe tăng 390 & 843 húc đổ cổng Dinh Độc Lập.<br>11h30 ngày 30/04/1975: Cờ Giải phóng tung bay trên nóc Dinh Độc Lập; Tổng thống Dương Văn Minh đầu hàng vô điều kiện.<br>NON SÔNG THỐNG NHẤT TRỌN VẸN MỘT DẢI"]:::victory
    end

    P10_GENEVE -->|"Chia cắt tại vĩ tuyến 17: Miền Bắc hoàn toàn giải phóng, bắt tay xây dựng CNXH làm hậu phương lớn"| MB_HAUPHUONG
    P10_GENEVE -->|"Mỹ dựng chính quyền Diệm xé bỏ Hiệp định Genève; đồng bào miền Nam anh dũng đứng lên đấu tranh"| MN_DONPHUONG

    %% =========================================================================
    %% 12. CÁC CUỘC CHIẾN TRANH BẢO VỆ BIÊN GIỚI & BIỂN ĐẢO TỔ QUỐC (1975 - 1989)
    %% =========================================================================
    subgraph Sub12_BienGioi ["12. CÁC CUỘC CHIẾN TRANH BẢO VỆ BIÊN GIỚI & BIỂN ĐẢO TỔ QUỐC (1975 - 1989)"]
        P12_UNIFY["NƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM (02/07/1976):<br>Quốc hội khóa VI thống nhất đất nước về mặt nhà nước, đặt tên nước và xác định thủ đô Hà Nội"]:::victory
        --> P12_TAYNAM["CHIẾN TRANH BẢO VỆ BIÊN GIỚI TÂY NAM & DIỆT CHỦNG KHMER ĐỎ (1977 - 1979):<br>- Tập đoàn Pol Pot xâm lấn biên giới, thảm sát đồng bào tại Thổ Chu và Ba Chúc (An Giang).<br>- 23/12/1978: Quân đội nhân dân Việt Nam mở cuộc tổng phản công quét sạch giặc khỏi biên cương.<br>- 07/01/1979: Phối hợp cùng quân dân Campuchia giải phóng Phnôm Pênh, cứu nhân dân Campuchia thoát họa diệt chủng"]:::victory
        --> P12_BAC1979["CUỘC CHIẾN ĐẤU BẢO VỆ BIÊN GIỚI PHÍA BẮC (17/02 - 18/03/1979):<br>Hơn 60 vạn quân tràn qua toàn tuyến biên giới 6 tỉnh phía Bắc: Lai Châu, Lào Cai, Hà Giang, Cao Bằng, Lạng Sơn, Quảng Ninh.<br>Quân và dân 6 tỉnh biên giới chiến đấu kiên cường tại Đồng Đăng, Trà Lĩnh, Phong Thổ; bẻ gãy kế hoạch đánh nhanh thắng nhanh.<br>05/03/1979: Chủ tịch nước Tôn Đức Thắng ra Lệnh Tổng động viên; đối phương tuyên bố rút quân"]:::war
        --> P12_VIXUYEN["MẶT TRẬN VỊ XUYÊN - HÀ GIANG 'LÒ VÔI THẾ KỶ' (1984 - 1989):<br>Chiến đấu ác liệt giữ vững từng tấc đất thiêng liêng ở các điểm cao 1509, 772, 685, Đồi Đài, Cửa khẩu Thanh Thủy.<br>Lời thề bất tử khắc trên báng súng của Liệt sĩ Nguyễn Viết Ninh: 'SỐNG BÁM ĐÁ ĐÁNH GIẶC, CHẾT HÓA ĐÁ BẤT TỬ'"]:::hero
        --> P12_GACMA["HẢI CHIẾN TRƯỜNG SA & 'VÒNG TRÒN BẤT TỬ' GẠC MA (14/03/1988):<br>Hải quân Trung Quốc nổ súng tấn công các chiến sĩ công binh tại cụm đảo chìm Gạc Ma, Cô Lin, Len Đao.<br>64 chiến sĩ Hải quân kết thành 'VÒNG TRÒN BẤT TỬ' bảo vệ lá cờ Tổ quốc và anh dũng hy sinh.<br>Thuyền trưởng Vũ Huy Lễ chỉ huy tàu HQ-505 ủi bãi giữ vững đảo Cô Lin; bảo vệ chủ quyền Cô Lin và Len Đao tại Quần đảo Trường Sa"]:::hero
    end

    P11_DAITHANG1975 --> P12_UNIFY

    %% =========================================================================
    %% 13. KỶ NGUYÊN ĐỔI MỚI, HỘI NHẬP SÂU RỘNG & VƯƠN MÌNH (1986 - 2026+)
    %% =========================================================================
    subgraph Sub13_DoiMoi ["13. KỶ NGUYÊN ĐỔI MỚI, HỘI NHẬP SÂU RỘNG & VƯƠN MÌNH CỦA DÂN TỘC (1986 - 2026+)"]
        P13_DM1986["ĐẠI HỘI VI KHỞI XƯỚNG ĐƯỜNG LỐI ĐỔI MỚI TOÀN DIỆN (12/1986):<br>Xóa bỏ bao cấp, phát triển nền kinh tế thị trường định hướng XHCN.<br>Năm 1989: Rút hết quân tình nguyện khỏi Campuchia, phá vỡ thế bao vây cấm vận quốc tế"]:::modern
        --> P13_BINHTHUONG["BÌNH THƯỜNG HÓA QUAN HỆ QUỐC TẾ (1991 - 1995):<br>- 1991: Bình thường hóa quan hệ Việt Nam - Trung Quốc.<br>- 1994: Mỹ dỡ bỏ cấm vận; 11/07/1995: Bình thường hóa quan hệ Việt Nam - Hoa Kỳ.<br>- 28/07/1995: Việt Nam chính thức gia nhập ASEAN"]:::modern
        --> P13_HOINHAP["HỘI NHẬP KINH TẾ QUỐC TẾ SÂU RỘNG (1998 - 2020):<br>- 1998: Gia nhập APEC; 2001: Ký Hiệp định Thương mại Việt - Mỹ (BTA).<br>- 11/01/2007: Gia nhập WTO, trở thành thành viên thứ 150.<br>- Thực thi các FTA thế hệ mới: CPTPP (2018), EVFTA (2020), RCEP (2020)"]:::modern
        --> P13_VUONMINH["KỶ NGUYÊN VƯƠN MÌNH CỦA DÂN TỘC VIỆT NAM (2021 - 2026+):<br>- Thiết lập mạng lưới Đối tác Chiến lược Toàn diện với các cường quốc hàng đầu thế giới.<br>- Hai lần đảm nhiệm thành công trọng trách Ủy viên không thường trực Hội đồng Bảo an LHQ.<br>- Kiên quyết, kiên trì bảo vệ vững chắc chủ quyền biển đảo theo Công ước LHQ về Luật Biển UNCLOS 1982.<br>- Đẩy mạnh chuyển đổi số quốc gia, công nghiệp bán dẫn, kinh tế xanh, dự án đường sắt tốc độ cao Bắc - Nam.<br>TỰ HÀO LỊCH SỬ - VỮNG BƯỚC VÀO KỶ NGUYÊN PHỒN VINH, THỊNH VƯỢNG"]:::modern
    end

    P12_GACMA -->|"Cùng với nhiệm vụ bảo vệ chủ quyền biên cương - biển đảo, Đại hội VI (12/1986) mở ra đường lối Đổi Mới toàn diện"| P13_DM1986
```
