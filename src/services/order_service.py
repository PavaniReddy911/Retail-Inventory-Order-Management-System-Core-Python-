from src.dao import product_dao, order_dao
from src.services import payments_service

class OrderError(Exception):
    pass

class OrderService:

    @staticmethod
    def create_order(cust_id: int, items: list[dict]):
        # Validate customer
        from src.dao import customer_dao
        cust = customer_dao.get_customer_by_id(cust_id)
        if not cust:
            raise OrderError("Customer not found")

        total_amount = 0
        # Check stock & calculate total
        for item in items:
            prod = product_dao.get_product_by_id(item["prod_id"])
            if not prod:
                raise OrderError(f"Product {item['prod_id']} not found")
            if prod["stock"] < item["quantity"]:
                raise OrderError(f"Insufficient stock for product {prod['name']}")
            total_amount += prod["price"] * item["quantity"]

        # Deduct stock
        for item in items:
            prod = product_dao.get_product_by_id(item["prod_id"])
            new_stock = prod["stock"] - item["quantity"]
            product_dao.update_product(prod["prod_id"], {"stock": new_stock})

        # Create order
        order = order_dao.create_order(cust_id, total_amount)
        for item in items:
            prod = product_dao.get_product_by_id(item["prod_id"])
            order_dao.create_order_item(order["order_id"], prod["prod_id"], item["quantity"], prod["price"])

        # Create pending payment
        payments_service.PaymentService.create_payment(order["order_id"], total_amount)
        return order

    @staticmethod
    def get_order_details(order_id: int):
        order = order_dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        items = order_dao.get_order_items(order_id)
        from src.dao import customer_dao
        customer = customer_dao.get_customer_by_id(order["cust_id"])
        return {"order": order, "customer": customer, "items": items}

    @staticmethod
    def cancel_order(order_id: int):
        order = order_dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Only PLACED orders can be cancelled")

        # Restore stock
        items = order_dao.get_order_items(order_id)
        for item in items:
            prod = product_dao.get_product_by_id(item["prod_id"])
            product_dao.update_product(prod["prod_id"], {"stock": prod["stock"] + item["quantity"]})

        # Update order status
        order_dao.update_order(order_id, {"status": "CANCELLED"})

        # Refund payment
        payments_service.PaymentService.refund_payment(order_id)

        return order_dao.get_order_by_id(order_id)
