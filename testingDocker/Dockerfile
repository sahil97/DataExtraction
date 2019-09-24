# this dockerfile is used for product deployments
FROM ubuntu:16.04

LABEL maintainer "Sahil Sharma <sahil.sharma071997@gmail.com>"

COPY flask/requirements.txt app/flask/requirements.txt
RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get update

# To solve add-apt-repository : command not found
RUN apt-get -y install software-properties-common

# Install OpenJDK-8
RUN apt-get update && \
   apt-get install -y openjdk-8-jdk && \
   apt-get install -y ant && \
   apt-get clean;
# Fix certificate issues
RUN apt-get update && \
   apt-get install ca-certificates-java && \
   apt-get clean && \
   update-ca-certificates -f;
# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["/sbin/my_init"]
# install python 3.6
RUN apt-get install python3
RUN apt-get update
RUN apt-get install curl
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python3 get-pip.py

RUN pip install -r app/flask/requirements.txt

COPY ./flask /app/flask
COPY ./web /app/web
WORKDIR /app

# for the flask config
ENV FLASK_ENV=prod

EXPOSE 5006
EXPOSE 5005
COPY startscript.sh startscript.sh
RUN ["chmod", "+x", "./startscript.sh"]
CMD ["./startscript.sh"]
