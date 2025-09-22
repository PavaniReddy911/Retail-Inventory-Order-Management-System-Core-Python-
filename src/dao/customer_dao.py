# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

def _sb():
    return get_supabase()


class CustomerDAO:
    """Data access object for customer operations"""

    def create(self, payload: Dict) -> Optional[Dict]:
        _sb().table("customers").insert(payload).execute()
        resp = _sb().table("customers").select("*").eq("email", payload["email"]).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_email(self, email: str) -> Optional[Dict]:
        resp = _sb().table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_id(self, customer_id: int) -> Optional[Dict]:
        resp = _sb().table("customers").select("*").eq("customer_id", customer_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update(self, customer_id: int, fields: Dict) -> Optional[Dict]:
        _sb().table("customers").update(fields).eq("customer_id", customer_id).execute()
        resp = _sb().table("customers").select("*").eq("customer_id", customer_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete(self, customer_id: int) -> Optional[Dict]:
        resp_before = _sb().table("customers").select("*").eq("customer_id", customer_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        _sb().table("customers").delete().eq("customer_id", customer_id).execute()
        return row

    def list_all(self, limit: int = 100) -> List[Dict]:
        resp = _sb().table("customers").select("*").order("customer_id").limit(limit).execute()
        return resp.data or []

    def search(self, email: str = None, city: str = None) -> List[Dict]:
        q = _sb().table("customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []
