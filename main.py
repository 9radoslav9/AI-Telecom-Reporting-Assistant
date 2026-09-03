# from aggregation import get_new_customers_by_month, get_revenue_by_region, get_usage_by_plan
# from formatting import format_usage_data
# from LLM import generate_summary
#
# data = get_usage_by_plan()
# formatted = format_usage_data(data)
#
# prompt = f"""Ето данни за потреблението на клиентите:
#
# {formatted}
#
# Направи кратко резюме на тези данни."""
#
# summary = generate_summary(prompt)
# print(summary)



# from aggregation import get_new_customers_by_month
# from formatting import format_new_customers_data
# from LLM import generate_summary
#
# data = get_new_customers_by_month()
# formatted = format_new_customers_data(data)
#
# prompt = f"""Ето данни за нови клиенти по месеци:
#
# {formatted}
#
# Направи кратко резюме на тези данни."""
#
# summary = generate_summary(prompt)
# print(summary)



# from aggregation import get_revenue_by_region
# from formatting import format_revenue_data
# from LLM import generate_summary
# from verification import verify_summary
#
# data = get_revenue_by_region()
# formatted = format_revenue_data(data)
#
# prompt = f"""Ето данни за приходи по региони (в лева):
#
# {formatted}
#
# Направи кратко резюме на тези данни."""
#
# summary = generate_summary(prompt)
# print(summary)
#
# results = verify_summary(data, summary, ["total_revenue"])
# for row, field, status in results:
#     print(row["region"], "-", status)



# from aggregation import get_new_customers_by_month
# from formatting import format_new_customers_data
# from LLM import generate_summary
# from verification import verify_summary
#
# data = get_new_customers_by_month()
# formatted = format_new_customers_data(data)
#
# prompt = f"""Ето данни за нови клиенти по месеци:
#
# {formatted}
#
# Направи кратко резюме на тези данни."""
#
# summary = generate_summary(prompt)
# print(summary)
#
# results = verify_summary(data, summary, ["customer_count"])
# for row, field, status in results:
#     print(row["month"], "-", status)



# from aggregation import get_usage_by_plan
# from formatting import format_usage_data
# from LLM import generate_summary
# from verification import verify_summary
#
# data = get_usage_by_plan()
# formatted = format_usage_data(data)
#
# prompt = f"""Ето данни за консумация по абонаментни планове:
#
# {formatted}
#
# Направи кратко резюме на тези данни."""
#
# summary = generate_summary(prompt)
# print(summary)
#
# results = verify_summary(data, summary, ["total_data_gb", "total_call_minutes", "total_sms_count"])
# for row, field, status in results:
#     print(row["plan_name"], "-", field, "-", status)