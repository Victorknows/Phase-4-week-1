from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
db = SQLAlchemy(app)

# Define Models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy=True) 

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    restaurants = db.relationship('RestaurantPizza', backref='pizza', lazy=True)

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)

    def validate_price(self):
        return 1 <= self.price <= 30

    def validate_pizza_and_restaurant_existence(self):
        return Pizza.query.get(self.pizza_id) is not None and Restaurant.query.get(self.restaurant_id) is not None

# Routes

@app.route('/')
def index():
    return 'Welcome to the Restaurant'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    with app.app_context():
        restaurants = Restaurant.query.all()
        return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    with app.app_context():
        restaurant = Restaurant.query.get(id)
        if restaurant:
            pizzas = [{'id': rp.pizza.id, 'name': rp.pizza.name, 'ingredients': rp.pizza.ingredients} for rp in restaurant.pizzas]
            return jsonify({'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address, 'pizzas': pizzas})
        else:
            return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    with app.app_context():
        restaurant = Restaurant.query.get(id)
        if restaurant:
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    with app.app_context():
        pizzas = Pizza.query.all()
        return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    with app.app_context():
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')
        
        restaurant_pizza = RestaurantPizza()
        
        if not restaurant_pizza.validate_pizza_and_restaurant_existence():
            return jsonify({'errors': ['Pizza or restaurant does not exist']}), 400

        restaurant_pizza.price = price
        
        if not restaurant_pizza.validate_price():
            return jsonify({'errors': ['Price must be between 1 and 30']}), 400
        
        restaurant_pizza.pizza_id = pizza_id
        restaurant_pizza.restaurant_id = restaurant_id
        
        try:
            db.session.add(restaurant_pizza)
            db.session.commit()
            return jsonify({'id': restaurant_pizza.pizza.id, 'name': restaurant_pizza.pizza.name, 'ingredients': restaurant_pizza.pizza.ingredients})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'errors': ['IntegrityError']}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
