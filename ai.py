from firebase_admin import db
from config import ai_model, app

def get_intent(text):
    lower_text = text.lower()

    # Define keywords for each intent
    intents = {
        "view_categories": ["ดูสินค้า", "มีอะไรบ้าง", "ขอรายการ", "เมนู", "product", "สินค้า"],
        "check_status": ["สถานะ", "เช็คของ", "ถึงไหนแล้ว", "ส่งของยัง", "ออเดอร์", "คำสั่งซื้อ"],
        "notify_payment": ["แจ้งโอนเงิน", "แจ้งโอน", "ส่งสลิป", "โอนแล้ว"],
        "view_unpaid_orders": [
            "ยังไม่จ่าย",
            "ยังไม่ชำระ",
            "ค้างจ่าย",
            "ค้างชำระ",
            "ยังไม่โอน",
            "สินค้าที่ยังไม่ชำระเงิน",
            "รายการที่ต้องจ่าย",
        ],
        "get_payment_info": [
            "โอนเงิน",
            "วิธีสั่งซื้อ",
            "ชำระเงิน",
            "จ่ายเงิน",
            "เลขบัญชี",
            "qr code",
            "พร้อมเพย์",
            "วิธีเช่าบูชา",
        ],
        "cancel": ["ยกเลิก", "cancel", "ไม่เอาแล้ว"],
        "contact_admin": [
            "ติดต่อแอดมิน",
            "คุยกับคน",
            "คุยกับพนักงาน",
            "แอดมิน",
            "ติดต่อ",
            "ติดต่อยังไง",
            "เบอร์โทร",
            "ไลน์",
        ],
    }

    for intent, keywords in intents.items():
        if any(keyword in lower_text for keyword in keywords):
            return {"name": intent, "data": {}}

    # Intent: View Products in a specific Category
    all_categories = db.reference("knowledge_base/categories").get() or []
    matched_category = next(
        (cat for cat in all_categories if cat.lower() in lower_text), None
    )
    if matched_category:
        return {"name": "view_products_in_category", "data": {"category": matched_category}}

    return {"name": "ask_ai", "data": {}}


def ask_ai(question):
    app.logger.info("Asking AI...")
    knowledge_base = db.reference("knowledge_base").get()
    context = str(knowledge_base)

    prompt = f"""คุณคือ "น้องมหาลาภ" ผู้ช่วยอัจฉริยะของร้าน "Maharat Amulet" ซึ่งเป็นร้านให้เช่าบูชาวัตถุมงคลและพระเครื่อง

จงตอบคำถามของลูกค้าต่อไปนี้อย่างสุภาพ, เป็นมิตร, และให้ข้อมูลที่ถูกต้องที่สุด โดยอ้างอิงจาก "ข้อมูลความรู้" ที่ให้มาเท่านั้น ห้ามตอบคำถามที่ไม่เกี่ยวข้องกับร้านค้า, พระเครื่อง, หรือการเช่าบูชาโดยเด็ดขาด หากไม่พบคำตอบในข้อมูล ให้ตอบอย่างสุภาพว่า "ขออภัยค่ะน้องมหาลาภยังไม่มีข้อมูลในส่วนนี้ คุณลูกค้าสามารถสอบถามกับแอดมินโดยตรงได้เลยนะคะ"

--- ข้อมูลความรู้ ---
{context}
---------------------

คำถามลูกค้า: "{question}"

คำตอบของน้องมหาลาภ: (โปรดใช้ Emoji ที่เหมาะสมเพื่อเพิ่มความเป็นมิตรและน่าสนใจในคำตอบของคุณ)"""

    response = ai_model.generate_content(prompt)
    return response.text
