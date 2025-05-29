import ray
import argparse
from merchant import MerchantActor

parser = argparse.ArgumentParser()
parser.add_argument("--merchant-id", required=True)
args = parser.parse_args()

ray.init(address='auto')  # Connect to Ray head node

# Register the merchant actor
actor = MerchantActor.options(name=args.merchant_id, lifetime="detached").remote(args.merchant_id)

print(f"[Merchant {args.merchant_id}] Registered and ready.")

# Keep running (actors live in background)
import time
while True:
    time.sleep(60)
