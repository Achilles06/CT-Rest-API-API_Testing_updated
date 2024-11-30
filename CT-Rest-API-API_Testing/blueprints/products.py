# blueprints/product.py

from flask import Blueprint, jsonify, request
from models import db, Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    # Get page and per_page from query parameters with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Paginate the products
    products_pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)

    # Get paginated products
    products = products_pagination.items

    # Create response format
    result = [{
        'id': prod.id,
        'name': prod.name,
        'price': prod.price
    } for prod in products]

    # Include pagination metadata in the response
    return jsonify({
        'products': result,
        'total': products_pagination.total,
        'page': products_pagination.page,
        'pages': products_pagination.pages,
        'per_page': products_pagination.per_page
    }), 200
