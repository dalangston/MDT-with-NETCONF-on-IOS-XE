FROM ubuntu:24.04
RUN apt-get update && apt-get install -y \
    vim \
    wget

# install prometheus
RUN mkdir /opt/monitoring/
RUN wget -P /tmp/ https://github.com/prometheus/prometheus/releases/download/v2.53.4/prometheus-2.53.4.linux-amd64.tar.gz

RUN tar xvf /tmp/prometheus-2.53.4.linux-amd64.tar.gz --directory=/opt/monitoring/ --no-recursion
RUN mv /opt/monitoring/prometheus-2.53.4.linux-amd64/ /opt/monitoring/prometheus/
COPY ./prometheus-custom.yml /opt/monitoring/prometheus/
RUN chmod +x /opt/monitoring/prometheus/*

CMD ["/opt/monitoring/prometheus/prometheus", "--config.file=/opt/monitoring/prometheus/prometheus-custom.yml"]
