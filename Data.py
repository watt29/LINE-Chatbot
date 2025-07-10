import firebase_admin
from firebase_admin import credentials, db

# เชื่อมต่อกับ Firebase
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://maharat-4564f-default-rtdb.asia-southeast1.firebasedatabase.app/ '
    })
    ref = db.reference('/')
except Exception as e:
    print(f"❌ ไม่สามารถเชื่อมต่อกับ Firebase ได้\n{e}")
    exit()

# --- ฟังก์ชันแสดงข้อมูล ---
def view_data():
    snapshot = ref.get()
    print("\n🤖 Auto Replies:")
    if 'auto_replies' in snapshot:
        for key, value in snapshot['auto_replies'].items():
            print(f"{key}: {value}")
    else:
        print("ไม่มีข้อมูล")

    print("\n🧠 Knowledge Base:")
    if 'knowledge_base' in snapshot:
        for key, value in snapshot['knowledge_base'].items():
            print(f"{key}: {value}")
    else:
        print("ไม่มีข้อมูล")

# --- ฟังก์ชันเพิ่มข้อมูล ---
def add_data():
    category = input("เลือกหมวดหมู่ (auto_replies / knowledge_base): ").strip()
    key = input("กรอก Keyword / Topic: ").strip()
    value = input("กรอกคำตอบ / เนื้อหา: ").strip()

    if not key or not value:
        print("⚠️ กรุณากรอกทั้ง Keyword/Topic และคำตอบ/เนื้อหา")
        return

    try:
        db.reference(f'/{category}/{key}').set(value)
        print("✅ เพิ่มข้อมูลเรียบร้อยแล้ว!")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดขณะเพิ่มข้อมูล: {e}")

# --- ฟังก์ชันแก้ไขข้อมูล ---
def edit_data():
    category = input("เลือกหมวดหมู่ (auto_replies / knowledge_base): ").strip()
    key = input("กรอก Keyword / Topic ที่ต้องการแก้ไข: ").strip()
    new_value = input("กรอกคำตอบ / เนื้อหาใหม่: ").strip()

    if not key or not new_value:
        print("⚠️ กรุณากรอกทั้ง Keyword/Topic และคำตอบ/เนื้อหาใหม่")
        return

    try:
        db.reference(f'/{category}/{key}').set(new_value)
        print("✅ แก้ไขข้อมูลเรียบร้อยแล้ว!")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดขณะแก้ไขข้อมูล: {e}")

# --- ฟังก์ชันลบข้อมูล ---
def delete_data():
    category = input("เลือกหมวดหมู่ (auto_replies / knowledge_base): ").strip()
    key = input("กรอก Keyword / Topic ที่ต้องการลบ: ").strip()

    if not key:
        print("⚠️ กรุณากรอก Keyword/Topic ที่ต้องการลบ")
        return

    try:
        db.reference(f'/{category}/{key}').delete()
        print("🗑️ ลบข้อมูลเรียบร้อยแล้ว!")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดขณะลบข้อมูล: {e}")

# --- เมนูหลัก ---
def main_menu():
    while True:
        print("\n===========================")
        print("Firebase Manager - Console")
        print("===========================")
        print("1. แสดงข้อมูลทั้งหมด")
        print("2. เพิ่มข้อมูล")
        print("3. แก้ไขข้อมูล")
        print("4. ลบข้อมูล")
        print("0. ออกจากโปรแกรม")
        choice = input("เลือกเมนู (0-4): ").strip()

        if choice == '1':
            view_data()
        elif choice == '2':
            add_data()
        elif choice == '3':
            edit_data()
        elif choice == '4':
            delete_data()
        elif choice == '0':
            print("👋 ออกจากโปรแกรมเรียบร้อยแล้ว")
            break
        else:
            print("❌ ไม่มีเมนูนี้ กรุณาลองใหม่")

# --- เริ่มต้นโปรแกรม ---
if __name__ == "__main__":
    main_menu()