from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
import sys
sys.path.insert(0, '/home/linux_dev_env/data-engineering-zoomcamp/week_2_workflow_orchestration/flows/03_deployment')

from _2_5_parameterized_flow import etl_parent_flow
docker_block = DockerContainer.load("docker-container")

docker_dep = Deployment.build_from_flow(

    flow = etl_parent_flow,
    name='docker-flow',
    infrastructure=docker_block

)

if __name__=="__main__":
    docker_dep.apply()
