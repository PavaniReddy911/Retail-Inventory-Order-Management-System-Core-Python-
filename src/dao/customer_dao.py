from typing import Optional, List, Dict
from src.config import get_supabase

def _sb():
    return get_supabase()

def create_customer(name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
    payload = {"name": name, "email": email, "phone": phone}
    if city:
        payload["city"] = city
    _sb().table("customers").insert(payload).execute()
    resp = _sb().table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_customer_by_id(cust_id: int) -> Optional[Dict]:
    resp = _sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_customer_by_name(name: str) -> Optional[Dict]:
    resp = _sb().table("customers").select("*").ilike("name", f"%{name}%").execute()
    return resp.data[0] if resp.data else None

def list_customers(limit: int = 100) -> List[Dict]:
    resp = _sb().table("customers").select("*").limit(limit).execute()
    return resp.data or []

def delete_customer(cust_id: int) -> Optional[Dict]:
    resp_before = _sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    row = resp_before.data[0] if resp_before.data else None
    _sb().table("customers").delete().eq("cust_id", cust_id).execute()
    return row
