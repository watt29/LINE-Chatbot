from linebot.models import (
    FlexSendMessage,
    CarouselContainer,
    BubbleContainer,
    ImageComponent,
    BoxComponent,
    TextComponent,
    ButtonComponent,
    URIAction,
    PostbackAction,
    TextSendMessage # <-- เพิ่มบรรทัดนี้
)
from firebase_admin import db

def create_product_carousel():
    try:
        products_ref = db.reference('products')
        products_data = products_ref.get()

        if not products_data:
            return TextSendMessage(text="ขออภัยค่ะ ขณะนี้ยังไม่มีสินค้าให้แสดง")

        bubbles = []
        for product_id, product_info in products_data.items():
            # Ensure product_info is a dictionary
            if not isinstance(product_info, dict):
                continue

            # Create buttons for each product
            buttons = []
            if 'actions' in product_info and isinstance(product_info['actions'], list):
                for action in product_info['actions']:
                    if action.get('type') == 'uri':
                        buttons.append(ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(label=action.get('label', 'ดู'), uri=action.get('uri', ''))
                        ))
                    elif action.get('type') == 'postback':
                        buttons.append(ButtonComponent(
                            style='primary',
                            height='sm',
                            action=PostbackAction(label=action.get('label', 'สั่งซื้อ'), data=action.get('data', ''))
                        ))

            # Create a bubble for each product
            bubble = BubbleContainer(
                hero=ImageComponent(
                    url=product_info.get('imageUrl', 'https://via.placeholder.com/400x300?text=No+Image'),
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
                    action=URIAction(uri=product_info.get('imageUrl', '')) # Click image to open full image
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=product_info.get('title', 'ไม่มีชื่อสินค้า'), weight='bold', size='xl'),
                        BoxComponent(
                            layout='baseline',
                            contents=[
                                TextComponent(text=product_info.get('price', 'ราคาไม่ระบุ'), weight='bold', size='xl', flex=0)
                            ],
                            margin='md'
                        ),
                        TextComponent(
                            text=product_info.get('description', 'ไม่มีรายละเอียด'),
                            wrap=True,
                            color='#666666',
                            size='sm',
                            margin='md'
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=buttons
                )
            )
            bubbles.append(bubble)
        
        # Create a carousel from the bubbles
        carousel_container = CarouselContainer(contents=bubbles)
        return FlexSendMessage(alt_text="สินค้าแนะนำ", contents=carousel_container)

    except Exception as e:
        print(f"Error creating product carousel: {e}")
        return TextSendMessage(text="ขออภัยค่ะ เกิดข้อผิดพลาดในการแสดงสินค้า")