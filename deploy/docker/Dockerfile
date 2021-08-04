FROM python:3.8-alpine

LABEL MAINTAINER="Herman <actini@outlook.com>" VERSION="1.0.7"

WORKDIR /app

COPY --chown=1000:1000 . /app

RUN apk add --no-cache curl && pip install -r requirements.txt

USER 1000:1000

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s CMD curl -fs http://127.0.0.1:5000/health || exit 1

CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:5000", "manager:app"]