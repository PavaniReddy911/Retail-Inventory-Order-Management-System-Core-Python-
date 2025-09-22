import argparse
import json
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService

# Initialize services
product_service = ProductService()
customer_service = CustomerService()
order_service = OrderService()
payment_service = PaymentService()
report_service = ReportService()

# ==================== Product Commands ====================
def cmd_product_add(args):
    result = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
    print(result)

def cmd_product_list(args):
    products = product_service.list_products()
    print(json.dumps(products, indent=2, default=str))

# ==================== Customer Commands ====================
def cmd_customer_add(args):
    result = customer_service.add_customer(args.name, args.email, args.phone, args.city)
    print(result)

def cmd_customer_list(args):
    customers = customer_service.list_customers()
    print(json.dumps(customers, indent=2, default=str))

# ==================== Order Commands ====================
def cmd_order_create(args):
    items = []
    for item in args.item:
        pid, qty = item.split(":")
        items.append({"prod_id": int(pid), "quantity": int(qty)})
    result = order_service.create_order(args.customer, items)
    print(result)

def cmd_order_show(args):
    result = order_service.get_order_details(args.order)
    print(json.dumps(result, indent=2, default=str))

def cmd_order_cancel(args):
    result = order_service.cancel_order(args.order)
    print(result)

def cmd_order_complete(args):
    result = order_service.complete_order(args.order)
    print(result)

def cmd_order_list(args):
    result = order_service.list_orders_by_customer(args.customer)
    print(json.dumps(result, indent=2, default=str))

# ==================== Payment Commands ====================
def cmd_payment_create(args):
    result = payment_service.create_payment_for_order(args.order)
    print(result)

def cmd_payment_process(args):
    result = payment_service.process_payment(args.order, args.method)
    print(result)

def cmd_payment_refund(args):
    result = payment_service.refund_payment(args.order)
    print(result)

# ==================== Report Commands ====================
def cmd_report_top_products(args):
    result = report_service.top_selling_products(args.top)
    print(json.dumps(result, indent=2, default=str))

def cmd_report_revenue(args):
    revenue = report_service.total_revenue_last_month()
    print(f"💰 Total revenue last month: {revenue}")

def cmd_report_orders_by_customer(args):
    result = report_service.orders_by_customer()
    print(json.dumps(result, indent=2, default=str))

def cmd_report_frequent_customers(args):
    result = report_service.frequent_customers(args.min_orders)
    print(json.dumps(result, indent=2, default=str))

# ==================== Build Parser ====================
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product
    p_prod = sub.add_parser("product")
    prod_sub = p_prod.add_subparsers(dest="action")
    addp = prod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category")
    addp.set_defaults(func=cmd_product_add)

    listp = prod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    # Customer
    p_cust = sub.add_parser("customer")
    cust_sub = p_cust.add_subparsers(dest="action")
    addc = cust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city")
    addc.set_defaults(func=cmd_customer_add)

    listc = cust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    # Order
    p_order = sub.add_parser("order")
    order_sub = p_order.add_subparsers(dest="action")
    createo = order_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", nargs="+", required=True, help="prod_id:qty")
    createo.set_defaults(func=cmd_order_create)

    showo = order_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    cano = order_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    compo = order_sub.add_parser("complete")
    compo.add_argument("--order", type=int, required=True)
    compo.set_defaults(func=cmd_order_complete)

    listo = order_sub.add_parser("list")
    listo.add_argument("--customer", type=int, required=True)
    listo.set_defaults(func=cmd_order_list)

    # Payment
    p_pay = sub.add_parser("payment")
    pay_sub = p_pay.add_subparsers(dest="action")
    createp = pay_sub.add_parser("create")
    createp.add_argument("--order", type=int, required=True)
    createp.set_defaults(func=cmd_payment_create)

    processp = pay_sub.add_parser("process")
    processp.add_argument("--order", type=int, required=True)
    processp.add_argument("--method", choices=["Cash","Card","UPI"], required=True)
    processp.set_defaults(func=cmd_payment_process)

    refundp = pay_sub.add_parser("refund")
    refundp.add_argument("--order", type=int, required=True)
    refundp.set_defaults(func=cmd_payment_refund)

    # Reports
    p_report = sub.add_parser("report")
    report_sub = p_report.add_subparsers(dest="action")
    top_products = report_sub.add_parser("top_products")
    top_products.add_argument("--top", type=int, default=5)
    top_products.set_defaults(func=cmd_report_top_products)

    revenue = report_sub.add_parser("revenue_last_month")
    revenue.set_defaults(func=cmd_report_revenue)

    orders_by_cust = report_sub.add_parser("orders_by_customer")
    orders_by_cust.set_defaults(func=cmd_report_orders_by_customer)

    frequent_cust = report_sub.add_parser("frequent_customers")
    frequent_cust.add_argument("--min_orders", type=int, default=2)
    frequent_cust.set_defaults(func=cmd_report_frequent_customers)

    return parser

# ==================== Main ====================
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
