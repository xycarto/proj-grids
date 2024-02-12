FROM  ubuntu:22.04

ENV TZ Pacific/Auckland

RUN apt-get update
RUN apt-get install -y tzdata
RUN echo "Pacific/Auckland" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends gnupg ca-certificates software-properties-common dirmngr wget \
    curl git-core libssl-dev libssh2-1-dev libcurl4-openssl-dev libxml2-dev && \
    apt upgrade --yes && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python packages
RUN apt-get update && apt-get -y install python3-pip
RUN pip3 install geopandas pyproj





