from linebot.models import (
    FlexSendMessage,
    BubbleContainer,
    ImageComponent,
    URIAction,
    BoxComponent,
    TextComponent,
    SeparatorComponent,
    ButtonComponent,
    MessageAction,
)
from config import line_bot_api

def send_payment_info(reply_token):
    flex_message = FlexSendMessage(
        alt_text="ข้อมูลการชำระเงิน PromptPay",
        contents=BubbleContainer(
            hero=ImageComponent(
                url="https://promptpay.io/0935325959.png",  # Replace with your QR code URL
                size="full",
                aspect_ratio="1:1",
                aspect_mode="fit",
                action=URIAction(uri="https://promptpay.io/0935325959"),
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text="สแกน QR Code เพื่อชำระเงิน 💰",
                        weight="bold",
                        size="xl",
                        align="center",
                    ),
                    SeparatorComponent(margin="md"),
                    BoxComponent(
                        layout="vertical",
                        margin="md",
                        spacing="sm",
                        contents=[
                            BoxComponent(
                                layout="baseline",
                                contents=[
                                    TextComponent(
                                        text="เบอร์พร้อมเพย์:",
                                        color="#aaaaaa",
                                        size="sm",
                                        flex=2,
                                    ),
                                    TextComponent(
                                        text="093-532-5959",
                                        wrap=True,
                                        color="#666666",
                                        size="sm",
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout="baseline",
                                contents=[
                                    TextComponent(
                                        text="ชื่อบัญชี:",
                                        color="#aaaaaa",
                                        size="sm",
                                        flex=2,
                                    ),
                                    TextComponent(
                                        text="นายจีรวัฒน์ พลอาจ",
                                        wrap=True,
                                        color="#666666",
                                        size="sm",
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    TextComponent(
                        text="\nเมื่อชำระเงินแล้ว สามารถส่งสลิปการโอนมาในแชทนี้เพื่อยืนยันได้เลยนะคะ ทางร้านจะรีบดำเนินการตรวจสอบให้ค่ะ 🙏",
                        wrap=True,
                        margin="lg",
                        size="sm",
                    ),
                ],
            ),
            footer=BoxComponent(
                layout="vertical",
                spacing="sm",
                contents=[
                    ButtonComponent(
                        style="primary",
                        height="sm",
                        action=MessageAction(label="แจ้งโอนเงิน 💰", text="แจ้งโอนเงิน"),
                    ),
                    ButtonComponent(
                        height="sm",
                        action=MessageAction(label="ตรวจสอบสถานะ 📦", text="ตรวจสอบสถานะ"),
                    ),
                    ButtonComponent(
                        height="sm",
                        action=MessageAction(label="ดูสินค้า ✨", text="ดูสินค้า"),
                    ),
                ],
            ),
        ),
    )
    line_bot_api.reply_message(reply_token, flex_message)
