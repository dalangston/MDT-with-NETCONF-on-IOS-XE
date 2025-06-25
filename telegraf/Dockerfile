FROM ubuntu:24.04
RUN apt-get update && apt-get install -y \
    vim \
    wget \
    python3 python3-pip \
    git

RUN mkdir /opt/monitoring/

# install telegraf
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf_1.34.1-1_amd64.deb
RUN dpkg -i telegraf_1.34.1-1_amd64.deb
RUN mkdir /opt/monitoring/telegraf/

# Clone ncclient fork from GitHub from CiscoDevNet
#RUN git clone https://github.com/CiscoDevNet/ncclient /opt/monitoring/telegraf/ncclient

# Install required packages for Python scripts
COPY requirements.txt .
RUN pip3 install -r requirements.txt  --break-system-packages
# copy NETCONF scripts/files and telegraf config file into the telegraf monitoring folder
COPY ./* /opt/monitoring/telegraf/
RUN chmod +x /opt/monitoring/telegraf/*

WORKDIR /opt/monitoring/telegraf
CMD ["telegraf", "--config", "/opt/monitoring/telegraf/telegraf.conf"]
