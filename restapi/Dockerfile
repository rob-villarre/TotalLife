FROM python:3.13  
 
RUN mkdir /app
 
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
RUN pip install --upgrade pip 
 
COPY requirements.txt  /app/
 
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . /app/
 
EXPOSE 8000

# TODO: add admin user?
# RUN python manage.py createsuperuser --username admin --email admin@example.com

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]