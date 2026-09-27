import os
import time
from datetime import datetime

import mysql.connector
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "60"))
QPS_THRESHOLD = float(os.getenv("QPS_THRESHOLD", "100"))


def connect_mysql():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )


def get_status_variables(connection):
    cursor = connection.cursor()

    variables = [
        "Threads_connected",
        "Threads_running",
        "Questions",
        "Queries",
        "Uptime",
        "Slow_queries"
    ]

    results = {}

    for variable in variables:
        cursor.execute(
            "SHOW GLOBAL STATUS LIKE %s",
            (variable,)
        )

        row = cursor.fetchone()

        if row:
            results[row[0]] = int(row[1])

    cursor.close()

    return results


def display_dashboard(status, qps):
    print("\033[2J\033[H", end="")

    print("=" * 60)
    print("             MYSQL STATUS DASHBOARD")
    print("=" * 60)

    print(
        f"Last updated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    table = [
        ["Threads Connected", status.get("Threads_connected", 0)],
        ["Threads Running", status.get("Threads_running", 0)],
        ["Questions", status.get("Questions", 0)],
        ["Queries", status.get("Queries", 0)],
        ["Uptime (seconds)", status.get("Uptime", 0)],
        ["Slow Queries", status.get("Slow_queries", 0)],
        ["Queries Per Second", f"{qps:.2f}"]
    ]

    print()

    print(
        tabulate(
            table,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )

    print()

    if qps > QPS_THRESHOLD:
        print(
            f"ALERT: QPS ({qps:.2f}) exceeded "
            f"threshold ({QPS_THRESHOLD:.2f})!"
        )
    else:
        print(
            f"QPS is within the limit "
            f"(threshold: {QPS_THRESHOLD:.2f})"
        )

    print()
    print(f"Next refresh in {REFRESH_INTERVAL} seconds...")


def main():
    previous_queries = None
    previous_time = None

    print("Connecting to MySQL...")

    try:
        connection = connect_mysql()

        print("Connected successfully.")
        time.sleep(2)

        while True:
            status = get_status_variables(connection)

            current_queries = status.get("Queries", 0)
            current_time = time.time()

            if previous_queries is None:
                qps = 0.0
            else:
                query_difference = current_queries - previous_queries
                time_difference = current_time - previous_time

                if time_difference > 0:
                    qps = query_difference / time_difference
                else:
                    qps = 0.0

            display_dashboard(status, qps)

            previous_queries = current_queries
            previous_time = current_time

            time.sleep(REFRESH_INTERVAL)

    except KeyboardInterrupt:
        print("\nDashboard stopped by user.")

    except mysql.connector.Error as error:
        print(f"\nMySQL error: {error}")

    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()