import httpx
from prefect import flow


@flow(log_prints=True)
def get_repo_info(repo_name: str = "Prefect-New"):
    url = "https://github.com/jitesh-raut/Prefect-New"
    response = httpx.get(url)
    response.raise_for_status()
    repo = response.json()
    print(f"{repo_name} repository statistics 🤓:")
    print(f"Stars 🌠 : {repo['stargazers_count']}")
    print(f"Forks 🍴 : {repo['forks_count']}")


if __name__ == "__main__":
    get_repo_info.from_source(
        source="https://github.com/jitesh-raut/Prefect-New.git", 
        entrypoint="repo_info.py:get_repo_info"
    ).deploy(
        name="my-deployment_v3", 
        work_pool_name="my-managed-pool", 
    )