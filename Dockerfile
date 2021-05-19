FROM python:3.9-slim-buster
WORKDIR /app
RUN pip3 install flask flask-wtf email_validator requests flask-login flask-sqlalchemy
CMD ["python3", "app.py"]
