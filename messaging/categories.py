from linebot.models import (
    QuickReplyButton,
    MessageAction,
    TextSendMessage,
    QuickReply,
)
from config import line_bot_api

def send_category_quick_reply(reply_token, categories):
    quick_reply_buttons = [
        QuickReplyButton(action=MessageAction(label=cat, text=cat)) for cat in categories
    ]
    message = TextSendMessage(
        text="สนใจสินค้าประเภทไหนเป็นพิเศษคะ? หรือเลือกสอบถามข้อมูลด้านล่างได้เลยค่ะ ✨",
        quick_reply=QuickReply(items=quick_reply_buttons),
    )
    line_bot_api.reply_message(reply_token, message)
