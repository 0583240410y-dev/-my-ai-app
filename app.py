from flask import Flask, render_template_string, request, jsonify
import os
import urllib.request
import json

app = Flask(__name__)

# קבלת מפתח ה-AI מתוך ההגדרות של הענן (Render)
AI_API_KEY = os.getenv("AI_API_KEY", "")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>עוזר ה-AI החכם שלך</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 450px; text-align: center; }
        h1 { color: #333; font-size: 22px; margin-bottom: 10px; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        .chat-box { border: 1px solid #ddd; border-radius: 8px; height: 250px; overflow-y: auto; padding: 10px; margin-bottom: 15px; text-align: right; background: #fafafa; }
        .message { margin-bottom: 10px; line-height: 1.4; }
        .user-msg { color: #0056b3; font-weight: bold; }
        .ai-msg { color: #333; }
        input[type="text"] { width: calc(100% - 22px); padding: 10px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 10px; font-size: 14px; }
        button { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; width: 100%; }
        button:hover { background-color: #0056b3; }
        .pricing { margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px; }
        .btn-upgrade { background-color: #28a745; margin-top: 5px; }
        .btn-upgrade:hover { background-color: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h1>עוזר ה-AI החכם שלך</h1>
        <p>שאל אותי כל שאלה, נסח מיילים או קבל תשובות חכמות בשניות.</p>
        
        <div class="chat-box" id="chatBox">
            <div class="message ai-msg"><b>AI:</b> שלום! אני כאן כדי לעזור לך. כתוב לי שאלה למטה...</div>
        </div>
        
        <input type="text" id="userInput" placeholder="הקלד את השאלה או הבקשה שלך כאן..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">שלח הודעה</button>
        
        <div class="pricing">
            <p>רוצה גישה בלתי הגבלה לכל הפיצ'רים המתקדמים?</p>
            <button class="btn-upgrade" onclick="upgradePlan()">שדרג מנוי עכשיו</button>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = input.value.trim();
            if (!text) return;
            
            chatBox.innerHTML += `<div class="message user-msg">אתה: ${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // הודעת המתנה
            const loadingId = 'loading-' + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="message ai-msg" style="color: #888;">AI חושב...</div>`;
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

        function upgradePlan() {
            alert('מעבר לדף התשלום המאובטח של Stripe...');
        }
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
    
    if not AI_API_KEY:
        return jsonify({"reply": f"קיבלתי את ההודעה שלך: '{user_message}'. (כדי לקבל תשובות חכמות מ-AI אמיתי, יש להגדיר מפתח AI בהגדרות Render)."}), 200

    # חיבור למודל הבינה המלאכותית (OpenAI)
    try:
        url = "https://api.openai.com/v1/chat/completions"
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}]
        })
        req = urllib.request.Request(url, data=payload.encode('utf-8'), headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_API_KEY}"
        })
        
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ai_reply = res_data["choices"][0]["message"]["content"]
            return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": "אירעה שגיאה בעיבוד הבקשה מול שרת ה-AI."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
