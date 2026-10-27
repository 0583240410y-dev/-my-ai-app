from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# קוד העיצוב והממשק של האפליקציה (HTML + עיצוב מודרני בעברית)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>עוזר ה-AI שלך</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 400px; text-align: center; }
        h1 { color: #333; font-size: 22px; margin-bottom: 10px; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        .chat-box { border: 1px solid #ddd; border-radius: 8px; height: 200px; overflow-y: auto; padding: 10px; margin-bottom: 15px; text-align: right; background: #fafafa; }
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
        <p>נסח הודעות, כתוב מיילים וחסוך שעות עבודה בשניות.</p>
        
        <div class="chat-box" id="chatBox">
            <div style="color: #888;">שלום! אני כאן כדי לעזור לך. כתוב לי משהו למטה...</div>
        </div>
        
        <input type="text" id="userInput" placeholder="הקלד את השאלה או הבקשה שלך כאן...">
        <button onclick="sendMessage()">שלח הודעה</button>
        
        <div class="pricing">
            <p>רוצה גישה בלתי הגבלה לכל הפיצ'רים המתקדמים?</p>
            <button class="btn-upgrade" onclick="upgradePlan()">שדרג מנוי עכשיו</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            if (!input.value.trim()) return;
            
            chatBox.innerHTML += `<div><b>אתה:</b> ${input.value}</div>`;
            const userText = input.value;
            input.value = '';
            
            setTimeout(() => {
                chatBox.innerHTML += `<div style="color: #007bff;"><b>AI:</b> קיבלתי את הבקשה שלך: "${userText}". המערכת פועלת מצוין!</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 500);
        }

        function upgradePlan() {
            alert('מעבר לדף התשלום המאובטח של Stripe...');
            // כאן אפשר לחבר בהמשך את קישור התשלום הישיר מ-Stripe
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
