FROM python:3.7

# copy files to leverage docker cache
COPY requirements.txt /app/

WORKDIR /app

# -----
# other installs

# -----

RUN pip install -r requirements.txt

COPY . /app

CMD ["python","app.py"]
