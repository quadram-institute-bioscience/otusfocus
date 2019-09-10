FROM bioconductor/release_base2:latest

MAINTAINER nitesh.turaga@roswellpark.org

# This is to avoid the error
# 'debconf: unable to initialize frontend: Dialog'
ENV DEBIAN_FRONTEND noninteractive

ADD scripts /setup
# Add BiocVersion
RUN R -e "BiocManager::install(version='3.9')"
RUN Rscript /setup/install.R

# Init command for s6-overlay
CMD ["/init"]
