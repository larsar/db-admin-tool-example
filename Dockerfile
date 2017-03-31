FROM python:3-onbuild
RUN  apt-get update
RUN  apt-get install -y wget sudo
RUN  rm -rf /var/lib/apt/lists/* &&\
     wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh &&\
     heroku status

ENTRYPOINT [ "python", "example.py"]
