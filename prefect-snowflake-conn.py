from prefect import flow, task
from prefect_snowflake import SnowflakeConnector


@task
def setup_table(block_name: str) -> None:
    with SnowflakeConnector.load(block_name) as connector:
        connector.execute(
            "CREATE TABLE IF NOT EXISTS customers_11 (name varchar, address varchar);"
        )
        connector.execute_many(
            "INSERT INTO customers_11 (name, address) VALUES (%(name)s, %(address)s);",
            seq_of_parameters=[
                {"name": "Ford", "address": "Highway 42"},
                {"name": "Unknown", "address": "Space"},
                {"name": "Me", "address": "Myway 88"},
            ],
        )

@task
def fetch_data(block_name: str) -> list:
    all_rows = []
    with SnowflakeConnector.load(block_name) as connector:
        while True:
            # Repeated fetch* calls using the same operation will
            # skip re-executing and instead return the next set of results
            new_rows = connector.fetch_many("SELECT * FROM customers_11", size=2)
            if len(new_rows) == 0:
                break
            all_rows.append(new_rows)
    return all_rows

@flow
def snowflake_flow(block_name: str) -> list:
    setup_table(block_name)
    #all_rows = fetch_data(block_name)
    #return all_rows

if __name__=="__main__":
    snowflake_flow("snowflake-connection-block")
