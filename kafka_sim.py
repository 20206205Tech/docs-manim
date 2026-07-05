from manim import *
import json

class KafkaArchitecture(Scene):
    def construct(self):
        # 1. CẤU HÌNH CÁC NODE BAN ĐẦU (Giao diện luồng Kafka)
        payment_svc = Text("Payment Service", font_size=20).shift(LEFT * 4.5)
        kafka = Text("Kafka Topic", font_size=24, color=YELLOW)
        document_svc = Text("Document Service", font_size=20).shift(RIGHT * 4.5 + UP * 2)
        conversation_svc = Text("Conversation Service", font_size=20).shift(RIGHT * 4.5 + DOWN * 2)

        box_p = SurroundingRectangle(payment_svc, color=BLUE, corner_radius=0.1)
        box_k = SurroundingRectangle(kafka, color=YELLOW, corner_radius=0.1)
        box_d = SurroundingRectangle(document_svc, color=GREEN, corner_radius=0.1)
        box_c = SurroundingRectangle(conversation_svc, color=GREEN, corner_radius=0.1)

        arrow_p_k = Arrow(box_p.get_right(), box_k.get_left(), buff=0.1)
        arrow_k_d = Arrow(box_k.get_right(), box_d.get_left(), buff=0.1)
        arrow_k_c = Arrow(box_k.get_right(), box_c.get_left(), buff=0.1)

        # Gom các phần tử giao diện cũ lại để xóa đồng loạt sau này
        old_kafka_ui = VGroup(
            payment_svc, box_p, 
            kafka, box_k, 
            conversation_svc, box_c, 
            arrow_p_k, arrow_k_d, arrow_k_c
        )

        # 2. CHUẨN BỊ NỘI DUNG SỰ KIỆN (JSON)
        event_name = Text("SubscriptionPurchasedEvent", font_size=18, color=RED).next_to(box_p, UP)
        
        # json_data = {
        #     "id": "4d2cfae1-...",
        #     "user_id": "b81a248d-...",
        #     "subscription_id": "404e3b95-...",
        #     "is_active": True,
        #     "created_at": "2026-05-19 04:55:05...",
        #     "updated_at": "2026-06-13 10:51:30...",
        #     "period_start": "2026-07-19 04:52:24...",
        #     "period_end": "2026-09-13 10:40:43...",
        #     "version": 5
        # }


        
        json_data = {
            "version": 2,
            "periodEnd": "2026-07-18T05:50:35.450Z",
            "periodStart": "2026-06-16T04:20:13.095Z",
            "planId": "df82eb45-...",
            "userId": "b81a248d-...",
            "subscriptionId": "404e3b95-..."
        }
        
        # Tạo chuỗi JSON định dạng đẹp
        json_str = json.dumps(json_data, indent=2)
        json_display = Text(json_str, font_size=12, font="Consolas").shift(LEFT * 4.5 + DOWN * 1.5)
        json_bg = SurroundingRectangle(json_display, color=GRAY, fill_opacity=0.2, fill_color=BLACK)
        json_group = VGroup(json_bg, json_display)

        # 3. BẮT ĐẦU DIỄN HOẠT
        # Hiển thị các thành phần hệ thống
        self.play(FadeIn(VGroup(payment_svc, box_p, kafka, box_k, document_svc, box_d, conversation_svc, box_c)))
        self.play(Create(VGroup(arrow_p_k, arrow_k_d, arrow_k_c)))
        self.wait(0.5)

        # Bước 1: Payment Service tạo ra Event và JSON
        self.play(Write(event_name))
        self.play(FadeIn(json_group, shift=UP))
        self.wait(2) # Đứng lại cho người xem đọc JSON

        # Bước 2: Thu nhỏ JSON thành một "gói tin" (packet) để gửi đi
        # Ban đầu nhãn gói tin vẫn ghi "Event" như cũ
        # packet = Rectangle(width=0.8, height=0.5, color=RED, fill_opacity=0.8)
        # packet_label = Text("Event", font_size=12).move_to(packet.get_center())
        # packet = Rectangle(width=1.4, height=0.5, color=RED, fill_opacity=0.8)
        # packet_label = Text("Event", font_size=12).move_to(packet.get_center())
        packet = Rectangle(width=0.6, height=0.4, color=RED, fill_opacity=0.8)
        packet_label = Text("Event", font_size=10).move_to(packet.get_center())

        self.play(
            ReplacementTransform(json_group, VGroup(packet, packet_label)),
            event_name.animate.scale(0.5).next_to(packet, UP, buff=0.1),
            run_time=1.5
        )

        # Bước 3: Gửi tới Kafka
        self.play(
            packet.animate.move_to(box_k.get_center()),
            packet_label.animate.move_to(box_k.get_center()),
            event_name.animate.move_to(box_k.get_top() + UP*0.2),
            run_time=1.5
        )
        self.play(Flash(box_k, color=RED))
        self.wait(0.5)

        # Bước 4: Kafka phân phối cho 2 Consumers (Document & Conversation)
        packet_copy = packet.copy()
        packet_label_copy = packet_label.copy()
        event_name_copy = event_name.copy()

        self.play(
            # Gói 1 bay lên Document
            packet.animate.move_to(box_d.get_left() + LEFT*0.5),
            packet_label.animate.move_to(box_d.get_left() + LEFT*0.5),
            event_name.animate.next_to(box_d, UP, buff=0.1),
            # Gói 2 bay xuống Conversation
            packet_copy.animate.move_to(box_c.get_left() + LEFT*0.5),
            packet_label_copy.animate.move_to(box_c.get_left() + LEFT*0.5),
            event_name_copy.animate.next_to(box_c, DOWN, buff=0.1),
            run_time=2
        )
        self.wait(0.5)

        # =========================================================
        # BƯỚC TRANSITION: XÓA GIAO DIỆN CŨ & THU PHÓNG VÀO DATABASE LOGIC
        # =========================================================
        
        # 1. Xóa sạch luồng cũ để giải phóng không gian màn hình
        self.play(
            FadeOut(old_kafka_ui),
            FadeOut(packet_copy),
            FadeOut(packet_label_copy),
            FadeOut(event_name),
            FadeOut(event_name_copy)
        )
        
        # 2. Dịch chuyển Document Service và gói tin sang góc trái, phóng to gói tin
        # Đồng thời biến đổi nhãn từ "Event" thành "version 5" rõ ràng, dễ đọc hơn
        new_packet = Rectangle(width=1.8, height=0.6, color=RED, fill_opacity=0.8).move_to(LEFT * 4 + DOWN * 0.5)
        new_label = Text("version 5", font_size=16).move_to(LEFT * 4 + DOWN * 0.5)
        self.play(
            box_d.animate.move_to(LEFT * 4 + UP * 2),
            document_svc.animate.move_to(LEFT * 4 + UP * 2),
            Transform(packet, new_packet),
            Transform(packet_label, new_label),
            run_time=1.2
        )

        # 3. Vẽ khối DATABASE lớn và tường minh ở trung tâm bên phải
        db_box = Rectangle(width=6.0, height=4.5, color=BLUE).shift(RIGHT * 1.0)
        db_title = Text("DATABASE", font_size=18, color=BLUE).next_to(db_box, UP, buff=0.2)
        
        # Các trường dữ liệu hiện tại trong DB (Đang ở trạng thái cũ: version = 4)
        db_fields = VGroup(
            Text("id: 4d2cfae1-...", font_size=14),
            Text("user_id: b81a248d-...", font_size=14),
            Text("subscription_id: 404e3b95-...", font_size=14),
            Text("is_active: True", font_size=14, color=GREEN),
            Text("created_at: 2026-05-19...", font_size=14),
            Text("updated_at: 2026-06-13...", font_size=14),
            Text("period_start: 2026-07-19...", font_size=14),
            Text("period_end: 2026-09-13...", font_size=14),
            Text("version: 4", font_size=14, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(db_box.get_center())

        db_ui = VGroup(db_box, db_title, db_fields)
        self.play(FadeIn(db_ui))
        self.wait(1)

        # --- KỊCH BẢN 1: SO SÁNH LỚN HƠN (version 5 > version 4) -> CẬP NHẬT ---
        # Chỉ mũi tên so sánh từ Gói tin vào trường Version của Database
        arrow_compare = Arrow(packet.get_right(), db_fields[8].get_left(), color=YELLOW, buff=0.2)
        compare_text = Text("Event(version 5) > DB(version 4) ?", font_size=14, color=YELLOW).next_to(arrow_compare, UP, buff=0.1)
        
        self.play(Create(arrow_compare), Write(compare_text))
        self.wait(1)

        action_text_1 = Text("UPDATE", font_size=16, color=GREEN).next_to(db_box, DOWN, buff=0.4)
        self.play(Write(action_text_1))
        self.wait(1)

        # Tạo trạng thái dữ liệu mới sau khi Update thành công (version: 5)
        db_fields_updated = VGroup(
            Text("id: 4d2cfae1-...", font_size=14),
            Text("user_id: b81a248d-...", font_size=14),
            Text("subscription_id: 404e3b95-...", font_size=14),
            Text("is_active: True", font_size=14, color=GREEN),
            Text("created_at: 2026-05-19...", font_size=14),
            Text("updated_at: 2026-06-13...", font_size=14),
            Text("period_start: 2026-07-19...", font_size=14),
            Text("period_end: 2026-09-13...", font_size=14),
            Text("version: 5", font_size=14, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(db_box.get_center())

        # Thực hiện biến đổi dữ liệu trực quan bên trong Database
        self.play(
            Transform(db_fields, db_fields_updated),
            Flash(db_box, color=GREEN, flash_radius=1.5),
            FadeOut(packet),
            FadeOut(packet_label),
            FadeOut(arrow_compare),
            FadeOut(compare_text),
            run_time=1.5
        )
        self.wait(1.5)
        self.play(FadeOut(action_text_1))

        # --- KỊCH BẢN 2: SO SÁNH NHỎ HƠN HOẶC BẰNG (version 3 <= version 5) -> BỎ QUA ---
        # Giả lập Database đang ở version 5
        db_fields_v5 = VGroup(
            Text("id: 4d2cfae1-...", font_size=14),
            Text("user_id: b81a248d-...", font_size=14),
            Text("subscription_id: 404e3b95-...", font_size=14),
            Text("is_active: True", font_size=14, color=GREEN),
            Text("created_at: 2026-05-19...", font_size=14),
            Text("updated_at: 2026-06-13...", font_size=14),
            Text("period_start: 2026-07-19...", font_size=14),
            Text("period_end: 2026-09-13...", font_size=14),
            Text("version: 5", font_size=14, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(db_box.get_center())

        self.play(
            Transform(db_fields, db_fields_v5),
            run_time=1.2
        )
        self.wait(1)

        # Giả lập một gói tin cũ (version 3) đến muộn xuất hiện ở phía Consumer
        old_packet = Rectangle(width=1.8, height=0.6, color=GRAY, fill_opacity=0.8).move_to(LEFT * 4 + DOWN * 0.5)
        old_label = Text("version 3", font_size=16).move_to(old_packet.get_center())
        old_data_packet = VGroup(old_packet, old_label)

        self.play(FadeIn(old_data_packet))
        
        arrow_compare_2 = Arrow(old_data_packet.get_right(), db_fields[8].get_left(), color=YELLOW, buff=0.2)
        compare_text_2 = Text("Event(version 3) <= DB(version 5) ?", font_size=14, color=YELLOW).next_to(arrow_compare_2, UP, buff=0.1)
        
        self.play(Create(arrow_compare_2), Write(compare_text_2))
        self.wait(1)

        action_text_2 = Text("SKIP", font_size=16, color=RED).next_to(db_box, DOWN, buff=0.4)
        cross_mark = Cross(old_data_packet) # Dấu gạch chéo đỏ đè lên gói tin cũ
        
        self.play(Write(action_text_2), Create(cross_mark))
        self.wait(1.5)

        # Xóa gói tin bị từ chối khỏi bộ nhớ hệ thống
        self.play(
            FadeOut(old_data_packet),
            FadeOut(cross_mark),
            FadeOut(arrow_compare_2),
            FadeOut(compare_text_2),
            FadeOut(action_text_2)
        )
        self.wait(2)