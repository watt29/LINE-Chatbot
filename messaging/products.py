from linebot.models import (
    FlexSendMessage,
    CarouselContainer,
    BubbleContainer,
    ImageComponent,
    BoxComponent,
    TextComponent,
    ButtonComponent,
    PostbackAction,
    URIAction,
    TextSendMessage,
)
from config import line_bot_api, db

def send_product_carousel(reply_token, category=None):
    query = db.reference("products")
    if category:
        query = query.order_by_child("category").equal_to(category)
    products = query.get()

    if not products:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(
                text=f'ขออภัยค่ะ ขณะนี้ยังไม่มีสินค้าในหมวดหมู่ "{category}" ค่ะ 😔'
            ),
        )
        return

    bubbles = []
    for item_id, product in products.items():
        bubble = BubbleContainer(
            hero=ImageComponent(
                url=product["image"],
                size="full",
                aspect_ratio="1:1",
                aspect_mode="cover",
            ),
            body=BoxComponent(
                layout="vertical",
                spacing="none",
                contents=[
                    TextComponent(
                        text=product["name"], weight="bold", size="xl", wrap=True
                    ),
                    BoxComponent(
                        layout="vertical",
                        margin="none",
                        spacing="sm",
                        contents=[
                            BoxComponent(
                                layout="baseline",
                                spacing="sm",
                                contents=[
                                    TextComponent(
                                        text="วัสดุ",
                                        color="#aaaaaa",
                                        size="sm",
                                        flex=2,
                                    ),
                                    TextComponent(
                                        text=product["material"],
                                        wrap=True,
                                        color="#666666",
                                        size="sm",
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout="baseline",
                                spacing="sm",
                                contents=[
                                    TextComponent(
                                        text="ราคา",
                                        color="#aaaaaa",
                                        size="sm",
                                        flex=2,
                                    ),
                                    TextComponent(
                                        text=product["price"],
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
                        text=product.get("description", ""),
                        wrap=True,
                        margin="none",
                        size="sm",
                    ),
                ],
            ),
            footer=BoxComponent(
                layout="vertical",
                spacing="none",
                flex=0,
                contents=[
                    ButtonComponent(
                        style="primary",
                        height="sm",
                        action=PostbackAction(
                            label="สั่งเช่าบูชา ✨",
                            data=f"action=buy&itemId={item_id}",
                            display_text=f"สนใจ {product['name']}",
                        ),
                    ),
                    ButtonComponent(
                        height="sm",
                        action=URIAction(
                            label="สอบถามเพิ่มเติม 💬",
                            uri="https://line.me/R/ti/p/@210oavob",
                        ),
                    ),
                ],
            ),
        )
        bubbles.append(bubble)

    carousel_message = FlexSendMessage(
        alt_text=f"รายการสินค้า: {category or 'ทั้งหมด'}",
        contents=CarouselContainer(contents=bubbles),
    )
    line_bot_api.reply_message(reply_token, carousel_message)
