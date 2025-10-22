# Setup Guide for Employers/Reviewers

This guide will help you quickly set up and run the Highland Catering Supplies Admin Portal for review purposes.

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Edge, or Safari)
- 5-10 minutes of setup time

---

## Quick Start (5 Minutes)

### Step 1: Clone or Extract the Project
```bash
# If using git
git clone [repository-url]
cd admin_centre

# Or simply extract the ZIP file and navigate to the folder
cd admin_centre
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Secret Key
```bash
cd highland_admin_portal
python generate_secret_key.py
```
This creates a `.env` file with a secure SECRET_KEY

### Step 5: Initialize Database with Sample Data
```bash
# Create database and populate with demo data
python init_db.py
```

**Default Admin Credentials Created:**
- Username: `admin`
- Password: `admin123`

**Additional Demo Users:**
- Manager: `manager` / `manager123`
- Staff: `staff` / `staff123`

### Step 6: Run the Application
```bash
python run.py
```

The application will start at: `http://127.0.0.1:5000`

---

## Exploring the Application

### Recommended Review Path

1. **Login as Admin** (`admin` / `admin123`)
   - View the main dashboard
   - Check out the Knowledge Base articles
   - Explore Company Updates

2. **Customer Management**
   - Navigate to "Customer Directory" (in the sidebar, click Tools → Customer Directory)
   - View existing customers
   - Try adding a new customer with multiple addresses

3. **Call Sheets**
   - Go to "Call Sheets" in the sidebar
   - Explore different days (Monday, Tuesday, etc.)
   - Try changing a customer's call status
   - Add a customer to a callsheet

4. **Standing Orders**
   - Navigate to "Standing Orders"
   - View existing recurring orders
   - Check the Schedule View
   - Explore order details

5. **Forms**
   - Go to "Forms" section
   - Try creating a Returns form
   - Check out different form types

6. **Knowledge Base**
   - Navigate to "KB Home"
   - Browse articles by category
   - Search for articles
   - Try creating a new article (requires login as staff/admin)

7. **Admin Features** (Admin only)
   - Go to "Admin Dashboard"
   - View "Reports & Analytics"
   - Check "User Management"

8. **Test Different Roles**
   - Logout and login as Manager or Staff
   - Notice the different menu options based on role

---

## Sample Data Included

The database initialization script creates:
- ✅ 3 user accounts (Admin, Manager, Staff)
- ✅ 15 sample customers with addresses
- ✅ 5 callsheets across different days
- ✅ 8 standing orders with products
- ✅ 10+ knowledge base articles
- ✅ Sample company updates
- ✅ Customer stock records
- ✅ Clearance stock items
- ✅ Form submissions

---

## Key Features to Review

### 1. Responsive Design
- **Test on mobile**: Press F12 in your browser, click the device toggle (Ctrl+Shift+M), and resize to 375px width
- Notice the hamburger menu appears on mobile
- All tables become scrollable
- Buttons stack vertically

### 2. Security
- Role-based access control (try logging in as different users)
- Secure password hashing
- CSRF protection on forms
- Session management

### 3. User Experience
- Drag-and-drop ordering in callsheets
- Auto-complete customer search
- Rich text editor in Knowledge Base
- Toast notifications for actions
- Color-coded status indicators

### 4. Data Management
- Multi-address customer support
- Complex form generation
- Inventory tracking
- Recurring order automation

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: "SECRET_KEY not found"
**Solution**: Run the secret key generator
```bash
python generate_secret_key.py
```

### Issue: Database locked or permission errors
**Solution**: Delete the database and reinitialize
```bash
rm instance/admin_portal_dev.db  # Mac/Linux
del instance\admin_portal_dev.db  # Windows
python init_db.py
```

### Issue: Port 5000 already in use
**Solution**: Either close the application using port 5000, or modify `run.py` to use a different port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## Testing Checklist for Reviewers

- [ ] Application starts without errors
- [ ] Can login with admin credentials
- [ ] Dashboard loads with data
- [ ] Can create a new customer
- [ ] Callsheets display and update
- [ ] Forms can be generated
- [ ] Knowledge Base articles are searchable
- [ ] Mobile view works (hamburger menu appears)
- [ ] Different user roles show different menus
- [ ] Reports and analytics display charts

---

## Production Deployment Notes

This application is designed to be production-ready with:
- Environment-based configuration (dev/staging/production)
- Secure cookie handling
- CSRF protection
- SQL injection prevention
- XSS protection via Jinja2 auto-escaping
- Secure password hashing

For production deployment:
1. Set `FLASK_ENV=production` in `.env`
2. Use PostgreSQL or MySQL instead of SQLite
3. Set `SESSION_COOKIE_SECURE=true` (requires HTTPS)
4. Configure proper logging
5. Set up automated backups
6. Use a production WSGI server (Gunicorn, uWSGI)

---

## Technical Architecture

### Backend Stack
- **Framework**: Flask 2.3+
- **ORM**: SQLAlchemy
- **Auth**: Flask-Login
- **Forms**: WTForms
- **Database**: SQLite (dev), PostgreSQL/MySQL compatible

### Frontend Stack
- **Framework**: Bootstrap 5.3
- **JavaScript**: Vanilla ES6+
- **Rich Text**: Quill.js
- **Charts**: Chart.js
- **UI Components**: Select2, SortableJS

### Code Organization
- **Blueprints**: Modular route organization
- **Application Factory**: Scalable app structure
- **Environment Config**: Separate dev/prod settings
- **Database Migrations**: Flask-Migrate support

---

## Questions or Feedback?

For questions about the application or technical implementation details, please contact:

**[Your Name]**
- Email: [your-email]
- LinkedIn: [your-linkedin]
- GitHub: [your-github]

Thank you for reviewing this project!
