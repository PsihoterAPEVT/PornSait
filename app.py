"""
SWILL ADULT STREAM - PYTHON FLASK
ОДИН КЛИК - ПОЛНОЦЕННЫЙ САЙТ
ЗАПУСК: python app.py
"""

import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from functools import wraps

# ============= ИНИЦИАЛИЗАЦИЯ =============
app = Flask(__name__)
app.secret_key = 'swill-purple-neon-2026-ultimate'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB

# СОЗДАЕМ ПАПКИ
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# ============= БАЗА ДАННЫХ (JSON) =============
DB_FILE = 'swill_database.json'

def init_db():
    if not os.path.exists(DB_FILE):
        db = {
            'videos': [
                {
                    'id': 1,
                    'title': '🔥 SWILL PREMIUM 4K',
                    'description': 'Эксклюзивный контент высшего качества. Только для взрослых.',
                    'filename': 'sample1.mp4',
                    'thumbnail': 'thumb1.jpg',
                    'views': 15420,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 2,
                    'title': '💎 SWILL GOLD EDITION',
                    'description': 'Самое популярное видео недели. Миллионы просмотров.',
                    'filename': 'sample2.mp4',
                    'thumbnail': 'thumb2.jpg',
                    'views': 8930,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'id': 3,
                    'title': '⭐ SWILL VIP CLUB',
                    'description': 'Только для подписчиков. Максимальное удовольствие.',
                    'filename': 'sample3.mp4',
                    'thumbnail': 'thumb3.jpg',
                    'views': 12750,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ],
            'earnings': {
                'total': 125430,
                'today': 12900,
                'week': 87400,
                'transactions': []
            },
            'settings': {
                'admin_password': 'swillmaster2025',
                'site_title': 'SWILL STREAM',
                'theme': 'dark_purple'
            }
        }
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
    return DB_FILE

def get_db():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# ============= ДЕКОРАТОРЫ =============
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin'))
        return f(*args, **kwargs)
    return decorated_function

# ============= МАРШРУТЫ =============
@app.route('/')
def index():
    db = get_db()
    videos = db['videos']
    earnings = db['earnings']
    return render_template('index.html', videos=videos, earnings=earnings)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        db = get_db()
        if password == db['settings']['admin_password']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin_login.html', error=True)
    return render_template('admin_login.html', error=False)

@app.route('/admin/panel')
@admin_required
def admin_panel():
    db = get_db()
    videos = db['videos']
    earnings = db['earnings']
    return render_template('admin_panel.html', videos=videos, earnings=earnings)

@app.route('/admin/upload', methods=['POST'])
@admin_required
def upload_video():
    if 'video' not in request.files or 'thumbnail' not in request.files:
        return redirect(url_for('admin_panel'))
    
    video = request.files['video']
    thumbnail = request.files['thumbnail']
    title = request.form.get('title')
    description = request.form.get('description')
    
    if video.filename == '' or thumbnail.filename == '':
        return redirect(url_for('admin_panel'))
    
    # СОХРАНЯЕМ ФАЙЛЫ
    video_filename = secure_filename(f"video_{datetime.now().timestamp()}_{video.filename}")
    thumb_filename = secure_filename(f"thumb_{datetime.now().timestamp()}_{thumbnail.filename}")
    
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
    thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], thumb_filename))
    
    # ДОБАВЛЯЕМ В БАЗУ
    db = get_db()
    new_id = len(db['videos']) + 1
    
    db['videos'].append({
        'id': new_id,
        'title': title,
        'description': description,
        'filename': video_filename,
        'thumbnail': thumb_filename,
        'views': 0,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # ГЕНЕРИРУЕМ ПРИБЫЛЬ
    earn_amount = random.randint(500, 5000)
    db['earnings']['total'] += earn_amount
    db['earnings']['today'] += earn_amount
    db['earnings']['week'] += earn_amount
    db['earnings']['transactions'].append({
        'video_id': new_id,
        'amount': earn_amount,
        'source': 'premium_ads',
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    save_db(db)
    return redirect(url_for('admin_panel', success=True))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))

@app.route('/api/earnings')
def api_earnings():
    db = get_db()
    return jsonify(db['earnings'])

@app.route('/api/videos')
def api_videos():
    db = get_db()
    return jsonify(db['videos'])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/video/<int:video_id>')
def video_player(video_id):
    db = get_db()
    video = next((v for v in db['videos'] if v['id'] == video_id), None)
    if video:
        video['views'] += 1
        save_db(db)
        return render_template('player.html', video=video)
    return redirect(url_for('index'))

# ============= ЗАПУСК =============
if __name__ == '__main__':
    init_db()
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     🔥 SWILL ADULT STREAM - PYTHON ACTIVATED 🔥     ║
    ║                ПОЛНАЯ СТРУКТУРА ГОТОВА              ║
    ╚══════════════════════════════════════════════════════╝
    """)
    print("🌐 САЙТ:           http://localhost:5000")
    print("🔑 АДМИНКА:        http://localhost:5000/admin")
    print("🔐 ПАРОЛЬ:         swillmaster2025")
    print("📁 ЗАГРУЗКИ:       /uploads/\n")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)