import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Gopinath",
        database="sales_quotes"
    )

def insert_quote(customer, brand, model, price, quote_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quotes (customer_name, brand, model, price, quote_text)
        VALUES (%s, %s, %s, %s, %s)
    """, (customer, brand, model, price, quote_text))
    conn.commit()
    quote_id = cursor.lastrowid
    conn.close()
    return quote_id

def fetch_all_quotes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quotes ORDER BY created_at DESC")
    quotes = cursor.fetchall()
    conn.close()
    return quotes