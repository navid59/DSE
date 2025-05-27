import ray

ray.init(address='auto')

def route_order(merchant_id, product_id, quantity):
    try:
        merchant = ray.get_actor(merchant_id)
        result = merchant.place_order.remote(product_id, quantity)
        return ray.get(result)
    except ValueError:
        return f"Merchant {merchant_id} not found."

# Example usage
if __name__ == "__main__":
    print("[Coordinator] Sending test orders...")
    result1 = route_order("merchant_a", "book", 1)
    print("Response:", result1)

    result2 = route_order("merchant_b", "pen", 5)
    print("Response:", result2)
