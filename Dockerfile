FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   gcc \
	   curl \
	   zlib1g-dev \
	   libjpeg-dev \
	   libpng-dev \
	   libfreetype6-dev \
	   liblcms2-dev \
	   libwebp-dev \
	   libopenjp2-7-dev \
	   libtiff5-dev \
	   tk-dev \
	   tcl-dev \
	   pkg-config \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN mkdir -p /app/staticfiles /app/media
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "teatro_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
