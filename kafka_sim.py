from manim import *

class KafkaArchitecture(Scene):
    def construct(self):
        # 1. KHỞI TẠO CÁC ĐỐI TƯỢNG (Mobjects)
        # Tạo Text
        service_1 = Text("Service 1 (Producer)", font_size=20).shift(LEFT * 4)
        kafka = Text("Kafka Topic", font_size=24, color=YELLOW)
        service_2 = Text("Service 2 (Consumer)", font_size=20).shift(RIGHT * 4 + UP * 2)
        service_3 = Text("Service 3 (Consumer)", font_size=20).shift(RIGHT * 4 + DOWN * 2)

        # Tạo khung bao quanh Text
        box1 = SurroundingRectangle(service_1, color=BLUE, corner_radius=0.1)
        box_k = SurroundingRectangle(kafka, color=YELLOW, corner_radius=0.1)
        box2 = SurroundingRectangle(service_2, color=GREEN, corner_radius=0.1)
        box3 = SurroundingRectangle(service_3, color=GREEN, corner_radius=0.1)

        # Tạo mũi tên luồng dữ liệu
        arrow_1_k = Arrow(box1.get_right(), box_k.get_left(), buff=0.1)
        arrow_k_2 = Arrow(box_k.get_right(), box2.get_left(), buff=0.1)
        arrow_k_3 = Arrow(box_k.get_right(), box3.get_left(), buff=0.1)

        # 2. XUẤT HIỆN TRÊN MÀN HÌNH (Animations)
        # Dùng FadeIn cho các cụm Node và Create cho mũi tên
        self.play(FadeIn(VGroup(service_1, box1, kafka, box_k, service_2, box2, service_3, box3)))
        self.play(Create(VGroup(arrow_1_k, arrow_k_2, arrow_k_3)))
        self.wait(1)

        # 3. MÔ PHỎNG LUỒNG SỰ KIỆN (Data Flow)
        event_msg = Dot(color=RED, radius=0.15)
        event_msg.move_to(box1.get_right())

        # Giai đoạn 1: Service 1 gửi tới Kafka
        self.play(FadeIn(event_msg))
        self.play(event_msg.animate.move_to(box_k.get_center()), run_time=1.5)
        
        # Nhấp nháy tại Kafka để báo hiệu đã nhận
        self.play(Flash(box_k, color=RED, flash_radius=1.5))

        # Giai đoạn 2: Kafka phân phối sự kiện cho 2 Consumer
        # Nhân bản dot thành 2 để bay về 2 hướng
        event_msg_copy = event_msg.copy()
        
        self.play(
            event_msg.animate.move_to(box2.get_left()),
            event_msg_copy.animate.move_to(box3.get_left()),
            run_time=1.5
        )

        # Biến mất sau khi Service 2, 3 nhận được
        self.play(Flash(box2, color=GREEN), Flash(box3, color=GREEN))
        self.play(FadeOut(event_msg), FadeOut(event_msg_copy))
        self.wait(2)