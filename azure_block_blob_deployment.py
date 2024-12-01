from prefect import flow
from prefect_azure import AzureBlobStorageCredentials
from prefect.filesystems import AzureBlobStorage

# Define the flow
@flow
def hello_goodbye_flow():
    print("Hello from the flow!")
    print("Goodbye from the flow!")

if __name__ == "__main__":
    # Define Azure Blob Storage credentials
    connection_string = (
        # "****"
    )
    blob_storage_credentials = AzureBlobStorageCredentials(
        connection_string=connection_string,
    )

    # Define Azure Blob Storage block
    azure_blob_storage_block = AzureBlobStorage(
        container="codestorage",
        blob_storage_credentials=blob_storage_credentials,
    )

    # Deploy the flow
    hello_goodbye_flow.deploy(
        name="my-azure-deployment",
        work_pool_name="my-managed-pool",
        storage=azure_blob_storage_block,  # Specify Azure Blob Storage block
    )
