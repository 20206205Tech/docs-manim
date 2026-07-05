from manim import *

class KafkaArchitecture(Scene):
    def construct(self):
        # 1. KHỞI TẠO CÁC ĐỐI TƯỢNG (Mobjects)
        # Đổi tên các Service theo nghiệp vụ thực tế
        payment_svc = Text("Payment Service", font_size=20).shift(LEFT * 4)
        kafka = Text("Kafka Topic", font_size=24, color=YELLOW)
        document_svc = Text("Document Service", font_size=20).shift(RIGHT * 4 + UP * 2)
        conversation_svc = Text("Conversation Service", font_size=20).shift(RIGHT * 4 + DOWN * 2)

        # Tạo khung bao quanh Text
        box_payment = SurroundingRectangle(payment_svc, color=BLUE, corner_radius=0.1)
        box_k = SurroundingRectangle(kafka, color=YELLOW, corner_radius=0.1)
        box_document = SurroundingRectangle(document_svc, color=GREEN, corner_radius=0.1)
        box_conversation = SurroundingRectangle(conversation_svc, color=GREEN, corner_radius=0.1)

        # Tạo mũi tên luồng dữ liệu
        arrow_1_k = Arrow(box_payment.get_right(), box_k.get_left(), buff=0.1)
        arrow_k_2 = Arrow(box_k.get_right(), box_document.get_left(), buff=0.1)
        arrow_k_3 = Arrow(box_k.get_right(), box_conversation.get_left(), buff=0.1)

        # 2. XUẤT HIỆN TRÊN MÀN HÌNH (Animations)
        # Nhóm các đối tượng lại để dễ dàng gọi lệnh hiển thị
        self.play(FadeIn(VGroup(
            payment_svc, box_payment, 
            kafka, box_k, 
            document_svc, box_document, 
            conversation_svc, box_conversation
        )))
        self.play(Create(VGroup(arrow_1_k, arrow_k_2, arrow_k_3)))
        self.wait(1)

        # 3. MÔ PHỎNG LUỒNG SỰ KIỆN (Data Flow)
        # Ví dụ sự kiện "Payment_Success"
        event_msg = Dot(color=RED, radius=0.15)
        event_msg.move_to(box_payment.get_right())

        # Giai đoạn 1: Payment Service gửi tới Kafka
        self.play(FadeIn(event_msg))
        self.play(event_msg.animate.move_to(box_k.get_center()), run_time=1.5)
        
        # Nhấp nháy tại Kafka để báo hiệu đã lưu trữ
        self.play(Flash(box_k, color=RED, flash_radius=1.5))

        # Giai đoạn 2: Kafka phân phối cho Document (tạo hóa đơn) và Conversation (gửi tin nhắn)
        event_msg_copy = event_msg.copy()
        
        self.play(
            event_msg.animate.move_to(box_document.get_left()),
            event_msg_copy.animate.move_to(box_conversation.get_left()),
            run_time=1.5
        )

        # Nhấp nháy màu xanh để báo hiệu 2 service đã nhận được tin nhắn và xử lý
        self.play(Flash(box_document, color=GREEN), Flash(box_conversation, color=GREEN))
        self.play(FadeOut(event_msg), FadeOut(event_msg_copy))
        
        # Dừng lại 2 giây trước khi kết thúc video
        self.wait(2)