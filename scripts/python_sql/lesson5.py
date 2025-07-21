from db_connection import get_connection
conn = get_connection()


def get_order_sum(conn, month):
    query = """SELECT
                customer_name,
                EXTRACT(MONTH FROM order_date) as month,
                SUM(total_amount)
            FROM orders AS o
            JOIN customers AS c
            ON o.customer_id = c.customer_id
            GROUP BY customer_name, order_date
            HAVING EXTRACT(MONTH FROM order_date) = %s;"""
    result = []

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (month,))
        rows = cur.fetchall()
        for row in rows:
            text = f'Покупатель {row[0]} совершил покупок на сумму {row[2]}'
            result.append(text)
    result = '\n'.join(result)

    print(result)
    return result

# end
get_order_sum(conn, 2)
conn.close()

