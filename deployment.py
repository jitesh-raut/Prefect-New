from prefect import flow

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/jitesh-raut/Prefect-New.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="hello_world.py:hello_goodbye_flow", # Specific flow to run
    ).deploy(
        name="my-first-deployment",
        work_pool_name="my-managed-pool", # Work pool target
        cron="* * * * *", # Cron schedule (every minute)
    )

