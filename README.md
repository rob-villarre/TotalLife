# Total Life

Built with Django REST API backend and Next.js frontend, fully containerized with Docker.

## Project Structure
- `/restapi` - Django REST API backend
- `/web` - Next.js frontend application

## Prerequisites

- Docker (v20.10.0 or higher)
- Docker Compose (v2 or higher)
- Git

## Quick Start Guide

### 1. Backend Setup (Django REST API)

Navigate to the backend directory:
```bash
cd restapi
```

Start the backend services:
```bash
docker-compose up -d
```

Apply database migrations:
```bash
docker-compose exec restapi python manage.py makemigrations
docker-compose exec restapi python manage.py migrate
```

Load initial data (optional):
```bash
# Load fixtures if available
docker-compose exec restapi python manage.py loaddata initial_data.json

# Create a superuser for admin access
docker-compose exec restapi python manage.py createsuperuser
```

Run tests
```bash
# Load fixtures if available
docker-compose exec restapi python manage.py test
```

The backend API will be available at: http://localhost:8000/api/
Admin interface: http://localhost:8000/admin/

### 2. Frontend Setup (Next.js)

In a new terminal, navigate to the frontend directory:
```bash
cd web
```

Start the frontend services:
```bash
docker-compose up -d
```

The frontend application will be available at: http://localhost:3000

## Environment Variables

For the backend (in /restapi/.env):

SECRET_KEY='django-insecure-md=m=_ua2p==bk5*h-05c6=)hlb(dr+&+)fngtnw1zfpvf31z+'
DEBUG=True
DJANGO_ALLOWED_HOSTS=[]

For the frontend (in /web/.env.local):

NEXT_PUBLIC_RESTAPI_APPOINTMENT_URL=http://localhost:8000/api/appointments/
NEXT_PUBLIC_RESTAPI_PATIENT_URL=http://localhost:8000/api/patients/
NEXT_PUBLIC_RESTAPI_CLINICIAN_URL=http://localhost:8000/api/clinicians/