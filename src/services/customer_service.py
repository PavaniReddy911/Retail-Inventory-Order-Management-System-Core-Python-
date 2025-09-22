# src/services/customer_service.py
from typing import Dict, List
from src.dao.customer_dao import CustomerDAO
from src.dao.order_dao import OrderDAO

class CustomerService:
    """Business logic for customer operations"""

    def __init__(self):
        self.dao = CustomerDAO()
        self.order_dao = OrderDAO()

    def add_customer(self, name: str, email: str, phone: str, city: str = None) -> str:
        if self.dao.get_by_email(email):
            return f"❌ Email already exists: {email}"
        data = {"name": name, "email": email, "phone": phone}
        if city:
            data["city"] = city
        customer = self.dao.create(data)
        return f"✅ Customer added: {customer}" if customer else "❌ Failed to add customer"

    def update_customer(self, customer_id: int, phone: str = None, city: str = None) -> str:
        customer = self.dao.get_by_id(customer_id)
        if not customer:
            return "❌ Customer not found"
        fields = {}
        if phone:
            fields["phone"] = phone
        if city:
            fields["city"] = city
        if not fields:
            return "❌ Nothing to update"
        updated = self.dao.update(customer_id, fields)
        return f"✅ Customer updated: {updated}" if updated else "❌ Failed to update customer"

    def delete_customer(self, customer_id: int) -> str:
        orders = self.order_dao.get_orders_by_customer(customer_id)
        if orders:
            return "❌ Cannot delete: Customer has orders"
        deleted = self.dao.delete(customer_id)
        return f"✅ Customer deleted: {deleted}" if deleted else "❌ Customer not found"

    def list_customers(self, limit: int = 100) -> List[Dict]:
        return self.dao.list_all(limit=limit)

    def search_customers(self, email: str = None, city: str = None) -> List[Dict]:
        return self.dao.search(email=email, city=city)
