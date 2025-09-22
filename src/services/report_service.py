from src.dao.order_dao import OrderDAO
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import CustomerDAO
from datetime import datetime, timedelta
from collections import Counter

class ReportService:
    """Generates sales reports"""

    def __init__(self):
        self.order_dao = OrderDAO()
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()

    def top_selling_products(self, top_n: int = 5):
        orders = self.order_dao.list_all_orders()
        all_items = []
        for o in orders:
            for item in o.get("items", []):
                all_items.append(item["prod_id"])
        counter = Counter(all_items)
        top_products = counter.most_common(top_n)
        return [
            {"prod_id": pid, "quantity": qty, "name": self.product_dao.get_product_by_id(pid)["name"]}
            for pid, qty in top_products
        ]

    def total_revenue_last_month(self):
        now = datetime.utcnow()
        last_month = now - timedelta(days=30)
        orders = self.order_dao.list_all_orders()
        revenue = sum(o.get("total_amount", 0) for o in orders if datetime.fromisoformat(o["created_at"]) >= last_month)
        return revenue

    def orders_by_customer(self):
        orders = self.order_dao.list_all_orders()
        counter = Counter(o["customer_id"] for o in orders)
        return [{"customer_id": cid, "total_orders": count} for cid, count in counter.items()]

    def frequent_customers(self, min_orders: int = 2):
        data = self.orders_by_customer()
        return [self.customer_dao.get_by_id(d["customer_id"]) for d in data if d["total_orders"] > min_orders]
