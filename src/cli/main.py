# src/cli/main.py
import argparse
import json

from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService

# Initialize services
product_service = ProductService()
customer_service = CustomerService()
order_service = OrderService()


# ----------------- Product Handlers -----------------
def cmd_product_add(args):
    items = product_service.add_product(
        args.name, args.sku, args.price, args.stock, args.category
    )
    print(items)


def cmd_product_list(args):
    products = product_service.list_products()
    print(json.dumps(products, indent=2))


# ----------------- Customer Handlers -----------------
def cmd_customer_add(args):
    result = customer_service.add_customer(
        args.name, args.email, args.phone, args.city
    )
    print(result)


def cmd_customer_update(args):
    result = customer_service.update_customer(
        args.customer, args.phone, args.city
    )
    print(result)


def cmd_customer_delete(args):
    result = customer_service.delete_customer(args.customer)
    print(result)


def cmd_customer_list(args):
    customers = customer_service.list_customers()
    print(json.dumps(customers, indent=2))


def cmd_customer_search(args):
    customers = customer_service.search_customers(args.email, args.city)
    print(json.dumps(customers, indent=2))


# ----------------- Order Handlers -----------------
def cmd_order_create(args):
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    result = order_service.create_order(args.customer, items)
    print(result)


def cmd_order_show(args):
    print(json.dumps(order_service.get_order_details(args.order), indent=2))


def cmd_order_cancel(args):
    result = order_service.cancel_order(args.order)
    print(result)


def cmd_order_complete(args):
    result = order_service.complete_order(args.order)
    print(result)


def cmd_order_list(args):
    orders = order_service.list_orders_by_customer(args.customer)
    print(json.dumps(orders, indent=2))


# ----------------- Build CLI -----------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # -------- Product CLI --------
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")

    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)

    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    # -------- Customer CLI --------
    pcust = sub.add_parser("customer", help="customer commands")
    pcust_sub = pcust.add_subparsers(dest="action")

    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    updatec = pcust_sub.add_parser("update")
    updatec.add_argument("--customer", type=int, required=True)
    updatec.add_argument("--phone", default=None)
    updatec.add_argument("--city", default=None)
    updatec.set_defaults(func=cmd_customer_update)

    deletec = pcust_sub.add_parser("delete")
    deletec.add_argument("--customer", type=int, required=True)
    deletec.set_defaults(func=cmd_customer_delete)

    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    searchc = pcust_sub.add_parser("search")
    searchc.add_argument("--email", default=None)
    searchc.add_argument("--city", default=None)
    searchc.set_defaults(func=cmd_customer_search)

    # -------- Order CLI --------
    porder = sub.add_parser("order", help="order commands")
    porder_sub = porder.add_subparsers(dest="action")

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument(
        "--item", required=True, nargs="+", help="prod_id:qty (repeatable)"
    )
    createo.set_defaults(func=cmd_order_create)

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    completeo = porder_sub.add_parser("complete")
    completeo.add_argument("--order", type=int, required=True)
    completeo.set_defaults(func=cmd_order_complete)

    listo = porder_sub.add_parser("list")
    listo.add_argument("--customer", type=int, required=True)
    listo.set_defaults(func=cmd_order_list)

    return parser


# ----------------- Main -----------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
