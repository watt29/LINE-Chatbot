from linebot.models import (
    QuickReplyButton,
    MessageAction,
    TextSendMessage,
    QuickReply,
)
from config import line_bot_api, db
from utils import get_status_emoji

def send_order_status(event, specific_product_name=None):
    user_id = event.source.user_id
    orders_ref = db.reference("orders").order_by_child("userId").equal_to(user_id)
    user_orders = orders_ref.get()

    if not user_orders:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="ไม่พบรายการสั่งซื้อของคุณลูกค้าค่ะ 😔",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า"))]
                ),
            ),
        )
        return

    filtered_orders = [
        order for order in user_orders.values() if order["status"] == "รอชำระเงิน"
    ]
    if specific_product_name:
        filtered_orders = [
            order
            for order in filtered_orders
            if specific_product_name.lower() in order["productName"].lower()
        ]

    if not filtered_orders:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="ไม่พบคำสั่งซื้อที่ยังรอชำระเงินค่ะ 😊",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า"))]
                ),
            ),
        )
        return

    reply_text = (
        f'สถานะของ "{specific_product_name}" ค่ะ:'
        if specific_product_name
        else "ตรวจสอบสถานะคำสั่งซื้อของคุณค่ะ:\n"
    )
    for order in filtered_orders:
        status_emoji = get_status_emoji(order["status"])
        reply_text += f"\n- {order['productName']}\n  สถานะ: {status_emoji} {order['status']}"
        if order.get("trackingNumber"):
            reply_text += f"\n  เลขพัสดุ: {order['trackingNumber']}"
        reply_text += "\n"

    all_order_ids = [
        QuickReplyButton(
            action=MessageAction(
                label=order["orderId"], text=f"ตรวจสอบสถานะ {order['orderId']}"
            )
        )
        for order in filtered_orders
    ]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=reply_text.strip(),
            quick_reply=QuickReply(
                items=[
                    *all_order_ids,
                    QuickReplyButton(action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า")),
                    QuickReplyButton(
                        action=MessageAction(label="ติดต่อแอดมิน 🙋‍♀️", text="ติดต่อแอดมิน")
                    ),
                ]
            ),
        ),
    )
