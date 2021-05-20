FROM rocker/r-ver:4.0.3 AS builder

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

COPY requirements.txt r_requirements.txt install_pkgs.R ./

# Install python and R packages
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    # Install pip
    python3-pip \
    # Install libraries for R packages installation
    libssl-dev \
    libxml2-dev \
    libudunits2-dev \
    libnetcdf-dev \
    libgit2-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libcurl4-openssl-dev && \
    # Install R packages
    Rscript install_pkgs.R r_requirements.txt && \
    # Install python packages
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt --ignore-installed --user && \
    # Install gunicorn
    pip3 install gunicorn --user


# vim:set ft=dockerfile:
FROM rocker/r-ver:4.0.3 AS prod
MAINTAINER https://github.com/pacificclimate/quail
LABEL Description="quail WPS" Vendor="pacificclimate" Version="0.7.0"

# Install Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3.8 \
      python3-pip

# COPY Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy R packages in r_requirements.txt and their dependencies
# Directories cannot be recursively copied
COPY --from=builder /root/R/x86_64-pc-linux-gnu-library/4.0/PCICt \
  /root/R/x86_64-pc-linux-gnu-library/4.0/PCICt
COPY --from=builder /root/R/x86_64-pc-linux-gnu-library/4.0/climdex.pcic \
  /root/R/x86_64-pc-linux-gnu-library/4.0/climdex.pcic
COPY --from=builder /root/R/x86_64-pc-linux-gnu-library/4.0/Rcpp \
  /root/R/x86_64-pc-linux-gnu-library/4.0/Rcpp

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH
# Add path to libR.so to the environment variable LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/lib/R/lib:$LD_LIBRARY_PATH

WORKDIR /code

COPY ./quail /code/quail

EXPOSE 5000

CMD gunicorn --bind=0.0.0.0:5000 quail.wsgi:application

# docker build -t pcic/quail .
# docker run -p 5000:5000 pcic/quail
# http://localhost:5000/wps?request=GetCapabilities&service=WPS
# http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
