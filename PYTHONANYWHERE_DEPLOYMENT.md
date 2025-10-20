# PythonAnywhere Deployment Guide

## Step 1: Clone Repository on PythonAnywhere

1. Open a Bash console on PythonAnywhere
2. Clone your repository:
```bash
cd ~
git clone https://github.com/cakesmack/admin_centre.git
cd admin_centre
```

## Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 admin_portal

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Initialize Database

```bash
cd highland_admin_portal
python3
```

In Python shell:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()

    # Create admin user
    admin = User(
        username='admin',
        email='admin@highlandhygiene.com',
        full_name='Admin User',
        role='admin',
        job_title='System Administrator',
        is_active=True
    )
    admin.set_password('YourSecurePassword123!')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")

exit()
```

## Step 4: Configure Web App

1. Go to the **Web** tab on PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration** (NOT Flask)
4. Select **Python 3.10**

## Step 5: Configure WSGI File

Click on the WSGI configuration file link and replace its contents with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/admin_centre/highland_admin_portal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-super-secret-key-change-this-in-production'

# Import the Flask app
from app import create_app
application = create_app()
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

## Step 6: Configure Static Files

In the **Web** tab, add these static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/admin_centre/highland_admin_portal/app/static/` |

## Step 7: Configure Virtual Environment

In the **Web** tab, under "Virtualenv":
- Enter: `/home/yourusername/.virtualenvs/admin_portal`

## Step 8: Reload Web App

Click the **Reload** button at the top of the Web tab.

Your app should now be live at: `https://yourusername.pythonanywhere.com`

## Step 9: Test Login

1. Visit your app URL
2. Login with:
   - Username: `admin`
   - Password: (the one you set in Step 3)

## Updating the App (Pull New Changes)

When you make changes and push to GitHub:

1. Open Bash console on PythonAnywhere:
```bash
cd ~/admin_centre
git pull origin main
```

2. If you made changes to dependencies:
```bash
workon admin_portal
pip install -r requirements.txt
```

3. If you made database changes:
```bash
cd highland_admin_portal
python3
```
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()  # Creates new tables if any
exit()
```

4. Reload web app from the Web tab

## Populate Sample Data (Optional for Testing)

```bash
cd ~/admin_centre
workon admin_portal
python populate_dummy_data.py
```

This will populate the database with sample customers, articles, etc. for testing.

## Troubleshooting

### Error Logs
- Check error logs in the **Web** tab under "Log files"
- Look for the error log link (usually `/var/log/yourusername.pythonanywhere.com.error.log`)

### Database Issues
- Make sure the `instance` folder exists: `mkdir -p highland_admin_portal/instance`
- Check database permissions: `ls -la highland_admin_portal/instance/`

### Import Errors
- Verify virtual environment is activated: `workon admin_portal`
- Check all dependencies are installed: `pip list`
- Make sure paths in WSGI file are correct

### Static Files Not Loading
- Double-check static file mappings in Web tab
- Verify the path exists: `ls -la ~/admin_centre/highland_admin_portal/app/static/`

## Security Notes for Production

1. **Change the SECRET_KEY** in the WSGI file to a strong random string
2. **Change the admin password** immediately after first login
3. **Don't commit** the database file to git (already in .gitignore)
4. Consider setting up **HTTPS** (PythonAnywhere provides this free)
5. Regularly **backup** your database:
   ```bash
   cp ~/admin_centre/highland_admin_portal/instance/admin_portal_dev.db ~/backups/db_backup_$(date +%Y%m%d).db
   ```

## Support

For PythonAnywhere specific issues, check:
- [PythonAnywhere Help Pages](https://help.pythonanywhere.com/)
- [PythonAnywhere Forums](https://www.pythonanywhere.com/forums/)
