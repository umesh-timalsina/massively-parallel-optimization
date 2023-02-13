from dask.distributed import Client, LocalCluster

from dask_jobqueue import SLURMCluster

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


@RegistersMPOConstruct(construct_name="runners", construct_key="ACCREClient")
def accre_client(
    num_workers=2,
    jobs=2,
    queue="debug",
    memory="8GB",
    cores=8,
    interface="em1"
):
    cluster = SLURMCluster(
        n_workers=num_workers,
        queue=queue,
        memory=memory,
        cores=cores,
        interface=interface 
    )   

    cluster.scale(jobs=jobs)

    client = Client(cluster)

    return client