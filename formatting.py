def format_revenue_data(data: list[dict]) -> str:
    lines = []
    for row in data:
        lines.append(f"{row['region']}: {row['total_revenue']} лв.")
    return "\n".join(lines)


def format_new_customers_data(data: list[dict]) -> str:
    lines = []
    for row in data:
        lines.append(f"{row['month']}: {row['customer_count']} нови клиента")
    return "\n".join(lines)


def format_usage_data(data: list[dict]) -> str:
    lines = []
    for row in data:
        lines.append(
            f"{row['plan_name']}: {row['total_data_gb']} GB общо данни, "
            f"{row['total_call_minutes']} мин. общо разговори, "
            f"{row['total_sms_count']} SMS общо"
        )
    return "\n".join(lines)