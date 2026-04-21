from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    numeroSerie = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        "id": i.id,
        "nombre": i.nombre,
        "numeroSerie": i.numeroSerie,
        "descripcion": i.descripcion
    } for i in items])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    nuevo = Item(
        nombre=data.get('nombre'),
        numeroSerie=data.get('numeroSerie'),
        descripcion=data.get('descripcion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"ok": True})

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True)