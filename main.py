from aggregation import get_new_customers_by_month, get_revenue_by_region, get_usage_by_plan
from formatting import format_usage_data
from LLM import generate_summary

data = get_usage_by_plan()
formatted = format_usage_data(data)

prompt = f"""Ето данни за потреблението на клиентите:

{formatted}

Направи кратко резюме на тези данни."""

summary = generate_summary(prompt)
print(summary)

