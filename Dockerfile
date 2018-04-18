FROM fedora

RUN dnf install -y python3-pip
COPY requirements.txt README.md app.py main.py schemas.py /opt/
RUN pip3 install -r /opt/requirements.txt

CMD ["cd /opt"]
WORKDIR /opt
ENTRYPOINT ["python3"]
CMD ["main.py"]
