# vim:set ft=dockerfile:
FROM r-base:4.0.3
MAINTAINER https://github.com/pacificclimate/chickadee
LABEL Description="quail WPS" Vendor="pacificclimate" Version="0.1.0"

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

# Update system
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    python3.8 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    python3-venv

COPY . /opt/wps

WORKDIR /opt/wps

# Install WPS
RUN pip3 install -e .

# Start WPS service on port 5005 on 0.0.0.0
EXPOSE 5005
ENTRYPOINT ["sh", "-c"]
CMD ["exec quail start -b 0.0.0.0"]

# docker build -t pcic/quail .
# docker run -p 5005:5005 pcic/quail
# http://localhost:5005/wps?request=GetCapabilities&service=WPS
# http://localhost:5005/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
