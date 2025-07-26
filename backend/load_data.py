# backend/scripts/load_data.py

import csv
import os
import sys

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Product
from sqlalchemy.orm import Session

def load_products_from_csv(file_path: str):
    db: Session = SessionLocal()
    try:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return

        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                # Skip if critical fields are missing
                if not row["product_id"] or not row["product_name"]:
                    continue

                try:
                    price = float(row["price"]) if row["price"] else 0.0
                except ValueError:
                    print(f"⚠️ Skipping row with invalid price: {row['price']}")
                    continue

                product = Product(
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    category=row.get("category", ""),
                    price=price,
                    description=row.get("description", "")
                )
                db.add(product)
                count += 1

            db.commit()
            print(f"✅ Loaded {count} products successfully!")

    except Exception as e:
        print("❌ Error loading products:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_products_from_csv("products.csv")