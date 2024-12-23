from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from urllib.parse import quote_plus
from parser import pars_subjects, parse_fuse_data

app = Flask(__name__)

# URL-encode username и password для подключения
username = quote_plus('admin')  # Ваше имя пользователя
password = quote_plus('mypassword123')  # Ваш пароль

# Подключение к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@db/fuses_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# --- МОДЕЛИ ---

class Fuse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    types = db.Column(db.ARRAY(db.String), nullable=False)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fuse_id = db.Column(db.Integer, db.ForeignKey('fuse.id'), nullable=False)

    fuse = db.relationship('Fuse', backref='user_profiles')

# Создание таблиц
with app.app_context():
    db.create_all()

# --- МАРШРУТЫ ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/import_fuses', methods=['POST'])
def import_fuses():
    try:
        data = pars_subjects()
        fuses = parse_fuse_data(data)
        for fuse_data in fuses:
            fuse = Fuse(
                name=fuse_data['name'],
                price=fuse_data['price'],
                types=fuse_data['types']
            )
            db.session.add(fuse)
        db.session.commit()
        return jsonify({'message': 'Fuses imported successfully'})
    except Exception as e:
        logging.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    try:
        price_limit = float(request.args.get('price', 0))
        fuses = Fuse.query.filter(Fuse.price <= price_limit).all()
        return render_template('search_results.html', fuses=fuses)
    except Exception as e:
        logging.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/search_fuse', methods=['GET'])
def search_fuse():
    query = request.args.get('query', '')
    if query:
        # Поиск предохранителей по части названия (используем ilike для поиска по подстроке)
        fuses = Fuse.query.filter(Fuse.name.ilike(f'%{query}%')).all()
        fuse_data = [{
            'name': fuse.name,
            'price': fuse.price,
            'types': fuse.types
        } for fuse in fuses]
        return jsonify({'fuses': fuse_data})
    return jsonify({'fuses': []})

@app.route('/save_to_profile/<int:fuse_id>', methods=['POST'])
def save_to_profile(fuse_id):
    try:
        fuse = Fuse.query.get(fuse_id)
        if not fuse:
            return jsonify({'error': 'Fuse not found'}), 404

        profile_entry = UserProfile(fuse_id=fuse_id)
        db.session.add(profile_entry)
        db.session.commit()
        return jsonify({'message': 'Fuse saved to your profile!'})
    except Exception as e:
        logging.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/profile')
def profile():
    saved_fuses = UserProfile.query.all()
    return render_template('profile.html', saved_fuses=saved_fuses)

if __name__ == '__main__':
    app.run(debug=True)
