from src.dao import payments_dao, order_dao

class PaymentError(Exception):
    pass

class PaymentService:

    @staticmethod
    def create_payment(order_id: int, amount: float):
        return payments_dao.create_payment(order_id, amount)

    @staticmethod
    def process_payment(order_id: int, method: str):
        payment = payments_dao.get_payment(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        if payment["status"] == "PAID":
            raise PaymentError("Payment already completed")
        payments_dao.update_payment(order_id, {"status": "PAID", "method": method})
        order_dao.update_order(order_id, {"status": "COMPLETED"})

    @staticmethod
    def refund_payment(order_id: int):
        payment = payments_dao.get_payment(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        payments_dao.update_payment(order_id, {"status": "REFUNDED"})
