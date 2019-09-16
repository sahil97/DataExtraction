# DataExtraction

#### Navigate to testingDocker folder and create a docker image by:

`docker build -t testingdocker:latest .`

#### check if images is showing up in:

`docker images`

#### After that run the docker image by:

`docker run -p 5005:5005 testingdocker:latest`

#### On another terminal, traverse to WebApp/webpage folder and run command
`python3 -m http.server` note the port : ( most probably 8000 ) and open the browser with URL  

`http://localhost:{port}`
