# TODO: move to a python:3.11.4-something image
## TODO: copy source files from host, instead of downloading
# TODO: remove postgresql, and move it to a separate container
# TODO: remove git
FROM debian:bookworm

RUN apt-get update && apt-get install -y python3.11-full python3.11-venv

ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv $VIRTUAL_ENV
RUN pip install --upgrade pip && pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

RUN pip install gunicorn python-dotenv # TODO: add these to requirements.txt

# RUN apt install procps

# COPY gunicorn-start.sh .

CMD ["/usr/bin/sh", "gunicorn-start.sh"]
# CMD ["python", "manage.py"]
# CMD ["/usr/bin/bash", "infinite_loop.sh"]

