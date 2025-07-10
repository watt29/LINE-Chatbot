import firebase_admin
from firebase_admin import credentials, db

# 1. โหลด Service Account Key และเชื่อมต่อกับ Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://maharat-c35cc-default-rtdb.asia-southeast1.firebasedatabase.app/ '
})

# 2. อ้างอิงฐานข้อมูล
ref = db.reference('/')  # จุดเริ่มต้นของฐานข้อมูล

# 3. ตัวอย่างฟังก์ชัน: บันทึกข้อมูล auto_replies
def set_auto_replies():
    data = {
        "สวัสดี": "สวัสดีค่ะ! มีอะไรให้ช่วยไหมคะ?",
        "เวลาเปิดทำการ": "ร้านเปิด 9.00 น. - 18.00 น. ทุกวันค่ะ",
        "ติดต่อเรา": "สามารถติดต่อแอดมินได้ทาง LINE Official Account ค่ะ"
    }
    db.reference('/auto_replies').set(data)
    print("✅ บันทึก auto_replies เรียบร้อย")

# 4. ตัวอย่างฟังก์ชัน: บันทึก knowledge_base
def set_knowledge_base():
    data = {
        "เกี่ยวกับร้าน": "ร้านของเราเชี่ยวชาญในการสร้าง LINE Bot ที่ตอบโจทย์ธุรกิจทุกประเภท ไม่ว่าจะเป็นบอทตอบคำถามอัตโนมัติ, ระบบจองคิว, หรือเชื่อมต่อกับระบบหลังบ้าน",
        "บริการของเรา": "เราให้บริการออกแบบ, พัฒนา, และดูแล LINE Bot พร้อมให้คำปรึกษาด้านการตลาดผ่าน LINE OA",
        "ติดต่อสอบถาม": "หากสนใจสร้าง LINE Bot สามารถติดต่อเราได้ทางอีเมล sales@yourcompany.com หรือโทร 081-234-5678"
    }
    db.reference('/knowledge_base').set(data)
    print("✅ บันทึก knowledge_base เรียบร้อย")

# 5. ตัวอย่างฟังก์ชัน: อ่านข้อมูลจาก Firebase
def get_data():
    auto_replies = db.reference('/auto_replies').get()
    knowledge_base = db.reference('/knowledge_base').get()

    print("\n💬 Auto Replies:")
    for q, a in auto_replies.items():
        print(f"{q}: {a}")

    print("\n📘 Knowledge Base:")
    for topic, desc in knowledge_base.items():
        print(f"{topic}: {desc}")

# 6. รันฟังก์ชัน
if __name__ == '__main__':
    set_auto_replies()
    set_knowledge_base()
    get_data()