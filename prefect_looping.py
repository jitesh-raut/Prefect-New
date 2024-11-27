from prefect_snowflake.database import SnowflakeConnector

with SnowflakeConnector.load("snowflake-connection-block") as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS customers (name varchar, address varchar);"
    )
    conn.execute_many(
        "INSERT INTO customers (name, address) VALUES (%(name)s, %(address)s);",
        seq_of_parameters=[
            {"name": "Ford", "address": "Highway 42"},
            {"name": "Unknown", "address": "Space"},
            {"name": "Me", "address": "Myway 88"},
        ],
    )
    results = conn.fetch_all(
        "SELECT * FROM customers WHERE address = %(address)s",
        parameters={"address": "Space"}
    )
    print(results)
