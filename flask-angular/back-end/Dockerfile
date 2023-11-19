FROM env-tdc:latest
LABEL authors="Marildo César"
WORKDIR /backend
COPY .. .

CMD gunicorn --bind 0.0.0.0:7300 wsgi:flask_app --log-level debug