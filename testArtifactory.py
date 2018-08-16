from artifactory import ArtifactoryPath
path = ArtifactoryPath("https://na.artifactory.swg-devops.com/artifactory/txo-dswim-esb-deployment-generic-local/Train-0.3/")

path.mkdir()
path.deploy_file('box.py')
