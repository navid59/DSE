import ray

@ray.remote
class MerchantActor:
    def __init__(self, merchant_id):
        self.merchant_id = merchant_id
        self.inventory = {}

    def add_product(self, product_id, stock):
        self.inventory[product_id] = stock
        return f"{stock} of {product_id} added."

    def place_order(self, product_id, quantity):
        if product_id not in self.inventory:
            return "Product not found."
        if self.inventory[product_id] < quantity:
            return "Out of stock."
        self.inventory[product_id] -= quantity
        return f"Order successful for {quantity} of {product_id}"
