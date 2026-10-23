from flask import Blueprint

# 1. Buat dulu instance Blueprint-nya
items_bp = Blueprint('items', __name__, url_prefix='/api/items')
categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

# 2. BARU import file handler di paling bawah
# Pastikan nama file di folder routes kamu adalah categories.py dan items.py
from app.routes import categories, items