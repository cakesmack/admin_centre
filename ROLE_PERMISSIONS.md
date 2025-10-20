# Role-Based Permissions Summary

## User Roles

The application now supports three distinct user roles with different access levels:

### 1. **Admin** (Full Access)
- Has complete access to all features
- Can access the Admin Dashboard
- Can manage users (create, edit, delete)
- Can approve/reject KB articles
- Can access Reports & Analytics
- Full CRUD operations on all resources

### 2. **Manager** (Limited Admin Access)
- **CAN ACCESS:**
  - Reports & Analytics page
  - KB Article approvals
  - All standard user features (forms, callsheets, stock, etc.)

- **CANNOT ACCESS:**
  - Admin Dashboard
  - User Management

### 3. **Staff** (Sales Staff - Standard Access)
- **CAN ACCESS:**
  - All standard features (forms, callsheets, customers, stock, etc.)
  - KB Articles (view, create, edit own articles)
  - Company updates
  - Todo lists
  - Standing orders

- **CANNOT ACCESS:**
  - Admin Dashboard
  - User Management
  - Reports & Analytics
  - KB Article approvals

## Implementation Details

### Helper Methods Added to User Model

The following methods were added to the `User` model in `app/models.py`:

```python
def is_admin(self):
    """Check if user is an admin"""
    return self.role == 'admin'

def is_manager(self):
    """Check if user is a manager"""
    return self.role == 'manager'

def is_staff(self):
    """Check if user is staff (sales staff)"""
    return self.role == 'staff'

def can_access_admin_dashboard(self):
    """Only admins can access the admin dashboard"""
    return self.role == 'admin'

def can_access_reports(self):
    """Admins and managers can access reports"""
    return self.role in ['admin', 'manager']

def can_approve_kb_articles(self):
    """Only admins and managers can approve KB articles"""
    return self.role in ['admin', 'manager']

def can_manage_users(self):
    """Only admins can manage users"""
    return self.role == 'admin'
```

### Files Modified

1. **app/models.py**
   - Added role checking helper methods

2. **app/templates/base.html**
   - Updated navigation to show/hide sections based on permissions
   - Admin Dashboard: Only visible to admins
   - User Management: Only visible to admins
   - Reports & Analytics: Visible to admins and managers

3. **app/blueprints/kb_articles.py**
   - Updated `/admin/approvals` route to allow both admin and manager roles
   - Updated dashboard to use `can_approve_kb_articles()` method

4. **app/blueprints/admin.py**
   - Created new `reports_access_required` decorator for manager access
   - Updated all report API routes to use the new decorator:
     - `/api/reports/summary`
     - `/api/reports/daily-activity`
     - `/api/reports/user-activity`
     - `/api/reports/inactive-customers`
     - `/api/reports/callsheet-analytics`
     - `/api/reports/additional-analytics`
     - `/api/reports/call-history-analytics`
     - `/api/reports/problem-customers`
     - `/api/reports/sales-rep-needed`
     - `/api/reports/returns-analytics`
   - Admin dashboard and import routes remain admin-only

## Navigation Visibility Matrix

| Section | Admin | Manager | Staff |
|---------|-------|---------|-------|
| Dashboard | ✓ | ✓ | ✓ |
| Customers | ✓ | ✓ | ✓ |
| Forms | ✓ | ✓ | ✓ |
| Callsheets | ✓ | ✓ | ✓ |
| Standing Orders | ✓ | ✓ | ✓ |
| Customer Stock | ✓ | ✓ | ✓ |
| Clearance Stock | ✓ | ✓ | ✓ |
| Knowledge Base | ✓ | ✓ | ✓ |
| Tools | ✓ | ✓ | ✓ |
| **Admin Dashboard** | ✓ | ✗ | ✗ |
| **User Management** | ✓ | ✗ | ✗ |
| **Reports & Analytics** | ✓ | ✓ | ✗ |
| **KB Approvals** | ✓ | ✓ | ✗ |

## Creating New Manager/Staff Users

When creating users in the admin panel, set the role field to:
- `admin` - For full admin access
- `manager` - For limited admin access (reports + KB approvals)
- `staff` - For standard sales staff access

## Testing the Permissions

1. **As Admin**: You should see all menu items including Admin Dashboard and User Management
2. **As Manager**: You should see Reports & Analytics but NOT Admin Dashboard or User Management
3. **As Staff**: You should NOT see any Admin section items

## Security Notes

- All permission checks are enforced at both the template level (UI) and route level (backend)
- Direct URL access to restricted pages will redirect to dashboard with an error message
- The decorators ensure that even if someone tries to access a URL directly, they'll be blocked
