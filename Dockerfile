FROM 711226717742.dkr.ecr.us-east-1.amazonaws.com/qat-base-image:latest
MAINTAINER apaul@transparent.com

RUN apt-get update

RUN apt-get install -y bzip2 \
    zlib1g-dev libopenjpeg-dev libjpeg-dev libcurl4-openssl-dev

ADD requirements-cpython.txt /opt/requirements-cpython.txt

RUN opt/v/bin/pip install -U -r /opt/requirements-cpython.txt && \
    rm /opt/requirements-cpython.txt

# change this add based on project #
ADD artifact_cleanup.py /opt/artifact_cleanup.py
EXPOSE 8000
WORKDIR /opt

CMD ["/opt/v/bin/python", "artifact_cleanup.py"]