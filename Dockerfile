# Use the official Python image as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY techcruncherapp/ /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Create directory for static files
RUN mkdir -p /techcruncherapp/technews/static/

# Command to run Gunicorn
CMD ["gunicorn", "techcruncherapp.wsgi:application", "--bind", "0.0.0.0:8000"]