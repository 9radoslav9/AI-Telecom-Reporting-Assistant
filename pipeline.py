from aggregation import get_revenue_by_region, get_new_customers_by_month, get_usage_by_plan
from formatting import format_revenue_data, format_new_customers_data, format_usage_data
from LLM import generate_summary
from verification import verify_summary


def run_pipeline(question: str) -> dict:
    if question == "revenue":
        data = get_revenue_by_region()
        formatted_text = format_revenue_data(data)
        fields_to_check = ["total_revenue"]
    elif question == "customers":
        data = get_new_customers_by_month()
        formatted_text = format_new_customers_data(data)
        fields_to_check = ["customer_count"]
    elif question == "usage":
        data = get_usage_by_plan()
        formatted_text = format_usage_data(data)
        fields_to_check = ["total_data_gb", "total_call_minutes", "total_sms_count"]
    else:
        raise ValueError(f"Непознат въпрос: {question}")

    summary = generate_summary(formatted_text)
    verification_result = verify_summary(data, summary, fields_to_check)

    return {
        "question": question,
        "data": data,
        "summary": summary,
        "verification": verification_result,
    }