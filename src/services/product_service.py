# src/services/product_service.py
from typing import Dict, List
from src.dao.product_dao import ProductDAO


class ProductService:
    """Business logic for products"""

    def __init__(self):
        self.dao = ProductDAO()

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> str:
        if price <= 0:
            return "❌ Price must be greater than 0"

        if self.dao.get_by_sku(sku):
            return f"❌ SKU already exists: {sku}"

        data = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            data["category"] = category

        product = self.dao.create(data)
        return f"✅ Product added: {product}" if product else "❌ Failed to add product"

    def restock_product(self, prod_id: int, delta: int) -> str:
        if delta <= 0:
            return "❌ Delta must be positive"

        product = self.dao.get_by_id(prod_id)
        if not product:
            return "❌ Product not found"

        new_stock = (product.get("stock") or 0) + delta
        updated = self.dao.update(prod_id, {"stock": new_stock})
        return f"✅ Stock updated: {updated}" if updated else "❌ Failed to update stock"

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        all_products = self.dao.list_all(limit=1000)
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]

    def list_products(self, limit: int = 100) -> List[Dict]:
        return self.dao.list_all(limit=limit)
