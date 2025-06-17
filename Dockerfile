FROM rocker/r-ver:4.4 AS build

COPY pyproject.toml install_pkgs.R ./

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
  Rscript install_pkgs.R

FROM rocker/r-ver:4.4

LABEL Maintainer="https://github.com/pacificclimate/quail" \
  Description="quail WPS" \
  Vendor="pacificclimate" \
  Version="0.7.1"

WORKDIR /tmp

# Copy R packages
ARG R_FILEPATH=/root/R/x86_64-pc-linux-gnu-library/4.4

COPY --from=build ${R_FILEPATH}/PCICt ${R_FILEPATH}/PCICt
COPY --from=build ${R_FILEPATH}/climdex.pcic ${R_FILEPATH}/climdex.pcic
COPY --from=build ${R_FILEPATH}/Rcpp ${R_FILEPATH}/Rcpp

# Add path to libR.so to the environment variable LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/usr/local/lib/R/lib:${LD_LIBRARY_PATH}"
ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

COPY . /tmp
COPY pyproject.toml poetry.lock* ./

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
  apt-get install -y --no-install-recommends python3 python3-pip curl  && \
  curl -sSL https://install.python-poetry.org | python3


RUN poetry config virtualenvs.in-project true && \
  poetry install

EXPOSE 5000
CMD ["poetry", "run", "gunicorn", "--bind=0.0.0.0:5000", "quail.wsgi:application"]


