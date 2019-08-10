FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get -y update && apt-get install -y \
    curl \
	lsb-release \
    wget \
    git \
    gcc \
    build-essential \
    libqt5gui5 \
	apt-transport-https \
    python3

RUN pip install --upgrade -q pip

RUN pip install 'urllib3<1.24,>=1.21.1'

RUN pip install camoco

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]