FROM rocker/r-ver:4.0.3 AS build

COPY r_requirements.txt install_pkgs.R ./

# Install python and R packages
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
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
  Rscript install_pkgs.R r_requirements.txt

FROM rocker/r-ver:4.0.3

LABEL Maintainer="https://github.com/pacificclimate/quail" \
  Description="quail WPS" \
  Vendor="pacificclimate" \
  Version="0.7.1"

WORKDIR /tmp

# Copy R packages
ARG R_FILEPATH=/root/R/x86_64-pc-linux-gnu-library/4.0

COPY --from=build ${R_FILEPATH}/PCICt ${R_FILEPATH}/PCICt
COPY --from=build ${R_FILEPATH}/climdex.pcic ${R_FILEPATH}/climdex.pcic
COPY --from=build ${R_FILEPATH}/Rcpp ${R_FILEPATH}/Rcpp

# Add path to libR.so to the environment variable LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/lib/R/lib:$LD_LIBRARY_PATH
ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

COPY . /tmp
COPY requirements.txt ./

# Install Python
RUN apt-get update && \
  apt-get install -y --no-install-recommends python3.8 python3-pip && \
  pip install -U pip && \
  pip install -r requirements.txt && \
  pip install gunicorn

EXPOSE 5000
CMD gunicorn --bind=0.0.0.0:5000 quail.wsgi:application
