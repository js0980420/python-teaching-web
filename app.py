from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# 初始化OpenAI客戶端
api_key = os.environ.get('OPENAI_API_KEY')
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

@app.route('/')
def index():
    """首頁路由"""
    return render_template('index.html')

@app.route('/lessons')
def lessons():
    """課程頁面路由"""
    return render_template('lessons.html')

@app.route('/ai-tutor')
def ai_tutor():
    """AI助教頁面路由"""
    return render_template('ai_tutor.html')

@app.route('/practice')
def practice():
    """練習頁面路由"""
    return render_template('practice.html')

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """與AI助教對話的API端點"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '請輸入訊息'}), 400
        
        if not client:
            return jsonify({'error': '未設置OpenAI API金鑰，請先設置環境變數'}), 400
        
        # 使用OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一個專業的Python程式設計助教。請用繁體中文回答，提供清楚的解釋和實用的程式碼範例。保持友善和耐心的教學態度。"
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': f'發生錯誤：{str(e)}'}), 500

@app.route('/api/check-code', methods=['POST'])
def check_code():
    """檢查Python程式碼的API端點"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': '請輸入程式碼'}), 400
        
        if not client:
            return jsonify({'error': '未設置OpenAI API金鑰，請先設置環境變數'}), 400
        
        # 使用OpenAI檢查程式碼
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一個Python程式碼檢查助手。請分析提供的程式碼，指出任何語法錯誤、邏輯問題或改進建議。用繁體中文回答。"
                },
                {
                    "role": "user", 
                    "content": f"請檢查這段Python程式碼：\n\n```python\n{code}\n```"
                }
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        feedback = response.choices[0].message.content
        return jsonify({'feedback': feedback})
        
    except Exception as e:
        return jsonify({'error': f'檢查程式碼時發生錯誤：{str(e)}'}), 500

# 支持Railway和其他雲端平台部署
if __name__ == '__main__':
    # 本地開發時使用
    app.run(debug=True, host='127.0.0.1', port=8000)
else:
    # 生產環境時，app對象可以被gunicorn直接使用
    pass 