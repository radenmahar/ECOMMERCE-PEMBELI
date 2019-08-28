FROM python:3.6.8
MAINTAINER Your Name "panji@alterra.id"
RUN mkdir -p /DockerAPipembeli
COPY . /DockerAPipembeli
RUN pip install --upgrade pip        
RUN pip install -r /DockerAPipembeli/requirements.txt
WORKDIR /DockerAPipembeli
ENTRYPOINT ["python"]
CMD ["app.py"]
