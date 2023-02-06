from dask.distributed import Client, LocalCluster

from mpo.utils import RegistersMPOConstruct


@RegistersMPOConstruct(
    construct_name="runners", construct_key="LocalClusterClient"
)
def local_cluster_client(
    num_workers: int = 8,
) -> Client:
    cluster = LocalCluster(
        name="localCluster", n_workers=num_workers, processes=True
    )

    client = Client(cluster)

    return client
