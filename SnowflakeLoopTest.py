from prefect import flow, task
from prefect_snowflake import SnowflakeConnector
import csv

@task
def setup_table_1(block_name: str, num_iterations: int) -> None:
    """
    Creates a Snowflake table named `snowflake_loop_test` and inserts numbers from 1 to `num_iterations`.

    Args:
        block_name (str): The name of the Snowflake connection block.
        num_iterations (int): The number of rows to insert into the table.
    """
    with SnowflakeConnector.load(block_name) as connector:
        # Create the table if it doesn't exist
        connector.execute(
            "CREATE TABLE IF NOT EXISTS snowflake_loop_test (NUM1 integer);"
        )
        
        # Generate numbers dynamically based on num_iterations
        seq_of_parameters = [{"num": i} for i in range(1, num_iterations + 1)]
        
        # Insert numbers into the table
        connector.execute_many(
            "INSERT INTO snowflake_loop_test (NUM1) VALUES (%(num)s);",
            seq_of_parameters=seq_of_parameters,
        )

@task
def fetch_data(block_name: str) -> list:
    """
    Fetches data from the `customers_11` table in batches of 2 rows at a time.

    Args:
        block_name (str): The name of the Snowflake connection block.

    Returns:
        list: A list of rows fetched from the table.
    """
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

@task
def export_table_to_csv(block_name: str, output_file: str):
    """
    Exports data from the `snowflake_loop_test` table in Snowflake to a CSV file.

    Args:
        block_name (str): The name of the Snowflake connection block.
        output_file (str): The path to the output CSV file.

    Raises:
        Exception: If an error occurs during database operations or file writing.
    """
    try:
        # Load the Snowflake connection block
        snowflake_connector = SnowflakeConnector.load(block_name)

        # Open connection
        conn = snowflake_connector.get_connection()
        cursor = conn.cursor()

        # Define your query
        query = "SELECT * FROM snowflake_loop_test"

        # Execute query
        cursor.execute(query)
        if cursor.description:  # Check if there are results
            result = cursor.fetchall()  # Fetch all results from the query
        else:
            result = []

        # Write to CSV
        with open(output_file, "w") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow([col[0] for col in cursor.description])
            # Write data
            writer.writerows(result)
    
    except Exception as e:
        raise

    finally:
        # Close connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@flow
def snowflake_flow(block_name: str) -> list:
    """
    Orchestrates the setup of a Snowflake table, inserts data, and exports it to a CSV file.

    Args:
        block_name (str): The name of the Snowflake connection block.

    Returns:
        list: A list of rows fetched from the table (optional).
    """
    setup_table_1(block_name, 50)
    export_table_to_csv(block_name, 'number_test_output.csv')

if __name__ == "__main__":
    snowflake_flow("snowflake-connection-block")