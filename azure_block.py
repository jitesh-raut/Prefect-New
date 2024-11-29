from prefect import flow
from prefect_azure import AzureBlobCredentials, AzureBlobStorage

if __name__ == "__main__":

    azure_blob_storage_block = AzureBlobStorage(   
        container="codestorage",
        folder="prefect",
        credentials=AzureBlobCredentials.load("my-code-cred-block")
    )

    flow.from_source(source=azure_blob_storage_block, entrypoint="hello_world_from_blob.py:hello_goodbye_flow").deploy(
        name="my-azure-deployment_from_blob_storage_source", work_pool_name="my-managed-pool"
    )