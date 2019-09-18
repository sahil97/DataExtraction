# DataExtraction

#### Navigate to testingDocker folder and create a docker image by:

`docker build -t testingdocker:latest .`

#### check if images is showing up in:

`docker images`

#### After that run the docker image by:

`sudo docker run -p 5006:5006 -p 5005:5005 testingdocker:latest`

#### and open the browser with URL  

`http://localhost:5006`
