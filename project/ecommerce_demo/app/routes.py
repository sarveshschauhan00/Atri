from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import json
import os

bp = Blueprint('main', __name__)

# Load data from JSON files
def load_json_data(filename):
    with open(os.path.join(os.path.dirname(__file__), '../data', filename), 'r') as file:
        return json.load(file)

# Save data to JSON files
def save_json_data(filename, data):
    with open(os.path.join(os.path.dirname(__file__), '../data', filename), 'w') as file:
        json.dump(data, file, indent=4)

# Load products data
products = load_json_data('products.json')

@bp.route('/')
def home():
    return render_template('home.html', products=products)

@bp.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        flash('Product not found!', 'error')
        return redirect(url_for('main.home'))
    return render_template('product.html', product=product)

@bp.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        flash('Product not found!', 'error')
        return redirect(url_for('main.home'))
    
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})

    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('main.cart'))

@bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    flash('Product removed from cart!', 'success')
    return redirect(url_for('main.cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user_data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'email': request.form['email']
        }
        users = load_json_data('users.json')
        user_id = max(user['id'] for user in users) + 1 if users else 1
        user_data['id'] = user_id
        users.append(user_data)
        save_json_data('users.json', users)

        cart_items = session.get('cart', [])
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)
        order_data = {
            'order_id': max(order['order_id'] for order in load_json_data('orders.json')) + 1 if load_json_data('orders.json') else 1,
            'user_id': user_id,
            'products': cart_items,
            'total_price': total_price,
            'status': 'confirmed'
        }
        orders = load_json_data('orders.json')
        orders.append(order_data)
        save_json_data('orders.json', orders)

        session.pop('cart', None)
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.confirmation', order_id=order_data['order_id']))
    
    return render_template('checkout.html')

@bp.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    orders = load_json_data('orders.json')
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order is None:
        flash('Order not found!', 'error')
        return redirect(url_for('main.home'))
    return render_template('confirmation.html', order=order)
