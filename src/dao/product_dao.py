# src/dao/product_dao.py
from typing import Dict, List, Optional
from src.config import get_supabase


class ProductDAO:
    """Handles raw database operations for products"""

    def __init__(self):
        self.db = get_supabase()

    def create(self, data: Dict) -> Optional[Dict]:
        self.db.table("products").insert(data).execute()
        resp = self.db.table("products").select("*").eq("sku", data["sku"]).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = self.db.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self.db.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        self.db.table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = self.db.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete(self, prod_id: int) -> Optional[Dict]:
        resp = self.db.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        row = resp.data[0] if resp.data else None
        self.db.table("products").delete().eq("prod_id", prod_id).execute()
        return row

    def list_all(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self.db.table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []
