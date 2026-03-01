import json
import os
from datetime import datetime

class Product:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

class Inventory:
    def __init__(self, filename="inventory_data.json"):
        self.filename = filename
        self.products = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                for pid, details in data.items():
                    self.products[pid] = Product(
                        details["product_id"],
                        details["name"],
                        details["quantity"],
                        details["price"]
                    )

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump({pid: product.to_dict() for pid, product in self.products.items()}, file, indent=4)

    def add_product(self, product_id, name, quantity, price):
        if product_id in self.products:
            print("❌ Product ID already exists!")
            return
        self.products[product_id] = Product(product_id, name, quantity, price)
        self.save_data()
        print("✅ Product added successfully!")

    def update_product(self, product_id, quantity=None, price=None):
        if product_id not in self.products:
            print("❌ Product not found!")
            return
        if quantity is not None:
            self.products[product_id].quantity = quantity
        if price is not None:
            self.products[product_id].price = price
        self.save_data()
        print("✅ Product updated successfully!")

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_data()
            print("🗑️ Product deleted successfully!")
        else:
            print("❌ Product not found!")

    def search_product(self, product_id):
        if product_id in self.products:
            product = self.products[product_id]
            print(f"\nProduct ID: {product.product_id}")
            print(f"Name: {product.name}")
            print(f"Quantity: {product.quantity}")
            print(f"Price: ₹{product.price}")
            print(f"Total Value: ₹{product.quantity * product.price}")
        else:
            print("❌ Product not found!")

    def view_inventory(self):
        if not self.products:
            print("⚠️ Inventory is empty!")
            return
        print("\n📦 Inventory List:")
        total_value = 0
        for product in self.products.values():
            value = product.quantity * product.price
            total_value += value
            print(f"{product.product_id} | {product.name} | Qty: {product.quantity} | Price: ₹{product.price} | Value: ₹{value}")
        print(f"\n💰 Total Inventory Value: ₹{total_value}")

    def low_stock_alert(self, threshold=5):
        print("\n⚠️ Low Stock Products:")
        found = False
        for product in self.products.values():
            if product.quantity <= threshold:
                print(f"{product.name} (Qty: {product.quantity})")
                found = True
        if not found:
            print("No low stock products!")

def main():
    inventory = Inventory()

    while True:
        print("\n====== PRODUCT INVENTORY MENU ======")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Search Product")
        print("5. View Inventory")
        print("6. Low Stock Alert")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pid = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            qty = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))
            inventory.add_product(pid, name, qty, price)

        elif choice == "2":
            pid = input("Enter Product ID: ")
            qty = input("Enter New Quantity (leave blank if no change): ")
            price = input("Enter New Price (leave blank if no change): ")
            qty = int(qty) if qty else None
            price = float(price) if price else None
            inventory.update_product(pid, qty, price)

        elif choice == "3":
            pid = input("Enter Product ID: ")
            inventory.delete_product(pid)

        elif choice == "4":
            pid = input("Enter Product ID: ")
            inventory.search_product(pid)

        elif choice == "5":
            inventory.view_inventory()

        elif choice == "6":
            inventory.low_stock_alert()

        elif choice == "7":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()