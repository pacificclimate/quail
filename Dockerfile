# vim:set ft=dockerfile:
FROM r-base:4.0.3
MAINTAINER https://github.com/pacificclimate/quail
LABEL Description="quail WPS" Vendor="pacificclimate" Version="0.1.0"

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

WORKDIR /code

COPY requirements.txt r_requirements.txt install_pkgs.R ./

# Update system
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libgit2-dev \
    libpq-dev \
    python3.8 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    libxml2-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libssl-dev \
    libcurl4-openssl-dev && \
  pip3 install --upgrade pip && \
  pip3 install -r requirements.txt --ignore-installed && \
  pip3 install gunicorn && \
  Rscript install_pkgs.R r_requirements.txt

COPY . .

EXPOSE 5005

CMD gunicorn --bind=0.0.0.0:5005 quail.wsgi:application

# docker build -t pcic/quail .
# docker run -p 5005:5005 pcic/quail
# http://localhost:5005/wps?request=GetCapabilities&service=WPS
# http://localhost:5005/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
