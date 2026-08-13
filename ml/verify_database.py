"""Read-only verification checks for the PrediCart SQLite database."""

from pathlib import Path
import sqlite3


DATABASE_PATH = Path("data") / "predicart.db"


def get_read_only_connection():
    """Open the database in read-only mode so verification cannot change it."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database was not found at {DATABASE_PATH}. Run ml/database.py first."
        )

    database_uri = f"file:{DATABASE_PATH.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(database_uri, uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def main():
    with get_read_only_connection() as connection:
        counts = {
            "products": connection.execute("SELECT COUNT(*) FROM products").fetchone()[0],
            "sales records": connection.execute("SELECT COUNT(*) FROM sales").fetchone()[0],
            "events": connection.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "inventory records": connection.execute(
                "SELECT COUNT(*) FROM inventory"
            ).fetchone()[0],
            "purchase-history records": connection.execute(
                "SELECT COUNT(*) FROM purchase_history"
            ).fetchone()[0],
        }
        sales_dates = connection.execute(
            "SELECT MIN(date) AS earliest, MAX(date) AS latest FROM sales"
        ).fetchone()
        inventory = connection.execute(
            """
            SELECT products.id, products.name, inventory.current_stock, inventory.incoming_stock
            FROM products
            LEFT JOIN inventory ON inventory.product_id = products.id
            ORDER BY products.id
            """
        ).fetchall()
        events = connection.execute(
            "SELECT date, name, type FROM events ORDER BY date, name"
        ).fetchall()
        product_sales = connection.execute(
            """
            SELECT
                products.id AS product_id,
                products.name AS product_name,
                COUNT(sales.id) AS sales_count,
                MIN(sales.date) AS earliest_sale_date,
                MAX(sales.date) AS latest_sale_date
            FROM products
            LEFT JOIN sales ON sales.product_id = products.id
            GROUP BY products.id, products.name
            ORDER BY products.id
            """
        ).fetchall()

    print("PrediCart database verification")
    for label, count in counts.items():
        print(f"Number of {label}: {count}")
    print(f"Earliest sales date: {sales_dates['earliest']}")
    print(f"Latest sales date: {sales_dates['latest']}")

    print("\nProducts and inventory:")
    for product in inventory:
        print(
            f"{product['id']} | {product['name']} | "
            f"current_stock={product['current_stock']} | "
            f"incoming_stock={product['incoming_stock']}"
        )

    print("\nEvents:")
    for event in events:
        print(f"{event['date']} | {event['name']} | {event['type']}")

    print("\nSales records by product:")
    all_products_have_sales = True
    for product in product_sales:
        has_sales = product["sales_count"] > 0
        all_products_have_sales &= has_sales
        print(
            f"{product['product_id']} | {product['product_name']} | "
            f"sales_records={product['sales_count']} | "
            f"earliest={product['earliest_sale_date']} | "
            f"latest={product['latest_sale_date']}"
        )

    print(f"\nEvery product has sales records: {all_products_have_sales}")


if __name__ == "__main__":
    main()
