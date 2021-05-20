FROM python:3.9-slim-buster



COPY app app



RUN pip3 install flask flask-wtf email_validator requests flask-login flask-sqlalchemy

CMD ["python", "app/app.py"]