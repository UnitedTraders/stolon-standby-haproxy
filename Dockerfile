FROM haproxy:2.0

LABEL maintainer="Anton Markelov <a.markelov@unitedtraders.com>"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ARG STOLONCTL_VERSION=0.13.0

#install python, wget, supervisor
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  python3 \
  python3-dev \
  python3-pip \
  python3-setuptools \
  supervisor \
  wget && \
  apt-get -y clean && \
  rm -rf /var/lib/apt/lists/*

#install script requirements
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

#install stolonctl
ADD https://github.com/sorintlab/stolon/releases/download/v${STOLONCTL_VERSION}/stolon-v${STOLONCTL_VERSION}-linux-amd64.tar.gz /tmp/stolon.tar.gz
RUN tar zxvf /tmp/stolon.tar.gz -C /tmp && \
  mv /tmp/stolon-v${STOLONCTL_VERSION}-linux-amd64/bin/stolonctl /usr/bin/stolonctl && \
  chmod +x /usr/bin/stolonctl

COPY docker/config.yml /app/config.yml

COPY docker/haproxy.cfg /usr/local/etc/haproxy/config.cfg 
COPY docker/stolon_haproxy.j2 /app/stolon_haproxy.j2
RUN touch /usr/local/etc/haproxy/stolon-config.cfg

COPY docker/supervisord.conf /app/supervisord.conf

COPY src /app/src

EXPOSE 35432
CMD ["supervisord", "-c", "/app/supervisord.conf"]