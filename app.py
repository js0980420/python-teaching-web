from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# 初始化XAI客戶端
api_key = os.environ.get('XAI_API_KEY', 'xai-e4IkGBt411Vrj0jEOKIfu6anO1OapqvMpcavAKDS35xRJrfUxTYSZLzuF9X28BBpJPuR4TPwBI2Lo7sL')
if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )
else:
    client = None

# 用戶會話存儲（簡單內存存儲，生產環境建議使用Redis）
user_sessions = {}

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
    """與AI助教對話的API端點（支持上下文記憶）"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({'error': '請輸入訊息'}), 400
        
        if not client:
            return jsonify({'error': '未設置XAI API金鑰'}), 400
        
        # 獲取或創建用戶會話
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                'messages': [
                    {
                        "role": "system", 
                        "content": "你是一個專業的Python程式設計助教。請用繁體中文回答，提供清楚的解釋和實用的程式碼範例。保持友善和耐心的教學態度。記住學生的學習進度，提供個人化指導。"
                    }
                ],
                'progress': {},
                'last_topic': None
            }
        
        # 添加用戶消息到會話記錄
        user_sessions[user_id]['messages'].append({
            "role": "user",
            "content": user_message
        })
        
        # 限制會話記錄長度（保留最近10輪對話）
        if len(user_sessions[user_id]['messages']) > 21:  # 1 system + 20 messages
            user_sessions[user_id]['messages'] = [
                user_sessions[user_id]['messages'][0]  # 保留system message
            ] + user_sessions[user_id]['messages'][-20:]  # 保留最近20條
        
        # 使用XAI API（grok模型）
        response = client.chat.completions.create(
            model="grok-beta",
            messages=user_sessions[user_id]['messages'],
            max_tokens=1000,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # 添加AI回應到會話記錄
        user_sessions[user_id]['messages'].append({
            "role": "assistant",
            "content": ai_response
        })
        
        return jsonify({
            'response': ai_response,
            'session_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'發生錯誤：{str(e)}'}), 500

@app.route('/api/check-code', methods=['POST'])
def check_code():
    """檢查Python程式碼的API端點（語法檢查+即時反饋）"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not code:
            return jsonify({'error': '請輸入程式碼'}), 400
        
        # 先進行基本語法檢查
        syntax_errors = []
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            syntax_errors.append({
                'line': e.lineno,
                'message': f'語法錯誤：{e.msg}',
                'type': 'syntax'
            })
        
        # 基本程式碼分析
        analysis = {
            'line_count': len(code.split('\n')),
            'has_functions': 'def ' in code,
            'has_loops': any(keyword in code for keyword in ['for ', 'while ']),
            'has_conditionals': any(keyword in code for keyword in ['if ', 'elif ', 'else:']),
            'imports': [line.strip() for line in code.split('\n') if line.strip().startswith('import') or line.strip().startswith('from')]
        }
        
        if not client:
            return jsonify({
                'syntax_errors': syntax_errors,
                'analysis': analysis,
                'ai_feedback': '未設置XAI API密鑰，僅提供基本檢查'
            })
        
        # 使用XAI進行深度代碼分析
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一個專業的Python程式碼審查助手。請分析程式碼的：1.語法正確性 2.邏輯合理性 3.代碼風格 4.性能優化建議 5.安全性問題。用繁體中文回答，提供具體的改進建議。"
                },
                {
                    "role": "user", 
                    "content": f"請詳細分析這段Python程式碼：\n\n```python\n{code}\n```\n\n請提供：語法檢查、邏輯分析、改進建議。"
                }
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        ai_feedback = response.choices[0].message.content
        
        # 更新用戶進度（如果有會話）
        if user_id in user_sessions:
            if 'code_submissions' not in user_sessions[user_id]:
                user_sessions[user_id]['code_submissions'] = []
            
            user_sessions[user_id]['code_submissions'].append({
                'code': code[:100] + '...' if len(code) > 100 else code,
                'timestamp': import_time(),
                'has_errors': len(syntax_errors) > 0
            })
        
        return jsonify({
            'syntax_errors': syntax_errors,
            'analysis': analysis,
            'ai_feedback': ai_feedback,
            'suggestions': generate_suggestions(code, analysis)
        })
        
    except Exception as e:
        return jsonify({'error': f'檢查程式碼時發生錯誤：{str(e)}'}), 500

def import_time():
    """獲取當前時間戳"""
    import time
    return time.time()

def generate_suggestions(code, analysis):
    """生成程式碼改進建議"""
    suggestions = []
    
    if not analysis['has_functions'] and analysis['line_count'] > 10:
        suggestions.append('考慮將代碼組織成函數，提高可讀性和重用性')
    
    if 'print(' in code:
        suggestions.append('除了print外，也可以學習使用logging模組')
    
    if not analysis['imports'] and analysis['line_count'] > 5:
        suggestions.append('可以考慮使用Python標準庫或第三方庫來簡化代碼')
    
    return suggestions

@app.route('/api/progress', methods=['GET', 'POST'])
def user_progress():
    """學習進度追蹤API"""
    try:
        if request.method == 'GET':
            user_id = request.args.get('user_id', 'anonymous')
            
            if user_id not in user_sessions:
                return jsonify({
                    'user_id': user_id,
                    'progress': {},
                    'stats': {
                        'total_conversations': 0,
                        'code_submissions': 0,
                        'topics_covered': [],
                        'last_activity': None
                    }
                })
            
            session_data = user_sessions[user_id]
            
            # 計算統計數據
            total_conversations = len([msg for msg in session_data.get('messages', []) if msg['role'] == 'user'])
            code_submissions = len(session_data.get('code_submissions', []))
            
            # 分析涵蓋的主題
            topics_covered = []
            for msg in session_data.get('messages', []):
                if msg['role'] == 'user':
                    content = msg['content'].lower()
                    if any(keyword in content for keyword in ['變數', 'variable', '資料型別']):
                        topics_covered.append('變數與資料型別')
                    if any(keyword in content for keyword in ['函數', 'function', 'def']):
                        topics_covered.append('函數')
                    if any(keyword in content for keyword in ['迴圈', 'loop', 'for', 'while']):
                        topics_covered.append('迴圈')
                    if any(keyword in content for keyword in ['條件', 'if', 'else']):
                        topics_covered.append('條件判斷')
            
            topics_covered = list(set(topics_covered))  # 去除重複
            
            last_activity = None
            if session_data.get('code_submissions'):
                last_activity = session_data['code_submissions'][-1]['timestamp']
            
            return jsonify({
                'user_id': user_id,
                'progress': session_data.get('progress', {}),
                'stats': {
                    'total_conversations': total_conversations,
                    'code_submissions': code_submissions,
                    'topics_covered': topics_covered,
                    'last_activity': last_activity
                }
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            user_id = data.get('user_id', 'anonymous')
            lesson_id = data.get('lesson_id')
            progress_data = data.get('progress', {})
            
            if user_id not in user_sessions:
                user_sessions[user_id] = {
                    'messages': [],
                    'progress': {},
                    'code_submissions': []
                }
            
            # 更新學習進度
            user_sessions[user_id]['progress'][lesson_id] = progress_data
            
            return jsonify({
                'success': True,
                'message': '學習進度已更新',
                'updated_progress': user_sessions[user_id]['progress']
            })
            
    except Exception as e:
        return jsonify({'error': f'進度追蹤錯誤：{str(e)}'}), 500

@app.route('/api/analytics', methods=['GET'])
def learning_analytics():
    """學習數據分析API"""
    try:
        # 全體用戶統計
        total_users = len(user_sessions)
        total_conversations = sum(
            len([msg for msg in session.get('messages', []) if msg['role'] == 'user'])
            for session in user_sessions.values()
        )
        total_code_submissions = sum(
            len(session.get('code_submissions', []))
            for session in user_sessions.values()
        )
        
        # 熱門主題分析
        topic_mentions = {}
        for session in user_sessions.values():
            for msg in session.get('messages', []):
                if msg['role'] == 'user':
                    content = msg['content'].lower()
                    topics = [
                        ('變數與資料型別', ['變數', 'variable', '資料型別', 'int', 'str', 'list']),
                        ('函數', ['函數', 'function', 'def', 'return']),
                        ('迴圈', ['迴圈', 'loop', 'for', 'while']),
                        ('條件判斷', ['條件', 'if', 'else', 'elif']),
                        ('錯誤處理', ['錯誤', 'error', 'try', 'except']),
                        ('檔案操作', ['檔案', 'file', 'open', 'read', 'write'])
                    ]
                    
                    for topic_name, keywords in topics:
                        if any(keyword in content for keyword in keywords):
                            topic_mentions[topic_name] = topic_mentions.get(topic_name, 0) + 1
        
        return jsonify({
            'overview': {
                'total_users': total_users,
                'total_conversations': total_conversations,
                'total_code_submissions': total_code_submissions,
                'avg_conversations_per_user': total_conversations / max(total_users, 1)
            },
            'popular_topics': sorted(topic_mentions.items(), key=lambda x: x[1], reverse=True)[:5],
            'recent_activity': get_recent_activity()
        })
        
    except Exception as e:
        return jsonify({'error': f'數據分析錯誤：{str(e)}'}), 500

def get_recent_activity():
    """獲取最近活動"""
    recent_submissions = []
    for user_id, session in user_sessions.items():
        for submission in session.get('code_submissions', [])[-3:]:  # 最近3次提交
            recent_submissions.append({
                'user_id': user_id[:8] + '...',  # 隱藏完整用戶ID
                'timestamp': submission['timestamp'],
                'has_errors': submission['has_errors']
            })
    
    # 按時間排序，取最新的10條
    recent_submissions.sort(key=lambda x: x['timestamp'], reverse=True)
    return recent_submissions[:10]

# 支持Railway和其他雲端平台部署
if __name__ == '__main__':
    # 本地開發時使用
    app.run(debug=True, host='127.0.0.1', port=8000)
else:
    # 生產環境時，app對象可以被gunicorn直接使用
    pass 