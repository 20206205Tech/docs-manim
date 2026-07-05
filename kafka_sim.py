from manim import *
import json

class KafkaArchitecture(Scene):
    def construct(self):
        # 1. CẤU HÌNH CÁC NODE
        payment_svc = Text("Payment Service", font_size=20).shift(LEFT * 4.5)
        kafka = Text("Kafka Topic", font_size=24, color=YELLOW)
        document_svc = Text("Document Service", font_size=20).shift(RIGHT * 4.5 + UP * 2)
        conversation_svc = Text("Conversation Service", font_size=20).shift(RIGHT * 4.5 + DOWN * 2)

        # Khung bao quanh các Service
        box_p = SurroundingRectangle(payment_svc, color=BLUE, corner_radius=0.1)
        box_k = SurroundingRectangle(kafka, color=YELLOW, corner_radius=0.1)
        box_d = SurroundingRectangle(document_svc, color=GREEN, corner_radius=0.1)
        box_c = SurroundingRectangle(conversation_svc, color=GREEN, corner_radius=0.1)

        # Mũi tên kết nối
        arrow_p_k = Arrow(box_p.get_right(), box_k.get_left(), buff=0.1)
        arrow_k_d = Arrow(box_k.get_right(), box_d.get_left(), buff=0.1)
        arrow_k_c = Arrow(box_k.get_right(), box_c.get_left(), buff=0.1)

        # 2. CHUẨN BỊ NỘI DUNG SỰ KIỆN (JSON)
        event_name = Text("SubscriptionPurchasedEvent", font_size=18, color=RED).next_to(box_p, UP)
        
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
        packet = Rectangle(width=0.6, height=0.4, color=RED, fill_opacity=0.8)
        packet_label = Text("Event", font_size=10).move_to(packet.get_center())
        data_packet = VGroup(packet, packet_label).move_to(box_p.get_right())

        self.play(
            ReplacementTransform(json_group, data_packet),
            event_name.animate.scale(0.5).next_to(data_packet, UP, buff=0.1),
            run_time=1.5
        )

        # Bước 3: Gửi tới Kafka
        self.play(data_packet.animate.move_to(box_k.get_center()), event_name.animate.move_to(box_k.get_top() + UP*0.2), run_time=1.5)
        self.play(Flash(box_k, color=RED))
        self.wait(0.5)

        # Bước 4: Kafka phân phối cho 2 Consumers (Document & Conversation)
        data_packet_copy = data_packet.copy()
        event_name_copy = event_name.copy()

        self.play(
            # Gói 1 bay lên Document
            data_packet.animate.move_to(box_d.get_left() + LEFT*0.3),
            event_name.animate.next_to(box_d, UP, buff=0.1),
            # Gói 2 bay xuống Conversation
            data_packet_copy.animate.move_to(box_c.get_left() + LEFT*0.3),
            event_name_copy.animate.next_to(box_c, DOWN, buff=0.1),
            run_time=2
        )

        # Bước 5: Báo hiệu nhận thành công và xử lý
        self.play(
            Flash(box_d, color=GREEN),
            Flash(box_c, color=GREEN),
            FadeOut(data_packet),
            FadeOut(data_packet_copy)
        )

        self.wait(3)