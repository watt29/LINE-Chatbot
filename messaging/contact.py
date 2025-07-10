from linebot.models import (
    QuickReplyButton,
    MessageAction,
    TextSendMessage,
    QuickReply,
)
from config import line_bot_api

def send_contact_admin_message(reply_token):
    message = TextSendMessage(
        text="ยินดีค่ะ! คุณลูกค้าต้องการสอบถามเรื่องอะไรเป็นพิเศษคะ? สามารถพิมพ์ข้อความทิ้งไว้ได้เลยค่ะ\n\nแอดมินจะรีบเข้ามาตอบกลับโดยเร็วที่สุดค่ะ 😊\n\nหรือหากต้องการความช่วยเหลือเร่งด่วน สามารถติดต่อได้ที่เบอร์ 📞 099-999-9999 หรือแอดไลน์ @maharat.admin ได้เลยนะคะ",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า")),
                QuickReplyButton(
                    action=MessageAction(label="ตรวจสอบสถานะ 📦", text="ตรวจสอบสถานะ")
                ),
                QuickReplyButton(
                    action=MessageAction(label="วิธีชำระเงิน 💰", text="วิธีชำระเงิน")
                ),
            ]
        ),
    )
    line_bot_api.reply_message(reply_token, message)
