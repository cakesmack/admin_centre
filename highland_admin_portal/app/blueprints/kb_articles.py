"""
Knowledge Base Articles Blueprint
Handles article management including CRUD operations and approval workflow
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid
from app import db
from app.models import Article, Category, ArticleView, User, Supplier
from sqlalchemy import or_, func

bp = Blueprint('kb_articles', __name__, url_prefix='/kb/articles')

# Image upload configuration
UPLOAD_FOLDER = 'app/static/uploads/kb_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
# Dashboard Routes
# ============================================================================

@bp.route('/dashboard')
@login_required
def kb_dashboard():
    """Knowledge Base Dashboard/Home Page"""
    # Get stats
    total_articles = Article.query.filter_by(status='published').count()
    total_categories = Category.query.count()
    total_suppliers = Supplier.query.count()
    pending_articles = Article.query.filter_by(status='pending').count() if current_user.can_approve_kb_articles() else 0

    # Get recent articles
    recent_articles = Article.query.filter_by(status='published')\
        .order_by(Article.created_at.desc())\
        .limit(5).all()

    # Get popular articles
    popular_articles = Article.query.filter_by(status='published')\
        .order_by(Article.view_count.desc())\
        .limit(5).all()

    # Get categories with article counts
    categories_data = []
    categories = Category.query.all()
    for category in categories:
        article_count = Article.query.filter_by(category_id=category.id, status='published').count()
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'article_count': article_count
        })

    return render_template('kb/dashboard.html',
                         total_articles=total_articles,
                         total_categories=total_categories,
                         total_suppliers=total_suppliers,
                         pending_articles=pending_articles,
                         recent_articles=recent_articles,
                         popular_articles=popular_articles,
                         categories=categories_data)

@bp.route('/admin/approvals')
@login_required
@role_required(['admin', 'manager'])
def admin_approvals():
    """Admin dashboard for article approvals (admin and manager only)"""
    pending_articles = Article.query.filter_by(status='pending')\
        .order_by(Article.updated_at.desc()).all()

    draft_count = Article.query.filter_by(status='draft').count()
    pending_count = Article.query.filter_by(status='pending').count()
    published_count = Article.query.filter_by(status='published').count()

    return render_template('kb/admin_approvals.html',
                         pending_articles=pending_articles,
                         draft_count=draft_count,
                         pending_count=pending_count,
                         published_count=published_count)

# ============================================================================
# Template Routes (Web Pages)
# ============================================================================

@bp.route('/')
@login_required
def list_articles():
    """Articles listing page"""
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')

    # Build query
    query = Article.query

    # Filter by role
    if current_user.role == 'rep':
        query = query.filter(Article.status == 'published')

    # Filter by category
    if category_id:
        query = query.filter(Article.category_id == category_id)

    # Search
    if search:
        query = query.filter(
            or_(
                Article.title.contains(search),
                Article.body.contains(search),
                Article.tags.contains(search)
            )
        )

    articles = query.order_by(Article.created_at.desc()).all()
    categories = Category.query.all()

    return render_template('kb/articles_list.html',
                         articles=articles,
                         categories=categories,
                         selected_category=category_id,
                         search_query=search)

@bp.route('/<int:article_id>')
@login_required
def view_article(article_id):
    """Article detail page"""
    article = Article.query.get_or_404(article_id)

    # Check permissions
    if article.status != 'published' and current_user.role == 'rep':
        flash('You do not have permission to view this article.', 'error')
        return redirect(url_for('kb_articles.list_articles'))

    # Track view
    article_view = ArticleView(article_id=article_id, user_id=current_user.id)
    db.session.add(article_view)
    article.view_count += 1
    db.session.commit()

    return render_template('kb/article_detail.html', article=article)

@bp.route('/new')
@login_required
@role_required(['staff', 'admin'])
def new_article():
    """New article form page"""
    categories = Category.query.all()
    return render_template('kb/article_form.html', article=None, categories=categories)

@bp.route('/<int:article_id>/edit')
@login_required
@role_required(['staff', 'admin'])
def edit_article(article_id):
    """Edit article form page"""
    article = Article.query.get_or_404(article_id)

    # Check permissions - staff can only edit their own articles
    if current_user.role == 'staff' and article.author_id != current_user.id:
        flash('You can only edit your own articles.', 'error')
        return redirect(url_for('kb_articles.list_articles'))

    categories = Category.query.all()
    return render_template('kb/article_form.html', article=article, categories=categories)

# ============================================================================
# API Routes (JSON endpoints)
# ============================================================================

@bp.route('/api', methods=['GET'])
@login_required
def api_list_articles():
    """API: List articles with filtering"""
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search')
    status_filter = request.args.get('status')
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)

    query = Article.query

    # Filter by status based on user role
    if current_user.role == 'rep':
        query = query.filter(Article.status == 'published')
    elif status_filter:
        query = query.filter(Article.status == status_filter)

    # Filter by category
    if category_id:
        query = query.filter(Article.category_id == category_id)

    # Search
    if search:
        query = query.filter(
            or_(
                Article.title.contains(search),
                Article.body.contains(search),
                Article.tags.contains(search)
            )
        )

    articles = query.order_by(Article.created_at.desc()).limit(limit).offset(offset).all()
    return jsonify([article.to_dict(include_body=False) for article in articles])

@bp.route('/api/<int:article_id>', methods=['GET'])
@login_required
def api_get_article(article_id):
    """API: Get specific article"""
    article = Article.query.get_or_404(article_id)

    # Check permissions
    if article.status != 'published' and current_user.role == 'rep':
        return jsonify({'error': 'Cannot view unpublished articles'}), 403

    return jsonify(article.to_dict())

@bp.route('/api', methods=['POST'])
@login_required
@role_required(['staff', 'admin'])
def api_create_article():
    """API: Create new article"""
    data = request.get_json()

    # DEBUG: Log what we received
    print(f"[DEBUG] Received article data: {data}")
    print(f"[DEBUG] Status from request: {data.get('status')}")

    # Allow status to be set on creation (default to draft)
    status = data.get('status', 'draft')
    # Validate status
    if status not in ['draft', 'pending', 'published']:
        print(f"[DEBUG] Invalid status '{status}', defaulting to 'draft'")
        status = 'draft'

    print(f"[DEBUG] Final status being set: {status}")

    article = Article(
        title=data['title'],
        body=data['body'],
        category_id=data.get('category_id'),
        tags=data.get('tags'),
        attachments=data.get('attachments'),
        author_id=current_user.id,
        status=status
    )

    db.session.add(article)
    db.session.commit()

    print(f"[DEBUG] Article saved with ID: {article.id}, Status: {article.status}")

    if status == 'pending':
        flash('Article submitted for review!', 'success')
    else:
        flash('Article created successfully!', 'success')
    return jsonify(article.to_dict()), 201

@bp.route('/api/<int:article_id>', methods=['PUT'])
@login_required
@role_required(['staff', 'admin'])
def api_update_article(article_id):
    """API: Update article"""
    article = Article.query.get_or_404(article_id)

    # Check permissions
    if current_user.role == 'staff' and article.author_id != current_user.id:
        return jsonify({'error': 'Can only edit your own articles'}), 403

    data = request.get_json()

    if 'title' in data:
        article.title = data['title']
    if 'body' in data:
        article.body = data['body']
    if 'category_id' in data:
        article.category_id = data['category_id']
    if 'tags' in data:
        article.tags = data['tags']
    if 'attachments' in data:
        article.attachments = data['attachments']
    if 'status' in data and current_user.role == 'admin':
        article.status = data['status']

    article.updated_at = datetime.utcnow()
    db.session.commit()

    flash('Article updated successfully!', 'success')
    return jsonify(article.to_dict())

@bp.route('/api/<int:article_id>', methods=['DELETE', 'POST'])
@login_required
@role_required(['admin'])
def api_delete_article(article_id):
    """API: Delete article (admin only)"""
    article = Article.query.get_or_404(article_id)

    article_title = article.title
    db.session.delete(article)
    db.session.commit()

    flash(f'Article "{article_title}" has been deleted successfully!', 'success')

    # Return redirect for POST (form submission), or 204 for DELETE (API)
    if request.method == 'POST':
        # Always redirect to articles list after deletion to avoid 404
        return redirect(url_for('kb_articles.list_articles'))
    return '', 204

@bp.route('/api/<int:article_id>/submit', methods=['POST'])
@login_required
@role_required(['staff', 'admin'])
def api_submit_article(article_id):
    """API: Submit article for approval"""
    article = Article.query.get_or_404(article_id)

    # Check permissions
    if current_user.role == 'staff' and article.author_id != current_user.id:
        return jsonify({'error': 'Can only submit your own articles'}), 403

    article.status = 'pending'
    article.updated_at = datetime.utcnow()
    db.session.commit()

    flash('Article submitted for approval!', 'success')
    return jsonify(article.to_dict())

@bp.route('/api/recent', methods=['GET'])
@login_required
def api_recent_articles():
    """API: Get recent published articles"""
    limit = request.args.get('limit', 5, type=int)

    articles = Article.query.filter_by(status='published')\
        .order_by(Article.created_at.desc())\
        .limit(limit).all()

    return jsonify([article.to_dict(include_body=False) for article in articles])

@bp.route('/api/popular', methods=['GET'])
@login_required
def api_popular_articles():
    """API: Get popular articles by view count"""
    limit = request.args.get('limit', 5, type=int)

    articles = Article.query.filter_by(status='published')\
        .order_by(Article.view_count.desc())\
        .limit(limit).all()

    return jsonify([article.to_dict(include_body=False) for article in articles])

@bp.route('/<int:article_id>/approve', methods=['POST'])
@login_required
@role_required(['admin'])
def approve_article(article_id):
    """Approve article for publication"""
    article = Article.query.get_or_404(article_id)

    article.status = 'published'
    article.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f'Article "{article.title}" has been published!', 'success')
    return redirect(request.referrer or url_for('kb_articles.list_articles'))

@bp.route('/<int:article_id>/reject', methods=['POST'])
@login_required
@role_required(['admin'])
def reject_article(article_id):
    """Reject article (return to draft)"""
    article = Article.query.get_or_404(article_id)

    article.status = 'draft'
    article.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f'Article "{article.title}" has been returned to draft.', 'info')
    return redirect(request.referrer or url_for('kb_articles.list_articles'))

@bp.route('/api/upload-image', methods=['POST'])
@login_required
@role_required(['staff', 'admin'])
def upload_image():
    """Upload image for article"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No image selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400

    # Check file size (5MB limit)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > 5 * 1024 * 1024:  # 5MB
        return jsonify({'success': False, 'error': 'File too large. Maximum size is 5MB'}), 400

    try:
        # Create upload folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Save file
        file.save(filepath)

        # Return URL for the uploaded image
        image_url = url_for('static', filename=f'uploads/kb_images/{filename}')

        return jsonify({
            'success': True,
            'image_url': image_url,
            'filename': filename
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
