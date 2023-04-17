FROM python

WORKDIR /mbk

COPY requirements.txt /mbk

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . /mbk

EXPOSE 5000

CMD ["python", "manage.py"]