import os
import json # Import json module
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import google.generativeai as genai

# --- INITIALIZATIONS ---
load_dotenv()

# Flask App
app = Flask(__name__)

# LINE Bot SDK
# Make sure to set LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET in your .env file
print(f"LINE_CHANNEL_ACCESS_TOKEN: {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')}") # Debug print
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# Firebase Admin
# For Render deployment, set FIREBASE_SERVICE_ACCOUNT_JSON as an environment variable
# containing the full JSON content of your serviceAccountKey.json file.
# Also set FIREBASE_DATABASE_URL in your .env file or Render environment variables.
try:
    # Try to load from environment variable first (for cloud deployment)
    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if service_account_json:
        cred = credentials.Certificate(json.loads(service_account_json))
    else:
        # Fallback to file for local development if env var is not set
        cred = credentials.Certificate("serviceAccountKey.json")

    firebase_admin.initialize_app(cred, {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")})
    auto_replies_ref = db.reference("auto_replies")
    knowledge_base_ref = db.reference("knowledge_base") # For AI context
except Exception as e:
    app.logger.error(f"Error initializing Firebase: {e}")
    # In a production environment, you might want to exit or disable Firebase-dependent features.
    # For now, the app will likely fail if Firebase isn't initialized.

# Google Generative AI
# Make sure to set GEMINI_API_KEY in your .env file or Render environment variables
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    ai_model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    app.logger.error(f"Error initializing Google Generative AI: {e}")

# --- WEBHOOK HANDLER ---
@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Check your CHANNEL_SECRET.")
        abort(400)
    except Exception as e:
        app.logger.error(f"Error handling webhook event: {e}")
        abort(500)
    return "OK"

# --- MESSAGE HANDLERS ---
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_text = event.message.text.strip().lower()
    reply_token = event.reply_token

    # Fetch auto-reply rules from Firebase
    rules = auto_replies_ref.get()
    
    response_text = None # Initialize as None

    if rules:
        for keyword, reply in rules.items():
            if keyword.lower() in user_text:
                response_text = reply
                break
    
    # If no auto-reply match, ask AI
    if response_text is None:
        response_text = ask_ai(user_text)
    
    try:
        line_bot_api.reply_message(reply_token, TextSendMessage(text=response_text))
    except Exception as e:
        app.logger.error(f"Error replying to message: {e}")


def ask_ai(question):
    try:
        knowledge_base = knowledge_base_ref.get()
        context = str(knowledge_base) if knowledge_base else "No specific knowledge base available."

        prompt = f"""คุณคือผู้ช่วยอัจฉริยะ จงตอบคำถามของลูกค้าต่อไปนี้อย่างสุภาพ, เป็นมิตร, และให้ข้อมูลที่ถูกต้องที่สุด โดยอ้างอิงจาก "ข้อมูลความรู้" ที่ให้มาเท่านั้น หากไม่พบคำตอบในข้อมูล ให้ตอบอย่างสุภาพว่า "ขออภัยค่ะ ฉันยังไม่มีข้อมูลในส่วนนี้"

--- ข้อมูลความรู้ ---
{context}
---------------------

คำถามลูกค้า: "{question}"

คำตอบ:"""
        response = ai_model.generate_content(prompt)
        return response.text
    except Exception as e:
        app.logger.error(f"Error asking AI: {e}")
        return "ขออภัยค่ะ เกิดข้อผิดพลาดในการประมวลผลคำถามด้วย AI"


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)