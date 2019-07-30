FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP src/app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src src
CMD ["flask", "run"]
