"""
Knowledge Base Suppliers Blueprint
Handles supplier information management
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from app import db
from app.models import Supplier

bp = Blueprint('kb_suppliers', __name__, url_prefix='/kb/suppliers')

def role_required(allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in allowed_roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================================================
# Template Routes (Web Pages)
# ============================================================================

@bp.route('/')
@login_required
def list_suppliers():
    """Suppliers listing page"""
    search = request.args.get('search', '')

    query = Supplier.query

    if search:
        query = query.filter(Supplier.name.contains(search))

    suppliers = query.order_by(Supplier.name).all()

    return render_template('kb/suppliers.html',
                         suppliers=suppliers,
                         search_query=search)

@bp.route('/<int:supplier_id>')
@login_required
def view_supplier(supplier_id):
    """Supplier detail page"""
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('kb/supplier_detail.html', supplier=supplier)

@bp.route('/new')
@login_required
@role_required(['staff', 'admin'])
def new_supplier():
    """New supplier form page"""
    return render_template('kb/supplier_form.html', supplier=None)

@bp.route('/<int:supplier_id>/edit')
@login_required
@role_required(['staff', 'admin'])
def edit_supplier(supplier_id):
    """Edit supplier form page"""
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('kb/supplier_form.html', supplier=supplier)

# ============================================================================
# API Routes (JSON endpoints)
# ============================================================================

@bp.route('/api', methods=['GET'])
@login_required
def api_list_suppliers():
    """API: List all suppliers with optional search"""
    search = request.args.get('search')

    query = Supplier.query

    if search:
        query = query.filter(Supplier.name.contains(search))

    suppliers = query.order_by(Supplier.name).all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

@bp.route('/api/<int:supplier_id>', methods=['GET'])
@login_required
def api_get_supplier(supplier_id):
    """API: Get specific supplier"""
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify(supplier.to_dict())

@bp.route('/api', methods=['POST'])
@login_required
@role_required(['staff', 'admin'])
def api_create_supplier():
    """API: Create new supplier"""
    data = request.get_json()

    # Check if supplier name already exists
    existing = Supplier.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Supplier name already exists'}), 400

    supplier = Supplier(
        name=data['name'],
        description=data.get('description'),
        contact_name=data.get('contact_name'),
        phone=data.get('phone'),
        email=data.get('email'),
        website=data.get('website'),
        address=data.get('address'),
        category=data.get('category'),
        notes=data.get('notes')
    )

    db.session.add(supplier)
    db.session.commit()

    flash('Supplier created successfully!', 'success')
    return jsonify(supplier.to_dict()), 201

@bp.route('/api/<int:supplier_id>', methods=['PUT'])
@login_required
@role_required(['staff', 'admin'])
def api_update_supplier(supplier_id):
    """API: Update supplier"""
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()

    if 'name' in data:
        # Check if new name already exists
        existing = Supplier.query.filter(
            Supplier.name == data['name'],
            Supplier.id != supplier_id
        ).first()
        if existing:
            return jsonify({'error': 'Supplier name already exists'}), 400
        supplier.name = data['name']

    if 'description' in data:
        supplier.description = data['description']
    if 'contact_name' in data:
        supplier.contact_name = data['contact_name']
    if 'phone' in data:
        supplier.phone = data['phone']
    if 'email' in data:
        supplier.email = data['email']
    if 'website' in data:
        supplier.website = data['website']
    if 'address' in data:
        supplier.address = data['address']
    if 'category' in data:
        supplier.category = data['category']
    if 'notes' in data:
        supplier.notes = data['notes']

    supplier.updated_at = datetime.utcnow()
    db.session.commit()

    flash('Supplier updated successfully!', 'success')
    return jsonify(supplier.to_dict())

@bp.route('/api/<int:supplier_id>', methods=['DELETE'])
@login_required
@role_required(['admin'])
def api_delete_supplier(supplier_id):
    """API: Delete supplier (admin only)"""
    supplier = Supplier.query.get_or_404(supplier_id)

    db.session.delete(supplier)
    db.session.commit()

    flash('Supplier deleted successfully!', 'success')
    return '', 204
