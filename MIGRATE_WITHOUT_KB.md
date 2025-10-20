# Migrate Existing App to New Version (Add KB Features)

This guide is for migrating your existing PythonAnywhere app that **does NOT have KB tables** to the new version that includes the integrated Knowledge Base.

## Important Notes

- Your existing database does NOT have KB tables (Article, Category, Supplier, etc.)
- The new app has KB fully integrated
- We'll keep your existing data (Users, Customers, Callsheets, Forms, etc.)
- We'll add the new KB tables to your database

## Step 1: Backup Your Current Database

**CRITICAL: Always backup first!**

```bash
# SSH into PythonAnywhere
cd ~/admin_portal  # or wherever your current app is

# Create backups folder
mkdir -p ~/backups

# Backup the database
cp instance/admin_portal_dev.db ~/backups/db_backup_$(date +%Y%m%d_%H%M%S).db

# Verify backup
ls -lh ~/backups/
```

## Step 2: Clone New Repository

```bash
cd ~
# Clone to a NEW directory
git clone https://github.com/cakesmack/admin_centre.git
cd admin_centre
```

## Step 3: Set Up Virtual Environment

```bash
# Create new virtualenv for the new app
mkvirtualenv --python=/usr/bin/python3.10 admin_centre_env

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Copy Your Existing Database

```bash
# Create instance folder
mkdir -p ~/admin_centre/highland_admin_portal/instance

# Copy your existing database
cp ~/admin_portal/instance/admin_portal_dev.db ~/admin_centre/highland_admin_portal/instance/

# Verify
ls -lh ~/admin_centre/highland_admin_portal/instance/
```

## Step 5: Add KB Tables to Your Database

This is the key step - we'll add the NEW KB tables without touching your existing data:

```bash
cd ~/admin_centre/highland_admin_portal
workon admin_centre_env

python3
```

In Python shell:
```python
from app import create_app, db
from app.models import User, Customer, Article, Category, Supplier

app = create_app()
with app.app_context():
    # This adds NEW tables (KB tables) without touching existing ones
    db.create_all()

    # Verify your existing data is intact
    print("\n=== EXISTING DATA CHECK ===")
    users = User.query.all()
    print(f"✓ Users: {len(users)}")
    for user in users:
        print(f"  - {user.username} ({user.email})")

    customers = Customer.query.all()
    print(f"✓ Customers: {len(customers)}")

    # Verify NEW KB tables were created
    print("\n=== NEW KB TABLES ===")
    articles = Article.query.all()
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    print(f"✓ Articles table created: {len(articles)} articles")
    print(f"✓ Categories table created: {len(categories)} categories")
    print(f"✓ Suppliers table created: {len(suppliers)} suppliers")

    print("\n✅ Database migration successful!")
    print("Your existing data is safe, and new KB tables are ready!")

exit()
```

## Step 6: Update WSGI Configuration

1. Go to the **Web** tab on PythonAnywhere
2. Click on your WSGI configuration file
3. **Replace the entire contents** with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/admin_centre/highland_admin_portal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-super-secret-production-key-change-this'

# Import the Flask app
from app import create_app
application = create_app()
```

**Replace `yourusername` with your actual PythonAnywhere username!**

## Step 7: Update Static Files Path

In the **Web** tab, update static files mapping:

**URL:** `/static/`
**Directory:** `/home/yourusername/admin_centre/highland_admin_portal/app/static/`

## Step 8: Update Virtual Environment Path

In the **Web** tab, under "Virtualenv", enter:
```
/home/yourusername/.virtualenvs/admin_centre_env
```

## Step 9: Reload Web App

Click the big **Reload** button at the top of the Web tab.

## Step 10: Test Your App

1. **Test existing features:**
   - Login with your existing credentials ✓
   - Check Customers page ✓
   - Check Callsheets ✓
   - Check Forms ✓
   - All your existing data should be there!

2. **Test NEW features:**
   - Navigate to Knowledge Base section (new menu item)
   - You should see an empty KB (no articles yet)
   - Try creating a new article
   - Check the new 3-tier role system when creating users

3. **Test styling:**
   - New cleaner, lighter color scheme should be visible
   - Navigation should look the same but content area is lighter

## Step 11: Verify User Roles

Your existing users might need role updates:

```bash
cd ~/admin_centre/highland_admin_portal
workon admin_centre_env
python3
```

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print("\nCurrent user roles:")
    for user in users:
        print(f"  {user.username}: {user.role}")

    # If any users have old role names or need updating:
    # Example: Update a user to manager
    # user = User.query.filter_by(username='someuser').first()
    # user.role = 'manager'  # Options: 'admin', 'manager', 'staff'
    # db.session.commit()

    print("\nValid roles are: admin, manager, staff")

exit()
```

## Step 12: Clean Up (After Everything Works!)

**ONLY after confirming everything works for a few days:**

```bash
# Rename old directory (keep as backup for now)
cd ~
mv admin_portal admin_portal_OLD_BACKUP

# Keep this backup for at least a week before deleting
```

## What Changed in the Database?

### Existing Tables (Untouched):
- ✓ User
- ✓ Customer
- ✓ CustomerAddress
- ✓ Product
- ✓ Callsheet
- ✓ CallsheetEntry
- ✓ Form
- ✓ StandingOrder
- ✓ StandingOrderItem
- ✓ CustomerStock
- ✓ StockTransaction
- ✓ CompanyUpdate
- ✓ TodoItem
- ✓ ClearanceStock

### NEW Tables Added:
- ✨ Article (KB articles)
- ✨ Category (KB categories)
- ✨ Supplier (KB suppliers)
- ✨ ArticleView (tracks article views)

## Troubleshooting

### "Table already exists" error
- This means some KB tables already exist somehow
- Safe to ignore - `db.create_all()` won't overwrite them

### Can't see existing data
- Database didn't copy correctly
- Restore from backup: `cp ~/backups/db_backup_*.db ~/admin_centre/highland_admin_portal/instance/admin_portal_dev.db`
- Run Step 5 again

### Import errors
- Check WSGI file path is correct
- Verify virtualenv is activated: `workon admin_centre_env`
- Check dependencies: `pip list`

### Static files not loading
- Check static files path in Web tab
- Make sure path is: `/home/yourusername/admin_centre/highland_admin_portal/app/static/`

### Profile page error
- This was fixed in the new code
- Make sure you reloaded the web app

## Future Updates

When you push updates to GitHub:

```bash
cd ~/admin_centre
git pull origin main
# Reload web app from Web tab
```

## Regular Backups

Create a backup script:
```bash
#!/bin/bash
# Save as ~/backup_db.sh
cp ~/admin_centre/highland_admin_portal/instance/admin_portal_dev.db ~/backups/db_backup_$(date +%Y%m%d).db
echo "Backup created!"
```

Run weekly: `bash ~/backup_db.sh`

## Summary

This migration:
- ✅ Keeps ALL your existing data (users, customers, forms, etc.)
- ✅ Adds NEW KB functionality (articles, categories, suppliers)
- ✅ Updates the code (roles, styling, bug fixes)
- ✅ Maintains your login credentials
- ✅ Safe process with backups

Your app will have everything it had before PLUS the new Knowledge Base feature!
