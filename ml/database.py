"""SQLite database helpers for PrediCart's generated sales data."""

from pathlib import Path
import sqlite3

import pandas as pd

from data_generator import BASE_DEMAND, FESTIVALS_AND_HOLIDAYS, PRODUCTS


DATABASE_PATH = Path("data") / "predicart.db"
SALES_DATA_PATH = Path("data") / "sales.csv"


def _get_connection():
    """Open a database connection with foreign-key checks enabled."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all PrediCart tables if they do not already exist."""
    with _get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                date TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS inventory (
                product_id TEXT PRIMARY KEY,
                current_stock INTEGER NOT NULL CHECK (current_stock >= 0),
                incoming_stock INTEGER NOT NULL CHECK (incoming_stock >= 0),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );

            CREATE TABLE IF NOT EXISTS purchase_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                date TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_sales_product_date
            ON sales (product_id, date);

            CREATE UNIQUE INDEX IF NOT EXISTS idx_events_date_name_type
            ON events (date, name, type);

            CREATE UNIQUE INDEX IF NOT EXISTS idx_purchase_history_product_date
            ON purchase_history (product_id, date);
            """
        )


def insert_products(products):
    """Insert or update product records from dictionaries with product_id, name, and category."""
    rows = [
        (product.get("product_id", product.get("id")), product["name"], product["category"])
        for product in products
    ]
    with _get_connection() as connection:
        connection.executemany(
            """
            INSERT INTO products (id, name, category)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET name = excluded.name, category = excluded.category
            """,
            rows,
        )


def insert_sales(sales_records):
    """Insert sales records containing product_id, date, and quantity."""
    rows = [
        (record["product_id"], str(record["date"]), int(record["quantity"]))
        for record in sales_records
    ]
    with _get_connection() as connection:
        connection.executemany(
            "INSERT OR IGNORE INTO sales (product_id, date, quantity) VALUES (?, ?, ?)",
            rows,
        )


def insert_events(events):
    """Insert event records containing date, name, and type."""
    rows = [
        (str(event["date"]), event["name"], event["type"])
        for event in events
    ]
    with _get_connection() as connection:
        connection.executemany(
            "INSERT OR IGNORE INTO events (date, name, type) VALUES (?, ?, ?)", rows
        )


def insert_inventory(inventory_records):
    """Insert or update inventory records containing current and incoming stock."""
    rows = [
        (
            record["product_id"],
            int(record["current_stock"]),
            int(record["incoming_stock"]),
        )
        for record in inventory_records
    ]
    with _get_connection() as connection:
        connection.executemany(
            """
            INSERT INTO inventory (product_id, current_stock, incoming_stock)
            VALUES (?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE SET
                current_stock = excluded.current_stock,
                incoming_stock = excluded.incoming_stock
            """,
            rows,
        )


def insert_purchase_history(purchase_records):
    """Insert purchase records containing product_id, date, and quantity."""
    rows = [
        (record["product_id"], str(record["date"]), int(record["quantity"]))
        for record in purchase_records
    ]
    with _get_connection() as connection:
        connection.executemany(
            "INSERT OR IGNORE INTO purchase_history (product_id, date, quantity) VALUES (?, ?, ?)",
            rows,
        )


def get_product_sales(product_id):
    """Return all sales records for a product ordered by date."""
    with _get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, product_id, date, quantity
            FROM sales
            WHERE product_id = ?
            ORDER BY date
            """,
            (product_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_events(start_date, end_date):
    """Return events within an inclusive date range."""
    with _get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, date, name, type
            FROM events
            WHERE date BETWEEN ? AND ?
            ORDER BY date
            """,
            (str(start_date), str(end_date)),
        ).fetchall()
    return [dict(row) for row in rows]


def _create_initial_inventory():
    """Create practical starting stock levels from each product's base daily demand."""
    return [
        {
            "product_id": product["product_id"],
            "current_stock": BASE_DEMAND[product["product_id"]] * 14,
            "incoming_stock": BASE_DEMAND[product["product_id"]] * 7,
        }
        for product in PRODUCTS
    ]


def _create_purchase_history(start_date):
    """Create three simple, recurring-style replenishment records per product."""
    purchase_dates = pd.date_range(start=start_date, periods=3, freq="180D")
    return [
        {
            "product_id": product["product_id"],
            "date": purchase_date.date().isoformat(),
            "quantity": BASE_DEMAND[product["product_id"]] * 30,
        }
        for product in PRODUCTS
        for purchase_date in purchase_dates
    ]


def populate_database():
    """Load configured products, generated sales, demo events, and stock records."""
    if not SALES_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Sales data was not found at {SALES_DATA_PATH}. Run ml/data_generator.py first."
        )

    sales_data = pd.read_csv(SALES_DATA_PATH, parse_dates=["date"])
    sales_data["date"] = sales_data["date"].dt.date.astype(str)
    insert_products(PRODUCTS)
    insert_sales(sales_data.to_dict(orient="records"))

    years = sorted(pd.to_datetime(sales_data["date"]).dt.year.unique())
    events = [
        {
            "date": pd.Timestamp(
                year=year,
                month=pd.Timestamp(festival["date"]).month,
                day=pd.Timestamp(festival["date"]).day,
            ).date().isoformat(),
            "name": festival["name"],
            "type": "festival",
        }
        for festival in FESTIVALS_AND_HOLIDAYS
        for year in years
    ]
    insert_events(events)
    insert_inventory(_create_initial_inventory())
    insert_purchase_history(_create_purchase_history(sales_data["date"].min()))

    return {
        "products": len(PRODUCTS),
        "sales": len(sales_data),
        "events": len(events),
        "inventory_records": len(PRODUCTS),
        "purchase_history_records": len(PRODUCTS) * 3,
    }


if __name__ == "__main__":
    initialize_database()
    summary = populate_database()
    print("PrediCart database populated successfully.")
    print(f"Products: {summary['products']}")
    print(f"Sales records: {summary['sales']}")
    print(f"Events: {summary['events']}")
    print(f"Inventory records: {summary['inventory_records']}")
    print(f"Purchase-history records: {summary['purchase_history_records']}")
    print(f"Database file: {DATABASE_PATH}")
