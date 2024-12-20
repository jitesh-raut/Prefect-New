from prefect import flow, task

# Define a task to greet by name
@task
def say_hello(name: str):
    print(f"Hello, {name}!")

# Define a task to say goodbye by name
@task
def say_goodbye(name: str):
    print(f"Goodbye, {name}!")

# Define the flow with a name parameter
@flow
def hello_goodbye_flow(name: str):
    say_hello(name)
    say_goodbye(name)

# Deploy the flow

if __name__ == "__main__":
    hello_goodbye_flow.from_source(
        source="https://github.com/jitesh-raut/Prefect-New.git",
        entrypoint="hello_world.py:hello_goodbye_flow",
        ).deploy(
        name="Test Deployment v2", # Name of deployment
        work_pool_name="my-managed-pool",
        image="prefecthq/prefect:3-python3.12.7",
        tags=["Test"],
        parameters={"name": "John Doe"}, # Parameters to pass into floM
        interval=600, # Run interval in seconds (Every 60 seconds)
    )