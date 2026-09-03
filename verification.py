def verify_summary(data, summary_text, fields_to_check):
    results = []

    for row in data:
        for field in fields_to_check:
            expected_value = row[field]
            expected_text = str(expected_value)

            if expected_text in summary_text:
                status = "намерено"
            else:
                status = "липсва"

            results.append((row, field, status))

    return results