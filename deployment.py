from prefect import flow
from prefect.runner.storage import GitRepository
from prefect_github import GitHubCredentials


if __name__ == "__main__":

    github_repo = GitRepository(
        url="https://github.com/jitesh-raut/Prefect-New.git",
        credentials=GitHubCredentials.load("git-credentials-blocks"),
    )

    flow.from_source(
        source=github_repo,
        entrypoint="hello_world.py:hello_goodbye_flow",
    ).deploy(
        name="Test Deployment v2", # Name of deployment
        work_pool_name="my-test-work-pool",
        image="prefecthq/prefect:3-python3.12.7",
        tags=["Test"],
        parameters={"name": "John Doe"}, # Parameters to pass into floM
        interval=600, # Run interval in seconds (Every 60 seconds)
    )
