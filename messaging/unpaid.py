from linebot.models import (
    QuickReplyButton,
    MessageAction,
    TextSendMessage,
    QuickReply,
)
from config import line_bot_api, db

def send_unpaid_orders(reply_token, user_id):
    orders_ref = db.reference("orders").order_by_child("userId").equal_to(user_id)
    user_orders = orders_ref.get()

    if not user_orders:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(
                text="ไม่พบรายการสั่งซื้อที่ยังรอชำระเงินของคุณลูกค้าค่ะ 😊",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า"))]
                ),
            ),
        )
        return

    unpaid_orders = [
        order for order in user_orders.values() if order["status"] == "รอชำระเงิน"
    ]

    if not unpaid_orders:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(
                text="คุณไม่มีคำสั่งซื้อที่ยังรอชำระเงินค่ะ ✅",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า"))]
                ),
            ),
        )
        return

    reply_text = "รายการคำสั่งซื้อที่ยังรอชำระเงินของคุณค่ะ:\n"
    for order in unpaid_orders:
        reply_text += f"\n- {order['productName']} (เลขที่: {order['orderId']})\n  สถานะ: ⏳ รอชำระเงิน\n"

    quick_reply_items = [
        QuickReplyButton(
            action=MessageAction(
                label=order["orderId"], text=f"แจ้งโอนเงิน {order['orderId']}"
            )
        )
        for order in unpaid_orders
    ]

    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(
            text=reply_text.strip(),
            quick_reply=QuickReply(
                items=[
                    *quick_reply_items,
                    QuickReplyButton(
                        action=MessageAction(label="วิธีชำระเงิน 💰", text="วิธีชำระเงิน")
                    ),
                    QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า")),
                ]
            ),
        ),
    )
