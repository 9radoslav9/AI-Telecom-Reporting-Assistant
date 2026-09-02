from database import supabase


def get_new_customers_by_month():
    response = supabase.rpc("new_customers_by_month").execute()
    return response.data


def get_revenue_by_region():
    response = supabase.rpc("revenue_by_region").execute()
    return response.data


def get_usage_by_plan():
    response = supabase.rpc("usage_by_plan").execute()
    return response.data