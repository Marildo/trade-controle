FROM env-tdc:latest
LABEL authors="Marildo César"
WORKDIR /backend
COPY .. .

CMD sleep 5 && gunicorn --bind 0.0.0.0:7300 wsgi:flask_app --timeout 420 --log-level debug