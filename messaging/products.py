from linebot.models import (
    FlexSendMessage,
    CarouselContainer,
    BubbleContainer,
    ImageComponent,
    BoxComponent,
    TextComponent,
    ButtonComponent,
    URIAction,
    PostbackAction
)
from firebase_admin import db

def _create_product_bubble(product_id, product_info):
    """Creates a Flex Message bubble for a single product."""
    if not isinstance(product_info, dict):
        return None

    buttons = []
    if 'actions' in product_info and isinstance(product_info.get('actions'), list):
        for action in product_info['actions']:
            action_type = action.get('type')
            if action_type == 'uri':
                uri = action.get('uri')
                if uri and uri.strip():
                    buttons.append(ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label=action.get('label', 'Details'), uri=uri)
                    ))
            elif action_type == 'postback':
                buttons.append(ButtonComponent(
                    style='primary',
                    height='sm',
                    action=PostbackAction(label=action.get('label', 'Buy'), data=action.get('data', ''))
                ))

    image_url = product_info.get('imageUrl')
    if not image_url or not image_url.strip():
        image_url = 'https://via.placeholder.com/400x300?text=No+Image'

    return BubbleContainer(
        hero=ImageComponent(
            url=image_url,
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=URIAction(uri=image_url)
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text=product_info.get('title', 'No Title'), weight='bold', size='xl'),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=product_info.get('price', 'N/A'), weight='bold', size='xl', flex=0)
                    ]
                ),
                TextComponent(
                    text=product_info.get('description', 'No description available.'),
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
            contents=buttons,
            flex=0
        )
    )

def create_product_carousel():
    """Creates a Flex Message carousel of products from Firebase."""
    try:
        products_ref = db.reference('products')
        products_data = products_ref.get()

        if not products_data:
            return None

        bubbles = [
            _create_product_bubble(pid, pinfo)
            for pid, pinfo in products_data.items()
        ]
        bubbles = [bubble for bubble in bubbles if bubble is not None]

        if not bubbles:
            return None

        carousel_container = CarouselContainer(contents=bubbles)
        return FlexSendMessage(alt_text="Recommended products", contents=carousel_container)

    except Exception as e:
        print(f"Error creating product carousel: {e}")
        return None