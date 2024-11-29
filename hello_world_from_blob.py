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


if __name__ == "__main__":
    hello_goodbye_flow("John Doe")