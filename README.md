# Smart Task Board

Smart Task Board built using Django and Django REST Framework.

## Tech Stack
* Python 3.8+ (Compatible with Django 4.2+)
* Django 4.2 LTS 
* Django REST Framework
* SQLite

## Setup Instructions

1. **Activate Virtual Environment and Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Start the Development Server**
```bash
python manage.py runserver

## UI Instructions
1. UI can be accessed at http://localhost:8000/
2. API endpoints are available at http://localhost:8000/api/
3. Swagger UI is available at http://localhost:8000/api/docs/
```

## API Documentation

Interactive API documentation is available via Swagger:
* Swagger UI: `/api/docs/`

