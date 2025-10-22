# Highland Catering Supplies - Admin Portal
## Full-Stack Business Management System

> A comprehensive enterprise web application built with Flask, SQLAlchemy, and Bootstrap 5 for managing daily operations of a catering supplies company.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technical Stack](#technical-stack)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

**Highland Catering Supplies Admin Portal** is a production-ready business management system designed to streamline operations for a catering supplies company. The application handles customer relationship management, order processing, inventory tracking, and internal knowledge sharing.

### Business Problem Solved
- **Manual Order Tracking**: Replaced paper-based callsheets with digital tracking system
- **Inventory Management**: Real-time customer stock monitoring and alerts
- **Knowledge Silos**: Centralized knowledge base for staff training and procedures
- **Reporting Gaps**: Comprehensive analytics dashboards for business intelligence

### Development Stats
- **Lines of Code**: ~15,000+
- **Templates**: 41 HTML templates
- **Database Tables**: 20+ tables with relationships
- **API Endpoints**: 50+ RESTful routes
- **User Roles**: 3-tier permission system

---

## ✨ Key Features

### 1. Customer Relationship Management
- Multi-address customer profiles
- Contact history tracking
- Account status management
- Customer notes and preferences

### 2. Call Sheets System
- Daily call scheduling and tracking
- Real-time status updates (Ordered, Declined, No Answer)
- Drag-and-drop ordering
- Historical call data and analytics
- Seasonal customer pause/resume functionality

### 3. Standing Orders Management
- Recurring order automation
- Weekly delivery schedules
- Order generation with calendar view
- Pause/resume/end order controls
- PDF generation for delivery notes

### 4. Inventory Management
- **Customer Stock**: Track stock held for customers
- **Clearance Stock**: Manage sales and promotions
- Transaction history and audit trails
- Low stock alerts
- Stock movement tracking

### 5. Forms & Documentation
- Returns forms with product lookup
- Invoice corrections
- Customer's own stock forms
- Print-ready PDF layouts
- Form submission history

### 6. Knowledge Base
- Rich text article editor (Quill.js)
- Category and supplier organization
- Article approval workflow
- Image uploads
- View count tracking
- Search functionality

### 7. Company Updates & Communication
- Rich text announcements
- Priority levels (Normal, Important, Urgent)
- Event scheduling
- Pin/sticky posts
- Category organization

### 8. Reports & Analytics
- Callsheet performance metrics
- Form submission statistics
- User activity tracking
- Weekly trends analysis
- Customizable date ranges
- Interactive charts (Chart.js)

### 9. User Management
- Role-based access control (Admin, Manager, Staff)
- User profile management
- Password change and forced resets
- Last login tracking
- User activity monitoring

---

## 🛠 Technical Stack

### Backend
- **Framework**: Flask 2.3+
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: WTForms with Flask-WTF
- **Database Migrations**: Flask-Migrate (Alembic)
- **Password Hashing**: Werkzeug Security

### Frontend
- **Framework**: Bootstrap 5.3
- **Icons**: Bootstrap Icons 1.11
- **JavaScript**: Vanilla JS with modern ES6+
- **Rich Text Editor**: Quill.js
- **Select Components**: Select2
- **Drag & Drop**: SortableJS
- **Charts**: Chart.js

### Database
- **Development**: SQLite
- **Production Ready**: PostgreSQL/MySQL compatible via SQLAlchemy

### Deployment
- **Platform**: PythonAnywhere (cloud hosting)
- **WSGI Server**: Production-ready Flask application
- **Static Files**: Optimized asset delivery

---

## 🏗 Architecture

### Application Structure
```
admin_centre/
├── highland_admin_portal/
│   ├── app/
│   │   ├── blueprints/              # Modular route organization
│   │   │   ├── admin.py             # Admin dashboard & reports
│   │   │   ├── auth.py              # Authentication routes
│   │   │   ├── callsheets.py        # Call sheet management
│   │   │   ├── customers.py         # Customer CRUD & API
│   │   │   ├── customer_stock.py    # Inventory tracking
│   │   │   ├── clearance_stock.py   # Clearance management
│   │   │   ├── forms.py             # Form generation
│   │   │   ├── kb_articles.py       # Knowledge base
│   │   │   ├── kb_categories.py     # KB categories
│   │   │   ├── kb_suppliers.py      # Supplier management
│   │   │   ├── standing_orders.py   # Recurring orders
│   │   │   └── company_updates.py   # Internal comms
│   │   ├── static/
│   │   │   ├── css/style.css        # Custom styling
│   │   │   └── js/script.js         # Custom JavaScript
│   │   ├── templates/               # Jinja2 templates
│   │   ├── models.py                # SQLAlchemy models
│   │   ├── forms.py                 # WTForms definitions
│   │   ├── utils.py                 # Helper functions
│   │   └── __init__.py              # Application factory
│   ├── migrations/                  # Database migrations
│   ├── config.py                    # Environment configuration
│   └── run.py                       # Application entry point
├── populate_dummy_data.py           # Sample data generator
└── requirements.txt                 # Python dependencies
```

### Design Patterns Used
1. **Application Factory Pattern**: Enables multiple app instances with different configs
2. **Blueprint Architecture**: Modular route organization for scalability
3. **Repository Pattern**: Database abstraction through SQLAlchemy models
4. **MVC Pattern**: Clear separation of models, views (templates), and controllers (routes)
5. **Dependency Injection**: Configuration management through environment variables

---

## 🔒 Security Features

### Authentication & Authorization
- ✅ Secure password hashing (Werkzeug + bcrypt)
- ✅ Role-based access control (RBAC)
- ✅ Session management with secure cookies
- ✅ CSRF protection on all forms
- ✅ Login required decorators
- ✅ Password strength validation

### Data Protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (Jinja2 auto-escaping)
- ✅ Environment variable configuration
- ✅ Secret key management
- ✅ Secure session handling

### Production Security Headers
```python
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block'
}
```

---

## 📊 Database Schema

### Core Tables
- **users** - User accounts with role-based permissions
- **customers** - Customer master data
- **customer_addresses** - Multiple delivery locations per customer
- **callsheets** - Call sheet definitions
- **callsheet_entries** - Individual customer entries in callsheets
- **standing_orders** - Recurring order templates
- **standing_order_items** - Products in standing orders
- **standing_order_schedules** - Generated delivery dates
- **customer_stock** - Inventory tracking per customer
- **stock_transactions** - Stock movement history
- **clearance_stock** - Clearance inventory items
- **forms** - Generated form records
- **kb_articles** - Knowledge base content
- **kb_categories** - Article categorization
- **kb_suppliers** - Supplier information
- **company_updates** - Internal announcements
- **todos** - User task management
- **activity_log** - System activity tracking

### Key Relationships
- One-to-Many: Customer → Addresses, Standing Orders
- Many-to-Many: Articles ↔ Categories
- One-to-Many: Callsheets → Entries → Customers
- One-to-Many: Standing Orders → Items, Schedules

---

## 📱 Responsive Design

### Mobile-First Approach
- ✅ Hamburger navigation menu for mobile devices
- ✅ Responsive tables with horizontal scrolling
- ✅ Touch-friendly button sizes and spacing
- ✅ Stacked layouts on small screens
- ✅ Optimized form inputs for mobile

### Breakpoints
- **Mobile**: 375px - 767px (1 column layouts)
- **Tablet**: 768px - 1023px (2 column layouts)
- **Desktop**: 1024px+ (Multi-column layouts)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Quick Start
```bash
# Clone repository
git clone [repository-url]
cd admin_centre

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate secure secret key
cd highland_admin_portal
python generate_secret_key.py

# Initialize database
flask db upgrade

# Create admin user (optional - use init_db.py)
python init_db.py

# Run development server
python run.py
```

Access at: `http://localhost:5000`

### Environment Variables (.env)
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=[generated-secret-key]
DATABASE_URL=sqlite:///admin_portal.db
```

---

## 🎨 UI/UX Highlights

### Design Philosophy
- **Clean & Minimal**: Reduced visual clutter for focus
- **Consistent Color Scheme**: Blue primary theme with status colors
- **Readable Typography**: Segoe UI font family
- **Intuitive Navigation**: Logical grouping and clear labels
- **Feedback**: Toast notifications and loading states

### Custom Features
- Drag-and-drop callsheet ordering
- Real-time form validation
- Auto-complete customer search
- Rich text editing with image support
- Color-coded callsheet statuses
- Sticky navigation sidebar

---

## 📈 Future Enhancements

### Planned Features
- [ ] RESTful API with JWT authentication
- [ ] Email notifications for orders and updates
- [ ] PDF generation improvements (WeasyPrint/ReportLab)
- [ ] Advanced search and filtering
- [ ] Export to Excel (pandas/openpyxl)
- [ ] Real-time notifications (WebSockets)
- [ ] Mobile app (React Native/Flutter)
- [ ] Automated backup system
- [ ] Two-factor authentication
- [ ] Audit log improvements

### Technical Debt
- [ ] Unit test coverage (pytest)
- [ ] Integration tests
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Performance optimization (caching, query optimization)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)

---

## 🎓 Learning Outcomes

### Skills Demonstrated
1. **Full-Stack Development**: End-to-end application development
2. **Database Design**: Normalized schema with proper relationships
3. **Authentication**: Secure user management and RBAC
4. **RESTful APIs**: JSON endpoints for AJAX interactions
5. **Responsive Design**: Mobile-first CSS and Bootstrap
6. **State Management**: Session handling and data persistence
7. **Error Handling**: Graceful degradation and user feedback
8. **Security Best Practices**: OWASP top 10 considerations
9. **Code Organization**: Modular architecture and blueprints
10. **Version Control**: Git workflow and documentation

### Problem-Solving Examples
- **Dynamic Address Selection**: Solved multi-address customer issue with dropdown selection
- **Callsheet Status Colors**: Implemented visual status system with CSS classes
- **Mobile Navigation**: Added hamburger menu for responsive design
- **Rich Text Editing**: Integrated Quill.js with image upload capability
- **Drag-and-Drop**: Implemented SortableJS for intuitive ordering

---

## 📝 Code Quality

### Best Practices Followed
- ✅ PEP 8 Python style guide
- ✅ DRY (Don't Repeat Yourself) principles
- ✅ Separation of concerns
- ✅ Meaningful variable and function names
- ✅ Comprehensive error handling
- ✅ Input validation and sanitization
- ✅ Database query optimization
- ✅ Responsive and accessible UI

### Documentation
- Inline code comments for complex logic
- Docstrings for functions and classes
- README with setup instructions
- Configuration examples
- Deployment guides

---

## 👨‍💻 Developer

**[Your Name]**
- Email: [your-email]
- LinkedIn: [your-linkedin]
- GitHub: [your-github]
- Portfolio: [your-portfolio]

---

## 📄 License

Proprietary - All rights reserved

---

## 🙏 Acknowledgments

Built as a comprehensive portfolio project demonstrating full-stack web development capabilities with Flask and modern web technologies.
