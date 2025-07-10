from config import user_states_ref

# --- UTILITY FUNCTIONS ---

def get_user_state(user_id):
    return user_states_ref.child(user_id).get()

def set_user_state(user_id, state):
    user_states_ref.child(user_id).set(state)

def clear_user_state(user_id):
    user_states_ref.child(user_id).delete()

def get_status_emoji(status):
    return {
        "รอชำระเงิน": "⏳",
        "รอตรวจสอบสลิป": "🔍",
        "กำลังจัดส่ง": "🚚",
        "จัดส่งแล้ว": "✅",
    }.get(status, "")
