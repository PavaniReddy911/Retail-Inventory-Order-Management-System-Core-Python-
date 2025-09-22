# src/dao/order_dao.py
from typing import List, Dict
from src.config import get_supabase

def _sb():
    return get_supabase()


class OrderDAO:
    """Data access for orders"""

    def create_order(self, customer_id: int, total_amount: float) -> Dict:
        """Insert into orders table and return the created order"""
        payload = {"customer_id": customer_id, "total_amount": total_amount, "status": "PLACED"}
        resp = _sb().table("orders").insert(payload).execute()
        # Fetch the inserted order (assuming auto-increment id)
        order_id = resp.data[0]["id"]
        order = _sb().table("orders").select("*").eq("id", order_id).limit(1).execute()
        return order.data[0] if order.data else {}

    def add_order_items(self, order_id: int, items: List[Dict]) -> None:
        """Insert multiple items into order_items table"""
        for item in items:
            payload = {
                "order_id": order_id,
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }
            _sb().table("order_items").insert(payload).execute()

    def get_order_by_id(self, order_id: int) -> Dict:
        """Return order info"""
        resp = _sb().table("orders").select("*").eq("id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else {}

    def get_items_by_order(self, order_id: int) -> List[Dict]:
        """Return all items of an order"""
        resp = _sb().table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []

    def get_orders_by_customer(self, customer_id: int) -> List[Dict]:
        """Return all orders of a customer"""
        resp = _sb().table("orders").select("*").eq("customer_id", customer_id).execute()
        return resp.data or []

    def update_order_status(self, order_id: int, status: str) -> Dict:
        """Update status and return updated row"""
        _sb().table("orders").update({"status": status}).eq("id", order_id).execute()
        return self.get_order_by_id(order_id)
