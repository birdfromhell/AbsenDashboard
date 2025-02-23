# Absen Dashboard

A school attendance management system built with Django. This system allows schools to manage student attendance, permissions, and generate reports.

## Features

- Multi-user roles (Admin, Teacher)
- School management
- Student management 
- Attendance tracking
- Permission/leave management
- Reporting and analytics
- Real-time attendance status
- Document upload support

## Prerequisites

- Python 3.8+
- pip
- virtualenv
- PostgreSQL/SQLite

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/ABSEN-DASHBOARD.git
cd ABSEN-DASHBOARD
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

3. Install required packages
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create .env file)
```bash
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## Required Libraries

```txt
asgiref==3.7.2
Django==4.2.7
django-appconf==1.0.5
django-compressor==4.4
django-cors-headers==4.3.1
django-rest-framework==0.1.0
django-sass-processor==1.2.2
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
drf-yasg==1.21.7
inflection==0.5.1
packaging==23.2
PyJWT==2.8.0
pytz==2023.3.post1
rcssmin==1.1.1
rjsmin==1.2.1
sqlparse==0.4.4
swagger-spec-validator==3.0.3
typing_extensions==4.8.0
uritemplate==4.1.1
```

## Project Structure

```
AbsenDashboard/
├── api/                    # REST API app
├── Dashboard/             # Main dashboard app
│   ├── management/       # Custom management commands
│   ├── migrations/      # Database migrations
│   ├── static/         # Static files
│   ├── templates/     # HTML templates
│   └── ...
├── static/              # Global static files
├── manage.py
└── requirements.txt
```

## API Documentation

API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## User Roles

1. Admin
- Manage schools
- Manage users
- View system-wide reports

2. Teacher
- Manage student attendance
- Handle permission requests
- View class/school reports

## License

This project is licensed under the MIT License - see the LICENSE file for details