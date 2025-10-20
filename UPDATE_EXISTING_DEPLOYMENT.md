# Update Existing PythonAnywhere Deployment (Keep Database)

This guide will help you update your existing PythonAnywhere app with the new code while **keeping your existing database intact**.

## Step 1: Backup Your Current Database

**IMPORTANT: Always backup first!**

1. Open a Bash console on PythonAnywhere
2. Backup your database:
```bash
# Find your current app directory (adjust path if different)
cd ~/admin_portal  # or wherever your old app is

# Create backups folder
mkdir -p ~/backups

# Backup the database
cp instance/admin_portal_dev.db ~/backups/db_backup_$(date +%Y%m%d_%H%M%S).db

# Verify backup exists
ls -lh ~/backups/
```

## Step 2: Clone New Repository (Separate Location)

```bash
cd ~
# Clone to a NEW directory (don't overwrite yet)
git clone https://github.com/cakesmack/admin_centre.git admin_centre_new
cd admin_centre_new
```

## Step 3: Copy Your Database to New App

```bash
# Create instance folder in new app
mkdir -p ~/admin_centre_new/highland_admin_portal/instance

# Copy your existing database
cp ~/admin_portal/instance/admin_portal_dev.db ~/admin_centre_new/highland_admin_portal/instance/

# Verify it copied
ls -lh ~/admin_centre_new/highland_admin_portal/instance/
```

## Step 4: Update Database Schema (Run Migrations)

The new app has additional features (manager role, etc.) that need database updates:

```bash
cd ~/admin_centre_new/highland_admin_portal
workon admin_portal  # Use your existing virtualenv, or create new one

python3
```

In Python shell:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # This will add any new tables/columns without destroying existing data
    db.create_all()

    # Verify your existing users are still there
    users = User.query.all()
    print(f"Found {len(users)} existing users")
    for user in users:
        print(f"  - {user.username} ({user.email}) - Role: {user.role}")

    print("\nDatabase updated successfully!")

exit()
```

## Step 5: Update Dependencies (If Needed)

If you're using the same virtualenv:
```bash
workon admin_portal
cd ~/admin_centre_new
pip install -r requirements.txt
```

If creating a new virtualenv:
```bash
mkvirtualenv --python=/usr/bin/python3.10 admin_portal_new
pip install -r requirements.txt
```

## Step 6: Update WSGI Configuration

1. Go to the **Web** tab on PythonAnywhere
2. Click on your WSGI configuration file
3. Update the path to point to the new directory:

**Change this:**
```python
project_home = '/home/yourusername/admin_portal'  # OLD PATH
```

**To this:**
```python
project_home = '/home/yourusername/admin_centre_new/highland_admin_portal'  # NEW PATH
```

Complete WSGI file should look like:
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/admin_centre_new/highland_admin_portal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-super-secret-key-here'

# Import the Flask app
from app import create_app
application = create_app()
```

## Step 7: Update Static Files Path

In the **Web** tab, update the static files mapping:

**Change from:**
```
/static/ → /home/yourusername/admin_portal/app/static/
```

**To:**
```
/static/ → /home/yourusername/admin_centre_new/highland_admin_portal/app/static/
```

## Step 8: Update Virtual Environment Path (If Changed)

If you created a new virtualenv, update it in the **Web** tab under "Virtualenv":
- Old: `/home/yourusername/.virtualenvs/admin_portal`
- New: `/home/yourusername/.virtualenvs/admin_portal_new`

(Or keep the same if you reused the virtualenv)

## Step 9: Reload Web App

Click the big **Reload** button at the top of the Web tab.

## Step 10: Test Your App

1. Visit your app URL
2. Login with your **existing credentials** (your old admin account)
3. Check that your data is still there:
   - Customers
   - Callsheets
   - Forms
   - Any other existing data

## Step 11: Verify New Features

1. Check if you can access your profile without errors
2. Try creating a new user and see the 3 role options (Admin, Manager, Staff)
3. Check the new styling is applied
4. Verify the KB section works

## Step 12: Clean Up Old Directory (After Testing)

**ONLY DO THIS AFTER CONFIRMING EVERYTHING WORKS!**

```bash
# Rename old directory (don't delete yet, just in case)
cd ~
mv admin_portal admin_portal_OLD_BACKUP

# Rename new directory to the standard name (optional)
mv admin_centre_new admin_centre
```

If you renamed the directory, update WSGI file again:
```python
project_home = '/home/yourusername/admin_centre/highland_admin_portal'
```

And static files:
```
/static/ → /home/yourusername/admin_centre/highland_admin_portal/app/static/
```

Then reload again.

## Troubleshooting

### Missing Users or Data
- You didn't copy the database correctly
- Restore from backup: `cp ~/backups/db_backup_*.db ~/admin_centre_new/highland_admin_portal/instance/admin_portal_dev.db`

### Import Errors
- Check the WSGI file path is correct
- Verify virtualenv has all dependencies: `pip list`
- Check error log in Web tab

### Role Errors
- The new code expects roles to be 'admin', 'manager', or 'staff'
- Your old data might have different role names
- Update them in Python:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # If your old roles were named differently, update them:
    users = User.query.all()
    for user in users:
        if user.role not in ['admin', 'manager', 'staff']:
            print(f"User {user.username} has role: {user.role}")
            # Update as needed
            # user.role = 'admin'  # or 'manager' or 'staff'
    # db.session.commit()
```

### Static Files Not Loading
- Double-check the static files path in Web tab
- Make sure it points to: `/home/yourusername/admin_centre_new/highland_admin_portal/app/static/`

## Future Updates

After this initial migration, when you push updates to GitHub:

```bash
cd ~/admin_centre  # or admin_centre_new
git pull origin main
# Reload web app from Web tab
```

## Database Backups

Set up regular backups:
```bash
# Add to cron or run manually
cp ~/admin_centre/highland_admin_portal/instance/admin_portal_dev.db ~/backups/db_backup_$(date +%Y%m%d).db
```

## Summary

This approach:
- ✅ Keeps all your existing data
- ✅ Updates the code to the new version
- ✅ Adds new features (3-tier roles, styling, etc.)
- ✅ Maintains your existing users and credentials
- ✅ Keeps a backup of everything just in case
