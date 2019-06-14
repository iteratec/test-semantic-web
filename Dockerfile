FROM continuumio/anaconda3

LABEL vendor="iteratec GmbH" 
LABEL maintainer="Danny Lade <danny.lade@iteratec.com>"

COPY environment.yml /

RUN apt-get update \
 && apt-get install -y procps \
 && apt autoclean

RUN conda update --yes --name base --channel defaults conda \
 && conda env update --name=base --file=/environment.yml

CMD "/bin/bash"
