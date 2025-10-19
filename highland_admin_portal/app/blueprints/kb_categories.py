"""
Knowledge Base Categories Blueprint
Handles category management for organizing articles
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Category, Article
from sqlalchemy import func

bp = Blueprint('kb_categories', __name__, url_prefix='/kb/categories')

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Template Routes (Web Pages)
# ============================================================================

@bp.route('/')
@login_required
def list_categories():
    """Categories listing page"""
    categories = Category.query.all()

    # Add article count for each category
    category_data = []
    for category in categories:
        article_count = db.session.query(func.count(Article.id))\
            .filter(Article.category_id == category.id, Article.status == 'published')\
            .scalar()

        category_data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'article_count': article_count,
            'created_at': category.created_at
        })

    return render_template('kb/categories.html', categories=category_data)

# ============================================================================
# API Routes (JSON endpoints)
# ============================================================================

@bp.route('/api', methods=['GET'])
@login_required
def api_list_categories():
    """API: List all categories with article counts"""
    categories = Category.query.all()

    result = []
    for category in categories:
        article_count = db.session.query(func.count(Article.id))\
            .filter(Article.category_id == category.id, Article.status == 'published')\
            .scalar()

        result.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'article_count': article_count
        })

    return jsonify(result)

@bp.route('/api/<int:category_id>', methods=['GET'])
@login_required
def api_get_category(category_id):
    """API: Get specific category"""
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict())

@bp.route('/api', methods=['POST'])
@login_required
@admin_required
def api_create_category():
    """API: Create new category (admin only)"""
    data = request.get_json()

    # Check if category name already exists
    existing = Category.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Category name already exists'}), 400

    category = Category(
        name=data['name'],
        description=data.get('description')
    )

    db.session.add(category)
    db.session.commit()

    flash('Category created successfully!', 'success')
    return jsonify(category.to_dict()), 201

@bp.route('/api/<int:category_id>', methods=['PUT'])
@login_required
@admin_required
def api_update_category(category_id):
    """API: Update category (admin only)"""
    category = Category.query.get_or_404(category_id)
    data = request.get_json()

    if 'name' in data:
        # Check if new name already exists
        existing = Category.query.filter(
            Category.name == data['name'],
            Category.id != category_id
        ).first()
        if existing:
            return jsonify({'error': 'Category name already exists'}), 400
        category.name = data['name']

    if 'description' in data:
        category.description = data['description']

    db.session.commit()

    flash('Category updated successfully!', 'success')
    return jsonify(category.to_dict())

@bp.route('/api/<int:category_id>', methods=['DELETE'])
@login_required
@admin_required
def api_delete_category(category_id):
    """API: Delete category (admin only)"""
    category = Category.query.get_or_404(category_id)

    # Check if category has articles
    article_count = db.session.query(func.count(Article.id))\
        .filter(Article.category_id == category_id)\
        .scalar()

    if article_count > 0:
        return jsonify({
            'error': f'Cannot delete category with {article_count} articles'
        }), 400

    db.session.delete(category)
    db.session.commit()

    flash('Category deleted successfully!', 'success')
    return '', 204
