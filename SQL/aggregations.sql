-- Брой нови клиенти по месец на регистрация, само от customers таблицата. / New Customers By Month
CREATE OR REPLACE FUNCTION new_customers_by_month()
RETURNS TABLE(month TEXT, customer_count BIGINT)
LANGUAGE SQL
AS $$
    SELECT
        TO_CHAR(signup_date::date, 'YYYY-MM') AS month,
        COUNT(*) AS customer_count
    FROM customers
    GROUP BY month
    ORDER BY month;
$$;



-- Общ приход по регион (join между customers и plans) / Revenue By Region
CREATE OR REPLACE FUNCTION revenue_by_region()
RETURNS TABLE(region TEXT, total_revenue NUMERIC)
LANGUAGE SQL
AS $$
    SELECT
        c.region AS region,
        SUM(p.monthly_price) AS total_revenue
    FROM customers AS c
    JOIN plans AS p ON p.plan_id = c.plan_id
    GROUP BY c.region
    ORDER BY total_revenue DESC;
$$;



-- Обща и средна употреба (data/минути/SMS) по план, през CTE. / Usage By Plan
CREATE OR REPLACE FUNCTION usage_by_plan()
RETURNS TABLE(
    plan_name TEXT,
    total_data_gb NUMERIC,
    total_call_minutes NUMERIC,
    total_sms_count NUMERIC,
    avg_data_gb_per_customer NUMERIC,
    avg_call_minutes_per_customer NUMERIC,
    avg_sms_count_per_customer NUMERIC
)
LANGUAGE SQL
AS $$
    WITH customer_usage AS (
        SELECT
            c.customer_id AS customer_id,
            p.plan_name AS plan_name,
            SUM(u.data_gb) AS customer_data_gb,
            SUM(u.call_minutes) AS customer_call_minutes,
            SUM(u.sms_count) AS customer_sms_count
        FROM usage_records AS u
        JOIN customers AS c ON c.customer_id = u.customer_id
        JOIN plans AS p ON p.plan_id = c.plan_id
        GROUP BY c.customer_id, p.plan_name
    )
    SELECT
        plan_name,
        SUM(customer_data_gb) AS total_data_gb,
        SUM(customer_call_minutes) AS total_call_minutes,
        SUM(customer_sms_count) AS total_sms_count,
        AVG(customer_data_gb) AS avg_data_gb_per_customer,
        AVG(customer_call_minutes) AS avg_call_minutes_per_customer,
        AVG(customer_sms_count) AS avg_sms_count_per_customer
    FROM customer_usage
    GROUP BY plan_name
    ORDER BY total_data_gb DESC;
$$;