from prefect import flow

from prefect_azure import AzureBlobStorageCredentials
from prefect_azure.blob_storage import blob_storage_download

@flow
def example_blob_storage_download_flow():
    connection_string = "DefaultEndpointsProtocol=https;AccountName=storageprefectexp;AccountKey=igKnSDj4w6l67t7yi+V7ngpFdzOY4lCPokBZiYmpvHyBB7yrv1BBnupO+1LXU59syEZmc43NyxvX+AStQh1l6Q==;EndpointSuffix=core.windows.net"
    blob_storage_credentials = AzureBlobStorageCredentials(
        connection_string=connection_string,
    )
    data = blob_storage_download(
        blob="prefect/prefect.txt",
        container="codestorage",
        blob_storage_credentials=blob_storage_credentials,
    )
    return data

example_blob_storage_download_flow()
