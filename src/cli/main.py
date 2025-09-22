import argparse
import json
from src.services import product_service, order_service, customer_service

def cmd_product_add(args):
    try:
        prod = product_service.product_class()
        p = prod.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_service.product_class.list_products()
    print(json.dumps(ps, indent=2, default=str))

def cmd_customer_add(args):
    try:
        c = customer_service.CustomerService.create_customer(
            args.name, args.email, args.phone, args.city
        )
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    from src.dao import customer_dao
    cs = customer_dao.list_customers(limit=100)
    print(json.dumps(cs, indent=2, default=str))

def cmd_customer_get(args):
    from src.dao import customer_dao
    row = customer_dao.get_customer_by_name(args.name)
    if row:
        print(json.dumps(row, indent=2, default=str))
    else:
        print("Customer not found.")

def cmd_customer_delete(args):
    from src.dao import customer_dao
    row = customer_dao.delete_customer(args.cust_id)
    if row:
        print("Deleted customer:")
        print(json.dumps(row, indent=2, default=str))
    else:
        print("Customer not found.")

def cmd_order_create(args):
    # items provided as prod_id:qty strings
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service.OrderService.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        o = order_service.OrderService.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_service.OrderService.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # product add/list
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

    # customer add/list/get/delete
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")

    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    getc = pcust_sub.add_parser("get")
    getc.add_argument("--name", required=True)
    getc.set_defaults(func=cmd_customer_get)

    delc = pcust_sub.add_parser("delete")
    delc.add_argument("--cust_id", type=int, required=True)
    delc.set_defaults(func=cmd_customer_delete)

    # order create/show/cancel
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
