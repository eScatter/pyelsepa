FROM debian:8
MAINTAINER Johan Hidding <j.hidding@esciencecenter.nl>

# fortran compiler
RUN apt-get update && apt-get install --no-install-recommends -y \
    gfortran

# unpack elsepa
COPY adus_v1_0.tar.gz /tmp
RUN tar xf /tmp/adus_v1_0.tar.gz -C opt

# compile
WORKDIR /opt/elsepa
RUN f77 -O3 elscata.f -o elscata && f77 -O3 elscatm.f -o elscatm

