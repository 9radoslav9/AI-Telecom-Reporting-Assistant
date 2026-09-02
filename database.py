from supabase import create_client
import os
from dotenv import load_dotenv
from faker import Faker
import random
from datetime import date, timedelta

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)


# plans_data = [
#     {"plan_name": "Basic", "monthly_price": 15.99},
#     {"plan_name": "Standard", "monthly_price": 29.99},
#     {"plan_name": "Premium", "monthly_price": 49.99},
# ]
#
# response = supabase.table("plans").insert(plans_data).execute()
# print(response)
#
#
#
#
# fake = Faker("bg_BG")
#
# bulgarian_regions = [
#     "Благоевград", "Бургас", "Варна", "Велико Търново", "Видин", "Враца",
#     "Габрово", "Добрич", "Кърджали", "Кюстендил", "Ловеч", "Монтана",
#     "Пазарджик", "Перник", "Плевен", "Пловдив", "Разград", "Русе",
#     "Силистра", "Сливен", "Смолян", "София", "Стара Загора", "Търговище",
#     "Хасково", "Шумен", "Ямбол"
# ]
#
# customers_data = []
#
# for i in range(50):
#     customer = {
#         "plan_id": random.choice([1, 2, 3]),
#         "signup_date": fake.date_between(start_date="-2y", end_date="today").isoformat(),
#         "region": random.choice(bulgarian_regions)
#     }
#     customers_data.append(customer)
#
# response = supabase.table("customers").insert(customers_data).execute()
#
# inserted_customers = response.data
#
# print(len(inserted_customers))
# print(inserted_customers[:3])
#
#
# response = supabase.table("customers").select("*").execute()
# inserted_customers = response.data
#
#
# usage_records_data = []
#
# for customer in inserted_customers:
#     for months_ago in range(1, 5):
#         record = {
#             "customer_id": customer["customer_id"],
#             "record_date": (date.today() - timedelta(days=30 * months_ago)).isoformat(),
#             "data_gb": round(random.uniform(0.5, 25.0), 2),
#             "call_minutes": random.randint(0, 500),
#             "sms_count": random.randint(0, 200),
#         }
#         usage_records_data.append(record)
#
# response = supabase.table("usage_records").insert(usage_records_data).execute()
# inserted_usage_records = response.data
#
# print(len(usage_records_data))
# print(usage_records_data[:3])