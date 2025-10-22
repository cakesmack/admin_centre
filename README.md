# Highland Admin Portal

A comprehensive admin portal for managing customers, orders, callsheets, inventory, and knowledge base for a catering supplies company.
<img width="1882" height="876" alt="image" src="https://github.com/user-attachments/assets/267cc6d7-2416-4711-ac64-68fc596cbcd3" />

## Features

- **User Management** - Multi-role user system (Admin, Manager, Staff)
- **Customer Management** - Track customers and their addresses
- **Callsheets** - Manage daily customer calls and order tracking
- **Standing Orders** - Automated recurring customer orders
- **Customer Stock** - Track customer inventory levels
- **Clearance Stock** - Manage clearance items and sales
- **Forms** - Generate delivery notes, returns forms, invoice corrections
- **Knowledge Base** - Internal documentation with article approval workflow
- **Reports & Analytics** - Comprehensive business analytics and reporting
- **Company Updates** - Internal communication and announcements

## User Roles

### Admin (Full Access)
- Complete access to all features
- User management
- Admin dashboard
- Reports & analytics
- KB article approvals

### Manager (Reports & Approvals)
- Access to reports & analytics
- KB article approvals
- All standard features
- No user management or admin dashboard access

### Staff (Standard Access)
- All operational features (callsheets, forms, customers, etc.)
- No admin sections or approvals

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd admin_centre
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create `.env` file):
```env
FLASK_APP=highland_admin_portal/run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

5. Initialize the database:
```bash
cd highland_admin_portal
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

6. Run the application:
```bash
python run.py
```

The app will be available at `http://localhost:5000`

### Default Login
- **Username:** admin
- **Password:** (set during first-time setup)

## PythonAnywhere Deployment

1. Upload files to PythonAnywhere
2. Create a virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.10 admin_portal
pip install -r requirements.txt
```

3. Configure WSGI file:
```python
import sys
path = '/home/yourusername/admin_centre/highland_admin_portal'
if path not in sys.path:
    sys.path.append(path)

from app import create_app
application = create_app()
```

4. Set up static files in web app configuration
5. Reload the web app

## Project Structure

```
admin_centre/
├── highland_admin_portal/
│   ├── app/
│   │   ├── blueprints/        # Route blueprints
│   │   ├── static/            # CSS, JS, images
│   │   ├── templates/         # HTML templates
│   │   ├── __init__.py        # App factory
│   │   ├── models.py          # Database models
│   │   ├── routes.py          # Main routes
│   │   └── forms.py           # WTForms
│   ├── instance/              # Database (gitignored)
│   ├── logs/                  # Application logs
│   └── run.py                 # Entry point
├── .gitignore
├── requirements.txt
└── README.md
```

## Database

Uses SQLite for development. The database file is stored in `highland_admin_portal/instance/admin_portal_dev.db` and is excluded from git.

## Documentation

- `ROLE_PERMISSIONS.md` - Detailed role permissions documentation
- `PROMOTIONAL_VIDEO_DATA.md` - Sample data for demos

## Contributing

This is a private project by Craig Mackenzie

## License

Proprietary - All rights reserved
