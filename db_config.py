import mysql.connector


def make_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="stores"
    )


def create_table(table_name):
    conn = make_connection()
    cursor = conn.cursor()

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        brand_name VARCHAR(255),
        store_ID VARCHAR(255),
        store_branch TEXT,
        store_address TEXT,
        store_phone VARCHAR(100),
        store_timing TEXT,
        map_url TEXT,
        store_url VARCHAR(255) unique,
        menu TEXT,
        city VARCHAR(255),
        page_url TEXT
    )
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def insert_into_db(table_name, data):
    conn = make_connection()
    cursor = conn.cursor()

    query = f"""
    INSERT INTO {table_name} (
        brand_name, store_ID, store_branch, store_address,
        store_phone, store_timing, map_url, store_url,
        menu, city, page_url
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data.get("brand_name"),
        data.get("store_ID"),
        data.get("store_branch"),
        data.get("store_address"),
        data.get("store_phone"),
        data.get("store_timing"),
        data.get("map_url"),
        data.get("store_url"),
        data.get("menu"),
        data.get("city"),
        data.get("page_url")
    )

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()