"""
Populate database with dummy data for promotional video
"""
import os
import sys
from datetime import datetime, timedelta
import random

# Add highland_admin_portal to path
portal_path = os.path.join(os.path.dirname(__file__), 'highland_admin_portal')
sys.path.insert(0, portal_path)

# Change to the highland_admin_portal directory
os.chdir(portal_path)

from app import create_app, db
from app.models import (
    User, Customer, CustomerAddress, Product, Callsheet, CallsheetEntry,
    TodoItem, CompanyUpdate, Form, CustomerStock, StockTransaction,
    StandingOrder, StandingOrderItem, ClearanceStock,
    Supplier, Category, Article, ArticleView
)

def clear_existing_data():
    """Clear existing data for a fresh start"""
    print("Clearing existing data...")

    # Order matters due to foreign key constraints
    ArticleView.query.delete()
    Article.query.delete()
    Category.query.delete()
    Supplier.query.delete()
    ClearanceStock.query.delete()
    StandingOrderItem.query.delete()
    StandingOrder.query.delete()
    StockTransaction.query.delete()
    CustomerStock.query.delete()
    Form.query.delete()
    CallsheetEntry.query.delete()
    Callsheet.query.delete()
    CustomerAddress.query.delete()
    Customer.query.delete()
    Product.query.delete()
    CompanyUpdate.query.delete()
    TodoItem.query.delete()

    # Keep users but clear their data
    users = User.query.all()
    for user in users:
        if user.username != 'admin':
            db.session.delete(user)

    db.session.commit()
    print("Existing data cleared!")

def create_users():
    """Create demo users"""
    print("Creating users...")

    users_data = [
        {
            'username': 'admin',
            'email': 'admin@highlandhygiene.com',
            'full_name': 'Sarah MacLeod',
            'role': 'admin',
            'job_title': 'Operations Manager',
            'direct_phone': '01463 234567',
            'mobile_phone': '07700 900123'
        },
        {
            'username': 'jsmith',
            'email': 'jsmith@highlandhygiene.com',
            'full_name': 'James Smith',
            'role': 'user',
            'job_title': 'Sales Representative',
            'direct_phone': '01463 234568',
            'mobile_phone': '07700 900124'
        },
        {
            'username': 'efraser',
            'email': 'efraser@highlandhygiene.com',
            'full_name': 'Emma Fraser',
            'role': 'user',
            'job_title': 'Account Manager',
            'direct_phone': '01463 234569',
            'mobile_phone': '07700 900125'
        },
        {
            'username': 'rcameron',
            'email': 'rcameron@highlandhygiene.com',
            'full_name': 'Robert Cameron',
            'role': 'user',
            'job_title': 'Warehouse Supervisor',
            'direct_phone': '01463 234570',
            'mobile_phone': '07700 900126'
        }
    ]

    created_users = []
    for user_data in users_data:
        existing = User.query.filter_by(username=user_data['username']).first()
        if existing:
            created_users.append(existing)
            continue

        user = User(**user_data)
        user.set_password('Password123!')
        user.is_active = True
        user.must_change_password = False
        user.last_login = datetime.now() - timedelta(hours=random.randint(1, 48))
        db.session.add(user)
        created_users.append(user)

    db.session.commit()
    print(f"Created {len(created_users)} users!")
    return created_users

def create_customers():
    """Create demo customers"""
    print("Creating customers...")

    customers_data = [
        {
            'account_number': 'CUST001',
            'name': 'Highland Hotel',
            'contact_name': 'John MacKenzie',
            'phone': '01463 123456',
            'email': 'john@highlandhotel.co.uk',
            'notes': 'Premium customer - weekly deliveries',
            'callsheet_notes': 'Prefers morning deliveries before 10am',
            'addresses': [
                {'label': 'Main Hotel', 'phone': '01463 123456', 'street': '15 High Street', 'city': 'Inverness', 'zip': 'IV1 1AA', 'is_primary': True},
                {'label': 'Annex Building', 'phone': '01463 123457', 'street': '17 High Street', 'city': 'Inverness', 'zip': 'IV1 1AA', 'is_primary': False}
            ]
        },
        {
            'account_number': 'CUST002',
            'name': 'Lochside Restaurant',
            'contact_name': 'Emma Brown',
            'phone': '01463 654321',
            'email': 'emma@lochside.co.uk',
            'notes': 'Requires eco-friendly products',
            'callsheet_notes': 'Call between 2-4pm (closed lunch)',
            'addresses': [
                {'label': 'Main Restaurant', 'phone': '01463 654321', 'street': '42 Ness Bank', 'city': 'Inverness', 'zip': 'IV2 4SF', 'is_primary': True}
            ]
        },
        {
            'account_number': 'CUST003',
            'name': 'Cafe Ness',
            'contact_name': 'Robert Johnson',
            'phone': '01463 789123',
            'email': 'rob@cafeness.com',
            'notes': 'Small orders, weekly',
            'callsheet_notes': 'Manager available mornings only',
            'addresses': [
                {'label': 'Cafe', 'phone': '01463 789123', 'street': '8 Castle Street', 'city': 'Inverness', 'zip': 'IV2 3EA', 'is_primary': True}
            ]
        },
        {
            'account_number': 'CUST004',
            'name': 'Morangie House Hotel',
            'contact_name': 'Duncan Ross',
            'phone': '01862 892281',
            'email': 'info@morangiehouse.com',
            'notes': 'Large account - bi-weekly orders',
            'callsheet_notes': 'Contact head housekeeper',
            'addresses': [
                {'label': 'Main House', 'phone': '01862 892281', 'street': 'Morangie Road', 'city': 'Tain', 'zip': 'IV19 1PY', 'is_primary': True},
                {'label': 'Gatehouse', 'phone': '01862 892282', 'street': 'Morangie Road Gate', 'city': 'Tain', 'zip': 'IV19 1PY', 'is_primary': False}
            ]
        },
        {
            'account_number': 'CUST005',
            'name': 'Mansfield Castle Hotel',
            'contact_name': 'Fiona Campbell',
            'phone': '01862 782345',
            'email': 'bookings@mansfield.co.uk',
            'notes': 'Historic property - careful with deliveries',
            'callsheet_notes': 'Ring doorbell at service entrance',
            'addresses': [
                {'label': 'Castle', 'phone': '01862 782345', 'street': 'Castle Drive', 'city': 'Tain', 'zip': 'IV19 1AB', 'is_primary': True}
            ]
        },
        {
            'account_number': 'CUST006',
            'name': 'Glen Ord Distillery',
            'contact_name': 'Andrew Stewart',
            'phone': '01463 872004',
            'email': 'andrew@glenord.com',
            'notes': 'Industrial supplies only',
            'callsheet_notes': 'Contact facility manager',
            'addresses': [
                {'label': 'Distillery', 'phone': '01463 872004', 'street': 'Glen Ord', 'city': 'Muir of Ord', 'zip': 'IV6 7UJ', 'is_primary': True}
            ]
        },
        {
            'account_number': 'CUST007',
            'name': 'The Royal Hotel',
            'contact_name': 'Margaret Wilson',
            'phone': '01463 231353',
            'email': 'reception@royalhotel.com',
            'notes': 'VIP customer - priority service',
            'callsheet_notes': 'Speak with Margaret or assistant manager',
            'addresses': [
                {'label': 'Hotel', 'phone': '01463 231353', 'street': '18 Academy Street', 'city': 'Inverness', 'zip': 'IV1 1LT', 'is_primary': True}
            ]
        },
        {
            'account_number': 'CUST008',
            'name': 'Riverside Nursing Home',
            'contact_name': 'Julie Thomson',
            'phone': '01463 242424',
            'email': 'admin@riverside-care.co.uk',
            'notes': 'Healthcare facility - strict hygiene requirements',
            'callsheet_notes': 'Use service entrance, sign in required',
            'addresses': [
                {'label': 'Main Building', 'phone': '01463 242424', 'street': '56 Old Edinburgh Road', 'city': 'Inverness', 'zip': 'IV2 3HN', 'is_primary': True}
            ]
        }
    ]

    created_customers = []
    for cust_data in customers_data:
        addresses = cust_data.pop('addresses')
        customer = Customer(**cust_data)
        db.session.add(customer)
        db.session.flush()  # Get customer ID

        for addr_data in addresses:
            address = CustomerAddress(customer_id=customer.id, **addr_data)
            db.session.add(address)

        created_customers.append(customer)

    db.session.commit()
    print(f"Created {len(created_customers)} customers with addresses!")
    return created_customers

def create_products():
    """Create demo products"""
    print("Creating products...")

    products_data = [
        {'code': 'HYG001', 'name': 'Toilet Rolls (12 pack)', 'description': 'Premium 3-ply toilet tissue'},
        {'code': 'HYG002', 'name': 'Hand Soap Refill 5L', 'description': 'Antibacterial liquid hand soap'},
        {'code': 'HYG003', 'name': 'Paper Towels (6 rolls)', 'description': 'Blue roll centrefeed'},
        {'code': 'HYG004', 'name': 'Sanitizer Gel 500ml', 'description': 'Alcohol-based hand sanitizer'},
        {'code': 'CAT001', 'name': 'Disposable Plates 10"', 'description': 'Biodegradable dinner plates (50 pack)'},
        {'code': 'CAT002', 'name': 'Plastic Cutlery Pack', 'description': 'Knives, forks, spoons (100 pieces)'},
        {'code': 'CAT003', 'name': 'Napkins White (200)', 'description': '33cm x 33cm 2-ply napkins'},
        {'code': 'CAT004', 'name': 'Food Containers 500ml', 'description': 'Microwave safe containers (50 pack)'},
        {'code': 'CLN001', 'name': 'Floor Cleaner 5L', 'description': 'Multi-surface floor cleaning solution'},
        {'code': 'CLN002', 'name': 'Bleach 5L', 'description': 'Industrial strength bleach'},
        {'code': 'CLN003', 'name': 'Glass Cleaner 750ml', 'description': 'Streak-free glass cleaner'},
        {'code': 'CLN004', 'name': 'Disinfectant Spray 5L', 'description': 'Hospital-grade disinfectant'},
    ]

    products = []
    for prod_data in products_data:
        product = Product(**prod_data)
        db.session.add(product)
        products.append(product)

    db.session.commit()
    print(f"Created {len(products)} products!")
    return products

def create_callsheets(users, customers):
    """Create demo callsheets"""
    print("Creating callsheets...")

    # Create callsheet for this week
    today = datetime.now()
    callsheet = Callsheet(
        name=f"Week {today.strftime('%W')} - Monday Calls",
        day_of_week='Monday',
        month=today.month,
        year=today.year,
        is_active=True,
        created_by=users[0].id,
        created_at=today - timedelta(days=2)
    )
    db.session.add(callsheet)
    db.session.flush()

    # Add entries for some customers
    statuses = ['not_called', 'ordered', 'no_answer', 'declined', 'callback']
    for i, customer in enumerate(customers[:6]):
        status = statuses[i % len(statuses)]
        entry = CallsheetEntry(
            callsheet_id=callsheet.id,
            customer_id=customer.id,
            address_id=customer.addresses[0].id if customer.addresses else None,
            address_label=customer.addresses[0].label if customer.addresses else None,
            call_status=status,
            called_by=users[random.randint(1, len(users)-1)].full_name if status != 'not_called' else None,
            call_date=datetime.now() - timedelta(hours=random.randint(1, 6)) if status != 'not_called' else None,
            person_spoken_to=customer.contact_name if status in ['ordered', 'callback'] else None,
            callback_time='2:00 PM' if status == 'callback' else None,
            user_id=users[random.randint(0, len(users)-1)].id,
            position=i
        )
        db.session.add(entry)

    db.session.commit()
    print("Created callsheet with entries!")
    return callsheet

def create_todo_items(users):
    """Create demo todo items"""
    print("Creating todo items...")

    todos_data = [
        ('Follow up with Highland Hotel about monthly invoice', False),
        ('Check stock levels for hand sanitizer', True),
        ('Schedule meeting with new supplier', False),
        ('Update product pricing for Q2', False),
        ('Review callsheet for tomorrow', True),
    ]

    for user in users[:2]:  # First 2 users get todos
        for text, completed in todos_data[:3]:
            todo = TodoItem(
                text=text,
                completed=completed,
                user_id=user.id,
                created_at=datetime.now() - timedelta(days=random.randint(0, 5))
            )
            db.session.add(todo)

    db.session.commit()
    print("Created todo items!")

def create_company_updates(users):
    """Create demo company updates"""
    print("Creating company updates...")

    updates_data = [
        {
            'title': 'New Eco-Friendly Product Line',
            'message': 'Excited to announce our new range of biodegradable products! Now available for order.',
            'priority': 'important',
            'category': 'products',
            'sticky': True
        },
        {
            'title': 'Holiday Schedule - Christmas',
            'message': 'Office will be closed Dec 25-26. Last delivery Dec 23rd, first delivery Dec 28th.',
            'priority': 'urgent',
            'category': 'general',
            'is_event': True,
            'event_date': datetime(2025, 12, 25),
            'sticky': True
        },
        {
            'title': 'Team Meeting - Thursday 10am',
            'message': 'Monthly sales review and planning session. All staff welcome.',
            'priority': 'normal',
            'category': 'general',
            'is_event': True,
            'event_date': datetime.now() + timedelta(days=2)
        },
        {
            'title': 'New Customer Welcome',
            'message': 'Please join us in welcoming our newest customer, Riverside Nursing Home!',
            'priority': 'normal',
            'category': 'general'
        }
    ]

    for update_data in updates_data:
        update = CompanyUpdate(
            **update_data,
            user_id=users[0].id,
            created_at=datetime.now() - timedelta(days=random.randint(0, 7))
        )
        db.session.add(update)

    db.session.commit()
    print("Created company updates!")

def create_customer_stock(customers, products, users):
    """Create demo customer stock"""
    print("Creating customer stock...")

    # Create stock items for first few customers
    for customer in customers[:4]:
        for product in products[:5]:
            stock = CustomerStock(
                customer_id=customer.id,
                product_code=product.code,
                product_name=product.name,
                current_stock=random.randint(0, 50),
                reorder_level=random.randint(5, 15),
                created_at=datetime.now() - timedelta(days=random.randint(10, 60))
            )
            db.session.add(stock)
            db.session.flush()

            # Add some stock transactions
            for _ in range(random.randint(1, 3)):
                transaction = StockTransaction(
                    stock_item_id=stock.id,
                    transaction_type=random.choice(['stock_in', 'stock_out']),
                    quantity=random.randint(5, 20),
                    reference=f"ORD{random.randint(1000, 9999)}",
                    notes='Regular delivery' if random.random() > 0.5 else 'Rush order',
                    transaction_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                    created_by=users[random.randint(0, len(users)-1)].id
                )
                db.session.add(transaction)

    db.session.commit()
    print("Created customer stock!")

def create_standing_orders(customers, products, users):
    """Create demo standing orders"""
    print("Creating standing orders...")

    # Create standing orders for a few customers
    for customer in customers[:3]:
        standing_order = StandingOrder(
            customer_id=customer.id,
            delivery_days='0,3',  # Monday and Thursday
            start_date=datetime.now().date() - timedelta(days=30),
            status='active',
            special_instructions=f'Please deliver to {customer.addresses[0].label if customer.addresses else "main entrance"}',
            created_by=users[0].id,
            created_at=datetime.now() - timedelta(days=30)
        )
        db.session.add(standing_order)
        db.session.flush()

        # Add items to standing order
        for product in products[:4]:
            item = StandingOrderItem(
                standing_order_id=standing_order.id,
                product_code=product.code,
                product_name=product.name,
                quantity=random.randint(2, 10),
                unit_type='units'
            )
            db.session.add(item)

    db.session.commit()
    print("Created standing orders!")

def create_clearance_stock(users, products):
    """Create demo clearance stock"""
    print("Creating clearance stock...")

    clearance_items = [
        {
            'qty': 500,
            'qty_sold': 127,
            'supplier_code': 'SUP-HYG-2024-001',
            'his_code': 'HYG005',
            'description': 'Premium Hand Towels - Discontinued Line',
            'cost_price': 1.25,
            'total_price': 625.00,
            'pallet': 'A1'
        },
        {
            'qty': 300,
            'qty_sold': 89,
            'supplier_code': 'SUP-CAT-2024-012',
            'his_code': 'CAT007',
            'description': 'Food Storage Bags (Bulk)',
            'cost_price': 2.50,
            'total_price': 750.00,
            'pallet': 'A1'
        },
        {
            'qty': 200,
            'qty_sold': 0,
            'supplier_code': 'SUP-CLN-2024-005',
            'his_code': 'CLN008',
            'description': 'Eco Surface Cleaner - New Formula',
            'cost_price': 3.75,
            'total_price': 750.00,
            'pallet': 'B2'
        }
    ]

    for item_data in clearance_items:
        item = ClearanceStock(
            **item_data,
            created_by=users[0].id,
            created_at=datetime.now() - timedelta(days=random.randint(5, 30))
        )
        db.session.add(item)

    db.session.commit()
    print("Created clearance stock!")

def create_knowledge_base(users):
    """Create demo knowledge base articles"""
    print("Creating knowledge base...")

    # Create suppliers
    suppliers_data = [
        {'name': 'Highland Supplies Ltd', 'website': 'https://highlandsupplies.co.uk', 'contact_info': 'sales@highlandsupplies.co.uk'},
        {'name': 'NorthCo Distributors', 'website': 'https://northco.com', 'contact_info': 'info@northco.com'},
        {'name': 'EcoProducts Scotland', 'website': 'https://ecoproducts.scot', 'contact_info': 'hello@ecoproducts.scot'}
    ]

    suppliers = []
    for sup_data in suppliers_data:
        supplier = Supplier(**sup_data)
        db.session.add(supplier)
        suppliers.append(supplier)

    db.session.flush()

    # Create categories
    categories_data = [
        {'name': 'Product Information', 'description': 'Details about our products', 'color': '#3B82F6'},
        {'name': 'Procedures', 'description': 'Standard operating procedures', 'color': '#10B981'},
        {'name': 'Troubleshooting', 'description': 'Common issues and solutions', 'color': '#F59E0B'},
        {'name': 'Supplier Info', 'description': 'Supplier contact and ordering info', 'color': '#8B5CF6'}
    ]

    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        categories.append(category)

    db.session.flush()

    # Create articles
    articles_data = [
        {
            'title': 'How to Process a Rush Order',
            'body': '''# Rush Order Procedure

## Overview
Rush orders require special handling to ensure timely delivery.

## Steps
1. Check stock availability immediately
2. Contact warehouse supervisor
3. Prioritize picking and packing
4. Arrange same-day or next-day delivery
5. Notify customer of dispatch time

## Important Notes
- Rush orders incur additional delivery charges
- Cutoff time is 2 PM for same-day delivery
- Always confirm with customer before processing

## Contact
For urgent queries, contact Robert Cameron (Warehouse Supervisor) on 01463 234570.''',
            'category_id': 2,
            'status': 'published',
            'tags': 'orders, urgent, delivery'
        },
        {
            'title': 'Hand Sanitizer Product Range',
            'body': '''# Hand Sanitizer Products

## Available Products
- HYG004: Sanitizer Gel 500ml (70% alcohol)
- HYG008: Sanitizer Foam 1L (65% alcohol)
- HYG012: Sanitizer Spray 250ml (70% alcohol)

## Usage Guidelines
All products meet BS EN 1276 standards for antibacterial efficacy.

## Storage
Store in cool, dry place away from heat sources. Maximum shelf life: 2 years.

## Safety Information
Highly flammable. Keep away from open flames. For external use only.''',
            'category_id': 1,
            'status': 'published',
            'tags': 'products, hygiene, sanitizer'
        },
        {
            'title': 'Highland Supplies Ltd - Ordering Guide',
            'body': '''# Highland Supplies Ltd

## Contact Information
- **Email:** sales@highlandsupplies.co.uk
- **Phone:** 01463 567890
- **Order Portal:** https://portal.highlandsupplies.co.uk

## Ordering Process
1. Login to supplier portal with credentials
2. Add items to cart
3. Submit order before 3 PM for next-day delivery
4. Order confirmation sent via email

## Payment Terms
Net 30 days from invoice date

## Delivery Schedule
- Monday-Friday: Standard delivery
- Minimum order value: £50
- Free delivery over £200

## Account Manager
Contact: Jennifer MacLeod
Direct: 01463 567891
Email: jennifer.macleod@highlandsupplies.co.uk''',
            'category_id': 4,
            'supplier_id': 1,
            'status': 'published',
            'tags': 'supplier, ordering, contact'
        },
        {
            'title': 'Dealing with Stock Discrepancies',
            'body': '''# Stock Discrepancy Procedure

## When to Use
Use this procedure when physical stock doesn't match system records.

## Investigation Steps
1. **Verify the Count**
   - Recount the physical stock
   - Check all storage locations
   - Review recent transactions

2. **Check for Errors**
   - Review recent deliveries
   - Check for unreported customer returns
   - Verify picking accuracy

3. **Documentation**
   - Document the discrepancy
   - Note date discovered and staff involved
   - Record actual vs. expected quantity

4. **Adjustment**
   - Use stock adjustment function
   - Select "adjustment" transaction type
   - Add detailed notes explaining variance

## Reporting
Discrepancies over £100 value must be reported to the Operations Manager.

## Prevention
- Regular spot checks
- Proper training on system usage
- Clear labeling of stock locations''',
            'category_id': 3,
            'status': 'published',
            'tags': 'stock, procedures, troubleshooting'
        },
        {
            'title': 'Eco-Friendly Product Range Overview',
            'body': '''# Eco-Friendly Products

## Our Commitment
Highland Hygiene is committed to offering sustainable, environmentally-friendly products.

## Product Categories

### Biodegradable Items
- Disposable plates and cutlery
- Food containers
- Napkins and paper products

### Recycled Content
- Paper towels (70% recycled content)
- Toilet tissue (100% recycled)

### Concentrated Solutions
- Multi-surface cleaners (reduces packaging)
- Floor care products (refill stations available)

## Certifications
All eco products carry relevant environmental certifications:
- EU Ecolabel
- Nordic Swan
- FSC Certified

## Customer Benefits
- Reduced environmental impact
- Cost savings on waste disposal
- Enhanced brand reputation
- Compliance with environmental regulations

## Ordering
Look for the green leaf symbol in product codes or filter by "Eco" category in the system.''',
            'category_id': 1,
            'status': 'published',
            'tags': 'products, eco-friendly, sustainability'
        },
        {
            'title': 'Customer Callsheet Best Practices',
            'body': '''# Callsheet Best Practices

## Preparation
- Review customer notes before calling
- Check previous order history
- Note any outstanding issues or special requirements

## During the Call
1. Greet professionally and introduce yourself
2. Confirm you're speaking with the decision maker
3. Ask about current needs and stock levels
4. Mention any promotions or new products
5. Confirm delivery details and special instructions
6. Thank them for their business

## Recording Information
- Update call status immediately
- Note who you spoke with
- Record any callback times accurately
- Add relevant notes for future reference

## Tips for Success
- Best calling times: 9-11 AM, 2-4 PM
- Avoid calling during busy service times
- Build rapport with regular contacts
- Follow up on promises made

## Handling Common Scenarios

### No Answer
- Try at different times of day
- Leave voicemail if appropriate
- Send follow-up email

### Declined Order
- Be polite and professional
- Ask if they'd like to schedule next contact
- Update customer notes with any feedback

### Callback Requested
- Schedule specific time
- Set reminder in system
- Ensure callback happens as promised''',
            'category_id': 2,
            'status': 'published',
            'tags': 'callsheets, sales, procedures'
        }
    ]

    for i, article_data in enumerate(articles_data):
        article = Article(
            **article_data,
            author_id=users[i % len(users)].id,
            view_count=random.randint(10, 150),
            created_at=datetime.now() - timedelta(days=random.randint(5, 60))
        )
        db.session.add(article)
        db.session.flush()

        # Add some article views
        for _ in range(random.randint(5, 20)):
            view = ArticleView(
                article_id=article.id,
                user_id=users[random.randint(0, len(users)-1)].id,
                viewed_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(view)

    db.session.commit()
    print("Created knowledge base with suppliers, categories, and articles!")

def create_forms(users, customers):
    """Create demo forms"""
    print("Creating forms...")

    forms_data = [
        {
            'type': 'customer_feedback',
            'data': '{"customer": "Highland Hotel", "rating": 5, "comments": "Excellent service as always"}',
            'is_completed': True,
            'completed_date': datetime.now() - timedelta(days=2)
        },
        {
            'type': 'delivery_note',
            'data': '{"customer": "Lochside Restaurant", "items": "HYG001 x 10, CLN001 x 2", "delivered": true}',
            'is_completed': True,
            'completed_date': datetime.now() - timedelta(hours=5)
        },
        {
            'type': 'incident_report',
            'data': '{"date": "2025-10-18", "description": "Delivery vehicle breakdown", "resolved": true}',
            'is_completed': True,
            'completed_date': datetime.now() - timedelta(days=1)
        },
        {
            'type': 'stock_check',
            'data': '{"location": "Warehouse A", "status": "in_progress"}',
            'is_completed': False
        }
    ]

    for form_data in forms_data:
        form = Form(
            **form_data,
            user_id=users[random.randint(0, len(users)-1)].id,
            completed_by=users[random.randint(0, len(users)-1)].id if form_data['is_completed'] else None,
            date_created=datetime.now() - timedelta(days=random.randint(1, 7))
        )
        db.session.add(form)

    db.session.commit()
    print("Created forms!")

def main():
    """Main function to populate database"""
    app = create_app()

    with app.app_context():
        print("\n" + "="*50)
        print("POPULATING DATABASE WITH DUMMY DATA")
        print("="*50 + "\n")

        # Clear existing data (automated for promotional video)
        clear_existing_data()

        # Create all data
        users = create_users()
        customers = create_customers()
        products = create_products()
        create_callsheets(users, customers)
        create_todo_items(users)
        create_company_updates(users)
        create_customer_stock(customers, products, users)
        create_standing_orders(customers, products, users)
        create_clearance_stock(users, products)
        create_knowledge_base(users)
        create_forms(users, customers)

        print("\n" + "="*50)
        print("DATABASE POPULATED SUCCESSFULLY!")
        print("="*50)
        print("\nSummary:")
        print(f"- Users: {User.query.count()}")
        print(f"- Customers: {Customer.query.count()}")
        print(f"- Products: {Product.query.count()}")
        print(f"- Callsheets: {Callsheet.query.count()}")
        print(f"- Callsheet Entries: {CallsheetEntry.query.count()}")
        print(f"- Todo Items: {TodoItem.query.count()}")
        print(f"- Company Updates: {CompanyUpdate.query.count()}")
        print(f"- Customer Stock Items: {CustomerStock.query.count()}")
        print(f"- Stock Transactions: {StockTransaction.query.count()}")
        print(f"- Standing Orders: {StandingOrder.query.count()}")
        print(f"- Clearance Items: {ClearanceStock.query.count()}")
        print(f"- KB Suppliers: {Supplier.query.count()}")
        print(f"- KB Categories: {Category.query.count()}")
        print(f"- KB Articles: {Article.query.count()}")
        print(f"- Forms: {Form.query.count()}")
        print("\nLogin credentials:")
        print("Username: admin")
        print("Password: Password123!")

if __name__ == '__main__':
    main()
