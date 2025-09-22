# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.services.customer_service import CustomerService
from src.services.product_service import ProductService

class OrderService:
    """Business logic for orders"""

    def __init__(self):
        self.dao = OrderDAO()
        self.customer_service = CustomerService()
        self.product_service = ProductService()

    def create_order(self, customer_id: int, items: List[Dict]) -> str:
        # Check customer exists
        customer = self.customer_service.dao.get_by_id(customer_id)
        if not customer:
            return f"❌ Customer not found: {customer_id}"

        # Check product stock and calculate total
        total_amount = 0
        order_items = []
        for it in items:
            prod = self.product_service.dao.get_product_by_id(it["prod_id"])
            if not prod:
                return f"❌ Product not found: {it['prod_id']}"
            if prod["stock"] < it["quantity"]:
                return f"❌ Not enough stock for {prod['name']} (available: {prod['stock']})"
            # Deduct stock
            new_stock = prod["stock"] - it["quantity"]
            self.product_service.dao.update_product(prod["prod_id"], {"stock": new_stock})
            total_amount += prod["price"] * it["quantity"]
            order_items.append({"prod_id": prod["prod_id"], "quantity": it["quantity"], "price": prod["price"]})

        # Create order
        order = self.dao.create_order(customer_id, total_amount)
        # Add order items
        self.dao.add_order_items(order["id"], order_items)
        return f"✅ Order created: {order}"

    def get_order_details(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            return {"error": "Order not found"}
        items = self.dao.get_items_by_order(order_id)
        customer = self.customer_service.dao.get_by_id(order["customer_id"])
        order["customer"] = customer
        order["items"] = items
        return order

    def cancel_order(self, order_id: int) -> str:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            return "❌ Order not found"
        if order["status"] != "PLACED":
            return "❌ Only PLACED orders can be cancelled"

        # Restore stock
        items = self.dao.get_items_by_order(order_id)
        for it in items:
            prod = self.product_service.dao.get_product_by_id(it["prod_id"])
            self.product_service.dao.update_product(prod["prod_id"], {"stock": prod["stock"] + it["quantity"]})

        updated = self.dao.update_order_status(order_id, "CANCELLED")
        return f"✅ Order cancelled: {updated}"

    def complete_order(self, order_id: int) -> str:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            return "❌ Order not found"
        if order["status"] != "PLACED":
            return "❌ Only PLACED orders can be completed"

        updated = self.dao.update_order_status(order_id, "COMPLETED")
        return f"✅ Order completed: {updated}"

    def list_orders_by_customer(self, customer_id: int) -> List[Dict]:
        return self.dao.get_orders_by_customer(customer_id)
