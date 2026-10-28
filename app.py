from flask import Flask, render_template_string, request, jsonify
import os
import urllib.request
import json

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Pro - עוזר הבינה המלאכותית המתקדם שלך</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 90vh; }
        .container { background: white; padding: 30px; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.08); width: 100%; max-width: 500px; text-align: center; }
        h1 { color: #1a1a1a; font-size: 24px; margin-bottom: 8px; font-weight: 700; }
        p.subtitle { color: #666; font-size: 14px; margin-bottom: 20px; }
        .templates { display: flex; gap: 8px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
        .template-btn { background: #eef2ff; color: #4f46e5; border: 1px solid #c7d2fe; padding: 6px 12px; border-radius: 20px; font-size: 12px; cursor: pointer; transition: all 0.2s; font-weight: 600; }
        .template-btn:hover { background: #4f46e5; color: white; }
        .chat-box { border: 1px solid #e5e7eb; border-radius: 12px; height: 280px; overflow-y: auto; padding: 15px; margin-bottom: 15px; text-align: right; background: #fafafa; }
        .message { margin-bottom: 12px; line-height: 1.5; font-size: 14px; }
        .user-msg { color: #1e40af; font-weight: 600; background: #e0e7ff; padding: 8px 12px; border-radius: 10px 10px 0 10px; display: inline-block; max-width: 80%; float: left; clear: both; }
        .ai-msg { color: #1f2937; background: #ffffff; padding: 8px 12px; border-radius: 10px 10px 10px 0; border: 1px solid #e5e7eb; display: inline-block; max-width: 85%; float: right; clear: both; white-space: pre-wrap; }
        .input-area { display: flex; gap: 8px; margin-bottom: 15px; }
        input[type="text"] { flex: 1; padding: 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; outline: none; }
        input[type="text"]:focus { border-color: #4f46e5; }
        button.send-btn { background-color: #4f46e5; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; transition: background 0.2s; }
        button.send-btn:hover { background-color: #4338ca; }
        .pricing { margin-top: 20px; border-top: 1px solid #f3f4f6; padding-top: 15px; }
        .btn-upgrade { background-color: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: bold; width: 100%; transition: background 0.2s; }
        .btn-upgrade:hover { background-color: #059669; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Pro - עוזר חכם</h1>
        <p class="subtitle">בחר תבנית מהירה או שאל כל שאלה לקבלת תשובה מיידית</p>
        <div class="templates">
            <button class="template-btn" onclick="setTemplate('email')">✉️ ניסוח מייל מקצועי</button>
            <button class="template-btn" onclick="setTemplate('post')">📱 כתיבת פוסט שיווקי</button>
            <button class="template-btn" onclick="setTemplate('summarize')">📝 סיכום טקסט</button>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message ai-msg"><b>AI:</b> שלום! במה אוכל לעזור לך היום?</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="הקלד את השאלה או הבקשה שלך..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">שלח</button>
        </div>
        <div class="pricing">
            <p style="font-size: 13px; color: #6b7280; margin-bottom: 8px;">רוצה גישה בלתי מוגבלת לכל הפיצ'רים המתקדמים?</p>
            <button class="btn-upgrade" onclick="upgradePlan()">שדרג מנוי עכשיו</button>
        </div>
    </div>
    <script>
        function setTemplate(type) {
            const input = document.getElementById('userInput');
            if (type === 'email') {
                input.value = "נסח לי מייל מקצועי בנושא: ";
            } else if (type === 'post') {
                input.value = "כתוב פוסט שיווקי ויראלי לרשתות החברתיות על: ";
            } else if (type === 'summarize') {
                input.value = "סכם לי בנקודות קצרות את הטקסט הבא: ";
            }
            input.focus();
        }
        function handleKeyPress(event) {
            if (event.key === 'Enter') { sendMessage(); }
        }
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = input.value.trim();
            if (!text) return;
            chatBox.innerHTML += `<div class="message user-msg">אתה: ${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
            const loadingId = 'loading-' + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="message ai-msg" style="color: #6b7280;">AI מעבד תשובה...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="message ai-msg"><b>AI:</b> ${data.reply}</div>`;
            } catch (error) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="message ai-msg" style="color: red;">שגיאה בתקשורת עם השרת.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        function upgradePlan() { alert('מעבר לדף התשלום המאובטח של Stripe...'); }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not GEMINI_API_KEY:
        return jsonify({"reply": "חסר מפתח API בהגדרות Render."}), 200

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = json.dumps({
            "contents": [{
                "parts": [{"text": user_message}]
            }]
        })
        req = urllib.request.Request(url, data=payload.encode('utf-8'), headers={
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ai_reply = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": "אירעה שגיאה בעיבוד הבקשה מול שרת ה-Gemini."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
