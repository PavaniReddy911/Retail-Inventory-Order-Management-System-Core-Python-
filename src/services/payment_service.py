from typing import Dict
from src.dao.payment_dao import PaymentDAO
from src.dao.order_dao import OrderDAO

class PaymentService:
    """Handles payments for orders"""

    def __init__(self):
        self.payment_dao = PaymentDAO()
        self.order_dao = OrderDAO()

    def create_payment_for_order(self, order_id: int) -> str:
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            return "❌ Order not found"
        payment = self.payment_dao.create({
            "order_id": order_id,
            "amount": order.get("total_amount", 0),
            "status": "PENDING"
        })
        return f"✅ Payment created: {payment}"

    def process_payment(self, order_id: int, method: str) -> str:
        payment = self.payment_dao.get_by_order(order_id)
        if not payment:
            return "❌ Payment record not found"
        if payment["status"] != "PENDING":
            return f"❌ Payment already {payment['status']}"

        updated = self.payment_dao.update(payment["payment_id"], {
            "status": "PAID",
            "method": method
        })
        # Mark order as completed
        self.order_dao.update(order_id, {"status": "COMPLETED"})
        return f"✅ Payment processed and order completed: {updated}"

    def refund_payment(self, order_id: int) -> str:
        payment = self.payment_dao.get_by_order(order_id)
        if not payment:
            return "❌ Payment record not found"

        updated = self.payment_dao.update(payment["payment_id"], {"status": "REFUNDED"})
        return f"✅ Payment refunded: {updated}"
