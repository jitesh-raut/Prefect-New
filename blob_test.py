from prefect import flow
from prefect_azure import AzureBlobStorageCredentials
from prefect_azure.blob_storage import blob_storage_download

@flow
async def example_blob_storage_download_flow():
    # connection_string = (
    #     "DefaultEndpointsProtocol=https;AccountName=storageprefectexp;"
    #     "AccountKey=igKnSDj4w6l67t7yi+V7ngpFdzOY4lCPokBZiYmpvHyBB7yrv1BBnupO+1LXU59syEZmc43NyxvX+AStQh1l6Q==;"
    #     "EndpointSuffix=core.windows.net"
    # )
    blob_storage_credentials = AzureBlobStorageCredentials(
        connection_string=connection_string,
    )
    # Await the async blob_storage_download call
    data = await blob_storage_download(
        blob="prefect/prefect.txt",
        container="codestorage",
        blob_storage_credentials=blob_storage_credentials,
    )
    print("Downloaded data:")
    print(data.decode("utf-8"))
    return data

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_blob_storage_download_flow())