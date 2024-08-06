import json
import os

class JSONModel:
    def __init__(self, filename):
        self.filename = os.path.join(os.path.dirname(__file__), '../data', filename)
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

class Product(JSONModel):
    def __init__(self):
        super().__init__('products.json')

    def get_all_products(self):
        return self.data

    def get_product_by_id(self, product_id):
        return next((product for product in self.data if product['id'] == product_id), None)

class User(JSONModel):
    def __init__(self):
        super().__init__('users.json')

    def add_user(self, user_data):
        user_id = max(user['id'] for user in self.data) + 1 if self.data else 1
        user_data['id'] = user_id
        self.data.append(user_data)
        self.save_data()
        return user_id

class Order(JSONModel):
    def __init__(self):
        super().__init__('orders.json')

    def add_order(self, order_data):
        order_id = max(order['order_id'] for order in self.data) + 1 if self.data else 1
        order_data['order_id'] = order_id
        self.data.append(order_data)
        self.save_data()
        return order_id

    def get_order_by_id(self, order_id):
        return next((order for order in self.data if order['order_id'] == order_id), None)
