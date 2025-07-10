import os
import firebase_admin
import google.generativeai as genai
from firebase_admin import credentials, db
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from dotenv import load_dotenv

# --- INITIALIZATIONS ---
load_dotenv()

# Flask App
app = Flask(__name__)

# LINE Bot SDK
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

# Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")})
user_states_ref = db.reference("user_states")

# Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ai_model = genai.GenerativeModel("gemini-1.5-flash")
